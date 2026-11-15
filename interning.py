"""Share repeated strings and nested settings across a structural payload.

Extension 1 remains the existing relative-entity reference. Extension 2 is a
zero-based dictionary reference containing a canonical unsigned LEB128 integer.
Dictionary records refer only to earlier records; object identity is not shared
in the restored JSON tree.
"""
from collections import Counter
import copy

import msgpack

from compact import pack, read_varints, varint


def intern(value, strings_only=False):
    counts = Counter()
    keys = {}

    def scan(node):
        compound = isinstance(node, (list, dict))
        eligible = (isinstance(node, str) and len(node.encode()) >= 4) or (compound and not strings_only)
        if eligible:
            key = pack(node)  # Map entry order can affect legacy module slots.
            keys[id(node)] = key
            if len(key) >= (5 if isinstance(node, str) else 8):
                counts[key] += 1
        if isinstance(node, dict):
            for k, v in node.items():
                scan(k)
                scan(v)
        elif isinstance(node, list):
            for v in node:
                scan(v)

    scan(value)
    selected = {key for key, count in counts.items() if (count - 1) * len(key) > count * 4 + 2}
    records, index = [], {}

    def emit(node):
        key = keys.get(id(node))
        if key in selected and key in index:
            return msgpack.ExtType(2, varint(index[key]))
        if isinstance(node, dict):
            out = {emit(k): emit(v) for k, v in node.items()}
        elif isinstance(node, list):
            out = [emit(v) for v in node]
        else:
            out = node
        if key in selected:
            index[key] = len(records)
            records.append(out)
            return msgpack.ExtType(2, varint(index[key]))
        return out

    root = emit(value)
    return [records, root]


def expand(payload):
    records, root = payload
    resolved = []

    def visit(node):
        if isinstance(node, msgpack.ExtType) and node.code == 2:
            index = list(read_varints(node.data))
            if len(index) != 1 or index[0] >= len(resolved):
                raise ValueError("invalid or forward dictionary reference")
            return copy.deepcopy(resolved[index[0]])
        if isinstance(node, dict):
            return {visit(k): visit(v) for k, v in node.items()}
        if isinstance(node, list):
            return [visit(v) for v in node]
        return node

    for record in records:
        resolved.append(visit(record))
    return visit(root)


def restore_payload(form, payload):
    from compact import restore
    from subassemblies import restore_blocks
    if form == "s":
        return restore(payload)
    if form in ("g", "o", "a", "r", "p", "t", "u"):
        return restore_blocks(payload)
    raise ValueError("unsupported dictionary base representation")
