# Factorio Compact Blueprints

The Quickbar Exchange V3 approach works for blueprints: encode their structure,
then compress the result. This is a working Python experiment, not a finalized
exchange standard or an in-game importer.

The current encoder reduced 13 complete public blueprint downloads from
2,614,053 native characters to **527,338 characters (4.96× smaller)**. That is
another **8.95%** beyond the first structural prototype. Explicit block modes
add 0.55% beyond the new wire, ordering, and shared-settings controls; most
of the incremental savings come from those controls. This is a curated sample,
not an estimate of typical savings for every blueprint.

See [the accuracy audit](ACCURACY.md), [popular-site measurements](SITE_RESULTS.md),
and [block-sharing measurements](BLOCK_RESULTS.md). The `BX0:` transport requires
conversion back to a native Factorio string before game import.

**Follow-up: popular blueprint sites.** A separate run tested 67 fixtures from
16 curated public site posts. Individual sampled pages were 2.09× smaller at
the median; complete books were 3.52× smaller at the median. See
[the site benchmark report](SITE_RESULTS.md) for source links, complete tables,
sampling limits, and comparisons with stronger JSON compression.

**Repeated subassemblies.** The encoder now also tries exact translated blocks,
book-wide block/settings dictionaries, and graph/order controls. The previous
results remain frozen; see [the block-sharing experiment](BLOCK_RESULTS.md) for
the incremental savings and the controls separating block modes from the other
improvements. `compact.py encode` automatically chooses among all modes.

## Measured results

This table records the first structural prototype (`repeated=False`), before
the subsequent graph, ordering, and repeated-block modes.

Lengths count every ASCII character copied, including prefixes. Native means
compact JSON → zlib level 9 → padded Base64, prefixed with `0`. The JSON-only
column tries stronger compressors without changing the data representation.
The experiment selects the shortest complete string across its candidates.

| Fixture | Native | Best JSON-only | Best structured | Native / best |
| --- | ---: | ---: | ---: | ---: |
| Public rail layout, 27 entities | 1,301 | 1,070 | 976 | 1.33× |
| Public rail layout, 133 entities | 3,157 | 2,020 | 1,238 | 2.55× |
| Public 4,096-tile layout | 16,893 | 7,542 | 1,656 | 10.20× |
| Public converted image, 63,315 entities | 430,105 | 98,881 | 6,070 | 70.86× |
| Public lamp image, 22,500 entities | 249,817 | 160,856 | 65,825 | 3.79× |
| Public lookup-table circuit, 8 entities | 620,225 | 318,289 | 303,508 | 2.04× |
| Synthetic 100×100 belt grid | 46,289 | 15,014 | 172 | 269.12× |
| Synthetic random positions and random tags | 42,369 | 33,233 | 28,069 | 1.51× |

These fixtures demonstrate feasibility, not an estimate of typical savings.
The public book is mostly rail designs; image blueprints and synthetic grids
have unusually strong structure. Circuit settings with substantial unique data
benefit much less from the structural transformation. No compression method can
guarantee large reductions for arbitrary input.

The structural win does not require a new compressor. With **zlib level 9**,
the converted image is 6,994 characters (61.50× smaller than native), and the
synthetic belt grid is 177 characters (261.52× smaller). Some fixtures benefit
substantially from Brotli or LZMA; codec portability matters for a Lua importer.

All 140 candidates across 14 fixtures reconstructed identical parsed JSON,
including numeric types and negative zero. JSON whitespace and object key order
are not retained. Five unit tests also cover randomized layouts, nested books,
nonconsecutive IDs, wire references, precision, modded fields, and fallbacks.
See [the accuracy audit](ACCURACY.md) for subsequent game-import validation.

## What carries over from Quickbar V3

Reference: [M45 Quickbar Exchange V3](https://github.com/M45-Science/QuickbarExchange/blob/main/V3.md).

1. **Adaptive sequence modes.** Constant/regular sequences become a count,
   starting value and step. Other choices are raw values, signed delta varints,
   delta runs, or fixed-width offset bit packing. Choose the shortest encoding.
2. **Palettes.** Identical entity settings are recorded once. Each entity carries
   a palette index instead of repeating its name, direction, quality, recipe,
   control settings, and other fields.
3. **Separate placement and content.** Entity IDs, X coordinates, Y coordinates,
   and palette indices are independent columns. Repetitive coordinate patterns
   remain visible to the compressor. Tile arrays use the same approach.
4. **Defaults cost little.** Constant sequences and ID progressions take a few
   bytes regardless of entity count. Exact coordinates can use integer scales
   of 1, 2, or 256; other values retain their original numeric representation.
5. **Compare complete printable lengths.** A raw JSON candidate remains available
   when structural encoding is unhelpful. This bounds regression relative to
   the same JSON compressed natively to at most five extra characters.

This prototype uses MessagePack for its container, byte-oriented varints, and
byte-aligned packed columns. It does **not** implement Q3's mixed-radix packer,
Rice gaps, or fixed prototype catalogs. Those are further experiments, especially
for small blueprints. Q3's item catalog must not be used directly as an entity
catalog: item and entity prototype names are different namespaces.

## Lossless behavior

Entity numbers and array order are preserved. Wire references, schedules,
parameters, metadata, quality, and unfamiliar mod fields are retained as data;
the codec does not need to understand their meanings. Entity and tile rows that
do not match the supported shape remain in their original representation.
Blueprint books retain their slot indices and nesting. No external dictionary,
network lookup, or installed mod catalog is required to decode a string.

The transport begins `BX0:` followed by a representation character (`j` for
original JSON, `s` for the original structural MessagePack, or one of the
[new graph/block representations](BLOCK_RESULTS.md)), a compressor character, then
unpadded Base64URL bytes. Compressor choices are none (`n`), zlib (`d`), Brotli
(`b`), Zstandard (`z`), and LZMA (`l`). The prefix and internal structures are
experimental and may change. Factorio requires conversion back to its native
string before import.

## Run

Python 3.10+ and the packages in `requirements.txt` are required.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -v
python3 compact.py encode example-native.txt compressed.txt
python3 compact.py decode compressed.txt restored.txt
```

To reproduce measurements, fetch the public fixtures locally and run:

```sh
python3 fetch_corpus.py
python3 benchmark.py
python3 fetch_site_corpus.py
python3 benchmark_sites.py
python3 benchmark_blocks.py
python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json
```

Community blueprint payloads and examples derived from them are excluded from
the repository. Their source links, pinned commits, hashes, and measured sizes
are included; the fetch scripts retrieve the payloads on demand. The bundled
`example-native.txt` and `example-compact.txt` are a synthetic belt grid.

The source code is MIT-licensed. Downloaded community designs retain their
authors' rights; the source manifests link to their public pages. The upstream
Draftsman license notice is retained in `corpus/UPSTREAM-LICENSE`.

`results.json` records every measured candidate and encoding/verification time.
The benchmarks use eight leaves sampled at evenly spaced entity-count ranks
from a 568-blueprint public book, plus three independent public examples and
three synthetic controls. The complete book is downloaded as a source but is
not included in the benchmark. Fixture source URLs, pinned commit, and hashes
are in `corpus/sources.json`; upstream licensing is in `corpus/UPSTREAM-LICENSE`.
`fetch_corpus.py` regenerates the downloaded public fixtures. Python library
versions are pinned for reproduction; timings depend on hardware.

## Next format experiments

Exact translated subassemblies and cross-page block sharing are now implemented
and measured in `BLOCK_RESULTS.md`. Further candidates include approximate
block matches with sparse exceptions, rotations/reflections, and reusable
internal wire graphs. The current implementation preserves original IDs and
wire data, but keeps modern blueprint-level wires outside the block dictionary.

Other useful candidates are separate settings and wire palettes, shared
dictionaries across book entries, sparse spatial occupancy/Rice modes, Q3-style
mixed-radix index packing, and a versioned built-in entity/recipe catalog with
literal extensions. Measure these against the current adaptive fallback rather
than assuming they help. Per-column choices currently minimize uncompressed
MessagePack length; jointly choosing modes after compression may do better.

A production specification needs decoder limits, integrity checking, strict
canonical/padding validation, and malformed-input tests. This decoder is a
research tool for trusted fixtures, with no resource bounds for hostile input.
An in-game implementation should select modes supported by Factorio's runtime;
this experiment does not establish Brotli/Zstandard/LZMA availability in Lua.
