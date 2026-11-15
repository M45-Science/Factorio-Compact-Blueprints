"""Lossless translated spatial motifs, with graph and ordering ablation controls.

Only disjoint cells are matched; rotations, reflection and approximate matches
are deliberately excluded. Coordinates are matched on an exact integer lattice.
The original order, IDs, numeric types and signed zero are explicit columns.
"""
from collections import Counter, defaultdict
import copy
import math
import zlib

import msgpack

from compact import (pack, read_varints, sequence, table, unsequence, untable,
                     unzigzag, varint, zigzag)


def canonical(value):
    if isinstance(value, dict):
        return {k: (value[k] if k == "items" and isinstance(value[k], dict)
                    else canonical(value[k])) for k in sorted(value)}
    if isinstance(value, list):
        return [canonical(v) for v in value]
    return value


def template_key(value):
    return pack(canonical(value))


def references(value, row_index, idmap):
    if isinstance(value, dict):
        return {k: (msgpack.ExtType(1, varint(zigzag(idmap[v] - row_index)))
                    if k == "entity_id" and type(v) is int and v in idmap
                    else references(v, row_index, idmap)) for k, v in value.items()}
    if isinstance(value, list):
        return [references(v, row_index, idmap) for v in value]
    return value


def normalize_rows(rows, entity):
    rows = copy.deepcopy(rows)
    if not entity:
        return rows
    idmap = {r["entity_number"]: i for i, r in enumerate(rows)}
    for i, row in enumerate(rows):
        if "connections" in row:
            row["connections"] = references(row["connections"], i, idmap)
        if isinstance(row.get("neighbours"), list):
            row["neighbours"] = [msgpack.ExtType(1, varint(zigzag(idmap[v] - i)))
                                 if type(v) is int and v in idmap else v
                                 for v in row["neighbours"]]
    return rows


def restore_references(value, row_index, ids):
    if isinstance(value, msgpack.ExtType):
        if value.code != 1:
            raise ValueError("unknown reference marker")
        values = list(read_varints(value.data))
        if len(values) != 1:
            raise ValueError("invalid reference")
        return ids[row_index + unzigzag(values[0])]
    if isinstance(value, dict):
        return {k: restore_references(v, row_index, ids) for k, v in value.items()}
    if isinstance(value, list):
        return [restore_references(v, row_index, ids) for v in value]
    return value


def unnormalize_rows(rows):
    ids = [r.get("entity_number") for r in rows]
    return [restore_references(row, i, ids) for i, row in enumerate(rows)]


def numeric_type(v):
    return int(type(v) is float) | (2 if isinstance(v, float) and v == 0
                                   and math.copysign(1, v) < 0 else 0)


def restore_number(v, scale, typ):
    if typ & 2:
        return -0.0
    return v / scale if typ & 1 else v // scale


def spatial_order(rows):
    return sorted(range(len(rows)), key=lambda i: (rows[i]["position"]["y"],
                                                  rows[i]["position"]["x"], i))


def reordered(rows, entity):
    order = spatial_order(rows)
    return [1, table([rows[i] for i in order], entity, template_key), sequence(order)]


def spatial_cells(descriptors, width, height):
    cells = defaultdict(list)
    for tid, x, y, i in descriptors:
        cells[(y // height if height else 0, x // width if width else 0)].append((tid, x, y, i))
    patterns, lookup, placements, counts = [], {}, [], Counter()
    for cell in sorted(cells):
        contents = cells[cell]
        ax, ay = min(v[1] for v in contents), min(v[2] for v in contents)
        contents.sort(key=lambda v: (v[2], v[1], v[0], v[3]))
        pattern = tuple((tid, x - ax, y - ay) for tid, x, y, _ in contents)
        pid = lookup.get(pattern)
        if pid is None:
            pid = len(patterns)
            lookup[pattern] = pid
            patterns.append(pattern)
        counts[pid] += 1
        placements.append((pid, ax, ay, [v[3] for v in contents]))
    # Shortlist by estimated reuse after accounting for instance overhead. Final
    # selection below compares actual zlib-compressed bytes, including order.
    score = sum((count - 1) * len(patterns[pid]) * 6 - count * 8
                for pid, count in counts.items() if count > 1 and len(patterns[pid]) >= 2)
    repeated_entities = sum(count * len(patterns[pid]) for pid, count in counts.items()
                            if count > 1 and len(patterns[pid]) >= 2)
    return score, patterns, placements, repeated_entities


def motif_table(rows, entity, flat, ordered):
    xs = [r["position"]["x"] for r in rows]
    ys = [r["position"]["y"] for r in rows]
    scale = None
    for candidate in (1, 2, 256):
        if all(math.isfinite(v) and abs(v * candidate) < 2**53
               and v * candidate == int(v * candidate) for v in xs + ys):
            scale = candidate
            break
    if scale is None or len(rows) < 16:
        return flat, None
    palette = flat[1][0]
    indices = unsequence(flat[1][1])
    desc = [(tid, int(x * scale), int(y * scale), i)
            for i, (tid, x, y) in enumerate(zip(indices, xs, ys))]
    dimensions = [(v, v) for v in (3, 4, 6, 8, 9, 12, 16, 24, 32)]
    dimensions += [(4, 8), (8, 4), (8, 16), (16, 8), (8, 32), (32, 8)]
    dimensions += [(0, v) for v in (1, 2, 3, 4, 6, 8, 9, 12, 16, 24, 32)]
    dimensions += [(v, 0) for v in (1, 2, 3, 4, 6, 8, 9, 12, 16, 24, 32)]
    shortlisted = []
    for width, height in dimensions:
        score, patterns, placements, repeated_entities = spatial_cells(desc, width * scale, height * scale)
        if repeated_entities and score > 0:
            shortlisted.append((score, width, height, patterns, placements, repeated_entities))
            shortlisted.sort(key=lambda v: (-v[0], v[1], v[2]))
            del shortlisted[3:]
    candidates = [(flat, None), (ordered, None)]
    # Original ID and numeric-type columns do not depend on the spatial split.
    ids = sequence([r["entity_number"] for r in rows]) if entity else None
    tx, ty = sequence([numeric_type(x) for x in xs]), sequence([numeric_type(y) for y in ys])
    for score, width, height, patterns, placements, repeated_entities in shortlisted:
        encoded_patterns = [[sequence([v[0] for v in p]), sequence([v[1] for v in p]),
                             sequence([v[2] for v in p])] for p in patterns]
        payload = [2, palette, encoded_patterns,
                   sequence([p[0] for p in placements]), sequence([p[1] for p in placements]),
                   sequence([p[2] for p in placements]), sequence([i for p in placements for i in p[3]]),
                   ids, tx, ty, scale]
        stats = {"width": width, "height": height, "patterns": len(patterns),
                 "instances": len(placements), "repeated_entities": repeated_entities,
                 "dictionary_entities": sum(map(len, patterns)), "rows": len(rows)}
        candidates.append((payload, stats))
    return min(candidates, key=lambda c: len(zlib.compress(pack(c[0]), 9)))


def fixed_motif_table(rows, entity, flat, width, height):
    """Build cells even without local repeats: another book page may reuse them."""
    xs = [r["position"]["x"] for r in rows]
    ys = [r["position"]["y"] for r in rows]
    scale = None
    for candidate in (1, 2, 256):
        if all(math.isfinite(v) and abs(v * candidate) < 2**53
               and v * candidate == int(v * candidate) for v in xs + ys):
            scale = candidate
            break
    if scale is None or len(rows) < 16:
        return flat
    indices = unsequence(flat[1][1])
    desc = [(tid, int(x * scale), int(y * scale), i)
            for i, (tid, x, y) in enumerate(zip(indices, xs, ys))]
    _, patterns, placements, _ = spatial_cells(desc, width * scale, height * scale)
    encoded = [[sequence([v[0] for v in p]), sequence([v[1] for v in p]),
                sequence([v[2] for v in p])] for p in patterns]
    return [2, flat[1][0], encoded, sequence([p[0] for p in placements]),
            sequence([p[1] for p in placements]), sequence([p[2] for p in placements]),
            sequence([i for p in placements for i in p[3]]),
            sequence([r["entity_number"] for r in rows]) if entity else None,
            sequence([numeric_type(x) for x in xs]), sequence([numeric_type(y) for y in ys]), scale]


def shared_dictionary(skeleton, tables, wires):
    """Share settings and exact translated blocks across every page of a book."""
    palette, palette_map, patterns, pattern_map = [], {}, [], {}
    encoded_tables = []
    occurrences = Counter()
    owners = defaultdict(set)
    for path, original in tables:
        payload = copy.deepcopy(original)
        local = payload[1][0] if payload[0] in (0, 1) else payload[1]
        remap = []
        for template in local:
            key = template_key(template)
            if key not in palette_map:
                palette_map[key] = len(palette)
                palette.append(template)
            remap.append(palette_map[key])
        if payload[0] in (0, 1):
            payload[1][0] = None
            payload[1][1] = sequence([remap[i] for i in unsequence(payload[1][1])])
        else:
            payload[1] = None
            pids = []
            for pattern in payload[2]:
                pattern[0] = sequence([remap[i] for i in unsequence(pattern[0])])
                key = pack(pattern)
                if key not in pattern_map:
                    pattern_map[key] = len(patterns)
                    patterns.append(pattern)
                pids.append(pattern_map[key])
            for pid in unsequence(payload[3]):
                occurrences[pids[pid]] += 1
                owners[pids[pid]].add(tuple(path))
            payload[2] = pids
        encoded_tables.append([path, payload])
    info = {"patterns": len(patterns), "instances": sum(occurrences.values()),
            "cross_table_patterns": sum(len(v) > 1 for v in owners.values()),
            "repeated_patterns": sum(c > 1 and len(unsequence(patterns[p][0])) >= 2
                                     for p, c in occurrences.items()),
            "repeated_entities": sum(c * len(unsequence(patterns[p][0])) for p, c in occurrences.items()
                                     if c > 1 and len(unsequence(patterns[p][0])) >= 2)}
    return [skeleton, encoded_tables, wires, palette, patterns], info


def restore_table(payload):
    mode = payload[0]
    if mode == 0:
        return unnormalize_rows(untable(payload[1]))
    if mode == 1:
        sorted_rows, order = untable(payload[1]), unsequence(payload[2])
        rows = [None] * len(order)
        for row, original_index in zip(sorted_rows, order):
            rows[original_index] = row
        return unnormalize_rows(rows)
    if mode != 2:
        raise ValueError("unknown block-table mode")
    _, palette, patterns, pids, axs, ays, order, ids, tx, ty, scale = payload
    patterns = [list(zip(*(unsequence(c) for c in pattern))) for pattern in patterns]
    order = unsequence(order)
    rows = [None] * len(order)
    ids = unsequence(ids) if ids is not None else None
    tx, ty = unsequence(tx), unsequence(ty)
    k = 0
    for pid, ax, ay in zip(unsequence(pids), unsequence(axs), unsequence(ays)):
        for tid, dx, dy in patterns[pid]:
            i = order[k]
            k += 1
            row = copy.deepcopy(palette[tid])
            row["position"] = {"x": restore_number(ax + dx, scale, tx[i]),
                               "y": restore_number(ay + dy, scale, ty[i])}
            if ids is not None:
                row["entity_number"] = ids[i]
            rows[i] = row
    if k != len(order) or any(row is None for row in rows):
        raise ValueError("invalid block order")
    return unnormalize_rows(rows)


def wires_table(wires, rows):
    if not isinstance(wires, list) or not wires or not rows:
        return None
    idmap = {r["entity_number"]: i for i, r in enumerate(rows)}
    if any(not isinstance(w, list) or len(w) != 4 or any(type(v) is not int for v in w)
           or w[0] not in idmap or w[2] not in idmap for w in wires):
        return None
    return [sequence([idmap[w[0]] for w in wires]), sequence([w[1] for w in wires]),
            sequence([idmap[w[2]] - idmap[w[0]] for w in wires]), sequence([w[3] for w in wires])]


def representations(value, with_stats=False):
    skeleton = copy.deepcopy(value)
    tables = {"g": [], "o": [], "a": [], "r": []}
    wires, stats, entries = [], [], []

    def walk(node, path):
        if not isinstance(node, dict):
            return
        bp = node.get("blueprint")
        if isinstance(bp, dict):
            for field in ("entities", "tiles"):
                rows = bp.get(field)
                if not isinstance(rows, list):
                    continue
                entity = field == "entities"
                supported = table(rows, entity)
                if supported is None:
                    continue
                normalized = normalize_rows(rows, entity)
                flat = [0, table(normalized, entity, template_key)]
                ordered = reordered(normalized, entity)
                adaptive = min((flat, ordered), key=lambda v: len(zlib.compress(pack(v), 9)))
                motifs, detail = motif_table(normalized, entity, flat, ordered)
                entries.append((path + ["blueprint", field], normalized, entity, flat))
                for mode, payload in (("g", flat), ("o", ordered), ("a", adaptive), ("r", motifs)):
                    tables[mode].append([path + ["blueprint", field], payload])
                if detail:
                    stats.append(dict(detail, path=path + ["blueprint", field]))
                if entity:
                    encoded = wires_table(bp.get("wires"), rows)
                    if encoded is not None:
                        wires.append([path + ["blueprint"], encoded])
                        bp["wires"] = None
                bp[field] = None
        book = node.get("blueprint_book")
        if isinstance(book, dict) and isinstance(book.get("blueprints"), list):
            for i, child in enumerate(book["blueprints"]):
                walk(child, path + ["blueprint_book", "blueprints", i])

    walk(skeleton, [])
    output = {mode: [skeleton, payload, wires] for mode, payload in tables.items()}
    # Palette-only control distinguishes shared settings from shared assemblies.
    output["p"], _ = shared_dictionary(skeleton, tables["a"], wires)
    output["t"], shared = shared_dictionary(skeleton, tables["r"], wires)
    if shared["repeated_patterns"]:
        stats.append(dict(shared, representation="t", kind="shared_dictionary"))
    if len(entries) > 1:
        choices = []
        for width, height in ((4, 4), (8, 8), (16, 16), (32, 32), (0, 4), (0, 8), (4, 0), (8, 0)):
            fixed = [[path, fixed_motif_table(rows, entity, flat, width, height)]
                     for path, rows, entity, flat in entries]
            payload, detail = shared_dictionary(skeleton, fixed, wires)
            choices.append((payload, dict(detail, width=width, height=height)))
        payload, detail = min(choices, key=lambda c: len(zlib.compress(pack(c[0]), 9)))
        output["u"] = payload
        if detail["repeated_patterns"]:
            stats.append(dict(detail, representation="u", kind="shared_dictionary"))
    else:
        output["u"] = output["t"]
    return (output, stats) if with_stats else output


def restore_blocks(value):
    skeleton, tables, wires = value[:3]
    global_palette, global_patterns = value[3:] if len(value) == 5 else (None, None)
    for path, payload in tables:
        if global_palette is not None:
            payload = copy.deepcopy(payload)
            if payload[0] in (0, 1):
                payload[1][0] = global_palette
            else:
                payload[1] = global_palette
                payload[2] = [global_patterns[i] for i in payload[2]]
        node = skeleton
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = restore_table(payload)
    for path, encoded in wires:
        bp = skeleton
        for key in path:
            bp = bp[key]
        ids = [r["entity_number"] for r in bp["entities"]]
        bp["wires"] = [[ids[a], b, ids[a + delta], d]
                       for a, b, delta, d in zip(*(unsequence(column) for column in encoded))]
    return skeleton
