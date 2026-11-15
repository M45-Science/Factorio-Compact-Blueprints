# Factorio Compact Blueprints

An experimental lossless transport for Factorio blueprints and blueprint books.
It separates entity settings from placement, packs integer sequences, and shares
repeated blocks within blueprints and across book pages. The encoder chooses the
shortest result from several representations and compressors.

`BX0:` strings require conversion back to Factorio's native format before import.
The format is experimental and may change.

## Performance

On **13 complete public blueprint downloads**, the encoder reduced the combined
size from **2,614,053 to 527,338 characters: 4.96× smaller, or about 80% less text**.
That is another **8.95%** beyond the first structural prototype.

The full benchmark covers **67 fixtures from 16 public blueprint posts**. This
is a curated sample, so the combined result is not a prediction for every design.

[Benchmarks: designs, public links, detailed results, and methodology](BENCHMARKS.md)

## Accuracy

The public-blueprint benchmark passed **3,015 exact parsed-JSON round trips**.
All **67 original/reconstructed import pairs** produced identical native exports
in Factorio 2.1.24. Six pairs had the same pre-existing import-error status in
both versions. The unit suite has **13 tests**.

Entity IDs, array order, positions, numeric types, wire references, settings,
metadata, nested books, and unfamiliar mod fields are retained. JSON whitespace
and object key ordering are not retained. No external dictionary or installed
mod catalog is needed to decode a transport string.

[Accuracy audit and game-import evidence](ACCURACY.md)

## Usage

Python 3.10+ is required.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -v
python3 compact.py encode native-blueprint.txt compressed.txt
python3 compact.py decode compressed.txt restored.txt
```

`encode` accepts a native blueprint string or blueprint JSON. `decode` writes a
native Factorio string. The bundled `example-native.txt` and
`example-compact.txt` are a synthetic belt-grid demonstration, outside the
public-blueprint benchmark.

## Encoding

Shared palettes store distinct entity settings once. Independent columns encode
entity IDs, coordinates, and palette indices with regular sequences, deltas,
runs, or bit packing. Optional modes use relative wire references, spatial
ordering, and exact translated-block dictionaries.

The transport starts with `BX0:`, then a representation character, a compressor
character, and unpadded Base64URL bytes. Compressor candidates are uncompressed,
zlib, Brotli, Zstandard, and LZMA. The original JSON encoding remains a fallback.
[Representation details](BLOCK_RESULTS.md#implementation)

The decoder is a research tool for trusted inputs and has not been hardened
against hostile compressed data. Searching all encoding candidates costs more
CPU than a native export.

## Reproducing the benchmarks

```sh
python3 fetch_site_corpus.py
python3 benchmark_sites.py
python3 benchmark_blocks.py
python3 report_benchmarks.py
python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json
```

The fetch script downloads public designs from pinned source records. Community
payloads are kept out of this repository; public links, source hashes, and all
measurements are included. The [Benchmarks page](BENCHMARKS.md#reproduce) explains
cache handling, sampling, and optional game-import verification.

## License

The source code is [MIT-licensed](LICENSE). Downloaded community designs retain
their authors' rights; the [source manifest](site-corpus/sources.json) links to
their public pages and pinned source records.
