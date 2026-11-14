"""Experimental lossless Factorio JSON transport. Not a frozen wire specification."""
import argparse
import base64
import copy
import itertools
import json
import lzma
import math
import zlib

import brotli
import msgpack
import zstandard


def json_bytes(value):
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode()


def pack(value):
    return msgpack.packb(value, use_bin_type=True)


def unpack(data):
    return msgpack.unpackb(data, raw=False, strict_map_key=False)


def varint(n):
    out = bytearray()
    while n >= 128:
        out.append((n & 127) | 128)
        n >>= 7
    out.append(n)
    return bytes(out)


def read_varints(data):
    n = shift = 0
    for b in data:
        n |= (b & 127) << shift
        if b & 128:
            shift += 7
        else:
            yield n
            n = shift = 0
    if shift:
        raise ValueError("truncated varint")


def zigzag(n):
    return 2 * n if n >= 0 else -2 * n - 1


def unzigzag(n):
    return n // 2 if n % 2 == 0 else -(n // 2) - 1


def sequence(values):
    """Q3-inspired adaptive modes, plus varint deltas and delta runs."""
    choices = [[0, values]]
    n = len(values)
    if not n:
        return choices[0]
    step = values[1] - values[0] if n > 1 else 0
    if all(v == values[0] + i * step for i, v in enumerate(values)):
        choices.append([1, n, values[0], step])
    deltas = [values[i] - values[i - 1] for i in range(1, n)]
    choices.append([2, values[0], b"".join(varint(zigzag(d)) for d in deltas)])
    runs = [(d, sum(1 for _ in g)) for d, g in itertools.groupby(deltas)]
    choices.append([3, values[0], b"".join(varint(zigzag(d)) + varint(c) for d, c in runs)])
    low, high = min(values), max(values)
    width = (high - low).bit_length()
    bits = bytearray()
    acc = count = 0
    for v in values:
        acc = (acc << width) | (v - low)
        count += width
        while count >= 8:
            count -= 8
            bits.append((acc >> count) & 255)
        acc &= (1 << count) - 1
    if count:
        bits.append(acc << (8 - count))
    choices.append([4, n, low, width, bytes(bits)])
    return min(choices, key=lambda v: len(pack(v)))


def unsequence(value):
    mode, *args = value
    if mode == 0:
        return args[0]
    if mode == 1:
        n, start, step = args
        return [start + i * step for i in range(n)]
    if mode in (2, 3):
        start, data = args
        result = [start]
        nums = iter(read_varints(data))
        if mode == 2:
            for d in nums:
                result.append(result[-1] + unzigzag(d))
        else:
            for d in nums:
                count = next(nums)
                d = unzigzag(d)
                start = result[-1]
                result.extend(start + (i + 1) * d for i in range(count))
        return result
    if mode == 4:
        n, low, width, data = args
        if width == 0:
            return [low] * n
        acc = count = 0
        result = []
        mask = (1 << width) - 1
        for b in data:
            acc = (acc << 8) | b
            count += 8
            while count >= width and len(result) < n:
                count -= width
                result.append(low + ((acc >> count) & mask))
            acc &= (1 << count) - 1
        return result
    raise ValueError("unknown sequence mode")


def coordinates(values):
    choices = [[0, values]]
    for scale in (1, 2, 256):
        if all(type(v) in (int, float) and math.isfinite(v)
               and abs(v * scale) < 2**53 and v * scale == int(v * scale)
               for v in values):
            # Preserve int versus float, including signed zero, in the JSON tree.
            types = bytes((type(v) is float) | (2 if isinstance(v, float) and
                          v == 0 and math.copysign(1, v) < 0 else 0) for v in values)
            choices.append([1, scale, sequence([int(v * scale) for v in values]),
                            sequence(list(types))])
    return min(choices, key=lambda v: len(pack(v)))


def uncoordinates(value):
    if value[0] == 0:
        return value[1]
    _, scale, encoded, types = value
    result = []
    for n, typ in zip(unsequence(encoded), unsequence(types)):
        v = n / scale if typ & 1 else n // scale
        result.append(-0.0 if typ & 2 else v)
    return result


def table(rows, entity, template_key=None):
    if not rows:
        return None
    reserved = {"position", "entity_number"} if entity else {"position"}
    if any(not isinstance(r, dict) or not isinstance(r.get("position"), dict)
           or set(r["position"]) != {"x", "y"}
           or any(type(r["position"][a]) not in (int, float) for a in ("x", "y"))
           or (entity and type(r.get("entity_number")) is not int) for r in rows):
        return None
    palette, lookup, indices = [], {}, []
    for r in rows:
        template = {k: v for k, v in r.items() if k not in reserved}
        key = (template_key(template) if template_key else
               json.dumps(template, sort_keys=True, separators=(",", ":")))
        if key not in lookup:
            lookup[key] = len(palette)
            palette.append(template)
        indices.append(lookup[key])
    return [palette, sequence(indices),
            coordinates([r["position"]["x"] for r in rows]),
            coordinates([r["position"]["y"] for r in rows]),
            sequence([r["entity_number"] for r in rows]) if entity else None]


def untable(value):
    palette, indices, xs, ys, ids = value
    indices, xs, ys = unsequence(indices), uncoordinates(xs), uncoordinates(ys)
    numbers = unsequence(ids) if ids is not None else [None] * len(indices)
    if len({len(indices), len(xs), len(ys), len(numbers)}) != 1:
        raise ValueError("column length mismatch")
    result = []
    for i, x, y, number in zip(indices, xs, ys, numbers):
        row = copy.deepcopy(palette[i])
        row["position"] = {"x": x, "y": y}
        if number is not None:
            row["entity_number"] = number
        result.append(row)
    return result


def transform(value):
    skeleton = copy.deepcopy(value)
    tables = []

    def walk(node, path):
        if not isinstance(node, dict):
            return
        bp = node.get("blueprint")
        if isinstance(bp, dict):
            for field in ("entities", "tiles"):
                if isinstance(bp.get(field), list):
                    encoded = table(bp[field], field == "entities")
                    if encoded is not None:
                        tables.append([path + ["blueprint", field], encoded])
                        bp[field] = None
        book = node.get("blueprint_book")
        if isinstance(book, dict) and isinstance(book.get("blueprints"), list):
            for i, child in enumerate(book["blueprints"]):
                walk(child, path + ["blueprint_book", "blueprints", i])

    walk(skeleton, [])
    return [skeleton, tables]


def restore(value):
    skeleton, tables = value
    for path, encoded in tables:
        node = skeleton
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = untable(encoded)
    return skeleton


COMPRESS = {
    "n": lambda b: b,
    "d": lambda b: zlib.compress(b, 9),
    "b": lambda b: brotli.compress(b, quality=11),
    "z": lambda b: zstandard.ZstdCompressor(level=19).compress(b),
    "l": lambda b: lzma.compress(b, preset=9),
}
DECOMPRESS = {
    "n": lambda b: b,
    "d": zlib.decompress,
    "b": brotli.decompress,
    "z": lambda b: zstandard.ZstdDecompressor().decompress(b),
    "l": lzma.decompress,
}


def printable(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def candidates(value, repeated=True):
    # Raw JSON fallback handles all JSON values and bounds incompressible overhead.
    forms = {"j": json_bytes(value)}
    try:
        forms["s"] = pack(transform(value))
    except (OverflowError, ValueError):
        pass
    if repeated:
        from subassemblies import representations
        try:
            forms.update({mode: pack(v) for mode, v in representations(value).items()})
        except (OverflowError, ValueError):
            pass
    return {f"{form}/{codec}": "BX0:" + form + codec + printable(compress(data))
            for form, data in forms.items() for codec, compress in COMPRESS.items()}


def encode(value):
    return min(candidates(value).values(), key=len)


def decode(text):
    if not text.startswith("BX0:"):
        raise ValueError("expected experimental BX0 prefix")
    form, codec, body = text[4], text[5], text[6:]
    data = DECOMPRESS[codec](base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    if form == "j":
        return json.loads(data)
    if form == "s":
        return restore(unpack(data))
    if form in ("g", "o", "a", "r", "p", "t", "u"):
        from subassemblies import restore_blocks
        return restore_blocks(unpack(data))
    raise ValueError("unknown representation")


def native_decode(text):
    text = text.strip()
    return json.loads(zlib.decompress(base64.b64decode(text[1:]))) if text.startswith("0") else json.loads(text)


def native_encode(value):
    return "0" + base64.b64encode(zlib.compress(json_bytes(value), 9)).decode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["encode", "decode"])
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    with open(args.input) as f:
        text = f.read()
    out = encode(native_decode(text)) if args.action == "encode" else native_encode(decode(text.strip()))
    with open(args.output, "w") as f:
        f.write(out + "\n")


if __name__ == "__main__":
    main()
