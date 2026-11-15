# Developer wire reference

`BX0:` is an experimental format. Existing representations remain readable.
User-facing usage is in the [README](README.md) and [Lua guide](LUA.md).

## Framing

An ASCII string is `BX0:` + representation + compressor + unpadded Base64URL.
The Base64URL alphabet is `A–Z a–z 0–9 - _`. The body decodes to the compressor's
bytes. A decoder restores the uncompressed payload before interpreting it.

| Compressor | Bytes |
| --- | --- |
| `n` | Uncompressed |
| `d` | zlib-wrapped DEFLATE |
| `b` | Brotli |
| `z` | Zstandard frame |
| `l` | XZ container with LZMA |

The native Factorio transport uses `0` + padded standard Base64 of zlib JSON.
Native strings must be converted before use as a `BX0:` body.

Representation `j` contains UTF-8 JSON. All others contain MessagePack with
string keys, typed arrays/maps, integers, binary blobs, and float64 values.
Float32 decoding is also supported. Nulls must survive in arrays and objects.

## Extensions

| MessagePack extension | Payload | Meaning |
| --- | --- | --- |
| 1 | Unsigned LEB128 of zigzag offset | Relative entity-row reference |
| 2 | Unsigned LEB128 index | Shared-value dictionary reference |
| 3 | ASCII JSON number | Literal number outside a runtime's exact integer range |

Extension 3 contains a number only, with no whitespace or nonfinite values.
It allows Lua to carry arbitrary JSON integers without double rounding.
Ordinary signed/unsigned 64-bit MessagePack integers remain preferred when
the number fits. A float must remain a float, including negative zero.

## Integer columns

Columns are arrays whose first entry selects a mode. IDs and indices on the
wire are zero-based. Zigzag maps `n >= 0` to `2*n`, otherwise to `-2*n-1`.
Unsigned LEB128 writes seven low bits per byte, low group first, with bit 7 set
when another group follows.

| Mode | Remaining entries | Reconstruction |
| --- | --- | --- |
| 0 | values | Literal integer array |
| 1 | count, start, step | `start + i*step` for `i = 0..count-1` |
| 2 | start, binary deltas | Start, then signed zigzag/LEB128 deltas |
| 3 | start, binary runs | Start, then pairs of zigzag delta and repetition count |
| 4 | count, minimum, width, binary bits | Minimum plus each fixed-width unsigned value |

Mode 4 writes high bits first and pads the last byte with zero low bits.
Integer arithmetic must remain exact, even for int64/uint64 ID columns.

Coordinates use `[0, literal_numbers]` or `[1, scale, integer_column, types]`.
Scales are 1, 2, or 256. Type code 0 means integer, 1 means float, and 3 means
negative floating-point zero. Dividing the scaled integer restores the value.

## Flat tables and paths

A flat table is `[palette, indices, X, Y, IDs_or_null]`. Each row copies a
palette object, restores `position.x/y`, and restores `entity_number` when IDs
are present. Palette objects contain the remaining fields.

A path is an array of object keys and zero-based array positions.
Representation `s` is `[skeleton, tables]`; each table entry is `[path, flat]`.
Replace the skeleton's placeholder at each path with its decoded row array.

## Graph, ordering, and block representations

Representations `g`, `o`, `a`, and `r` use `[skeleton, tables, wires]`.
Representations `p`, `t`, and `u` use the same fields followed by a shared
palette and shared block dictionary. The letters describe encoder strategies;
decoding is selected by each table's own mode.

A table entry is `[path, payload]`:

| Payload mode | Remaining fields |
| --- | --- |
| 0 | flat table |
| 1 | spatially ordered flat table, original-index column |
| 2 | palette, blocks, block-ID column, anchor-X column, anchor-Y column, original-index column, original-ID column or null, X-type column, Y-type column, scale |

A block is `[template-index column, relative-X column, relative-Y column]`.
Each instance adds its anchor to the block coordinates. Its expanded rows are
placed at the original indices, restoring row order and IDs exactly.

With a shared palette, each local palette field is null. With a shared block
dictionary, each local blocks array contains dictionary indices rather than
literal blocks. Copy row templates before restoring fields and references.

Extension 1 inside legacy `connections` and `neighbours` resolves against the
original row array: `original_ID[current_row + signed_offset]`. A wire entry is
`[blueprint_path, [source_rows, source_connectors, target_deltas, target_connectors]]`.
Each field is an integer column; target row is source row plus target delta.
Restore original IDs before rebuilding the wire list. Preserve wire order.

## Shared-value representation `i`

Its MessagePack payload is `[base_representation, [dictionary, root]]`.
Supported bases are `s`, `g`, `o`, `a`, `r`, `p`, `t`, and `u`.

Read dictionary records in order. Extension 2 refers to a **strictly earlier**
record when used inside a record, or to any record when used in the root.
Resolve references recursively in values and map keys. Copy referenced arrays
and objects: reconstructed JSON values must not alias mutable row templates.
Then decode the expanded root using the base representation's normal rules.

Records can be strings, arrays, or maps. Encoder dictionary selection and record
order are optimization choices, not decoding requirements. Forward, cyclic,
truncated, or out-of-range references are invalid. The Lua encoder currently
shares strings; both implementations decode compound records as well.

## Compatibility

Python reads every compressor. The dependency-free Lua module reads all
representations with no compression; Factorio supplies zlib support. Other
compressors require caller-provided callbacks. Use Python's `--portable` mode
for strings intended for Factorio's Lua runtime.

The decoder is currently for trusted input. This specification does not claim
hostile-input resource bounds for decompression or recursive expansion.

Fixed strings and their expected JSON values are in
[`test-vectors.json`](test-vectors.json). Both implementations read these in the local test suite.
Preserve legacy `items` map entry order when converting back to JSON: Factorio
can use it to choose module slots while migrating older blueprints. Both
codecs retain this order; its optional `pack(value, true)` flag is for canonical
comparison in tests, not normal wire serialization.
