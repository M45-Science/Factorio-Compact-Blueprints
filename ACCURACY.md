# Accuracy checks

The Python encoder was checked against **67 public-blueprint examples**:
13 complete designs and 54 individual pages from blueprint books.

- All **8,375 encoding candidates** restored the same parsed JSON, including
  numeric types and precision.
- Every saved size and source-file hash matched a fresh calculation.
- All **67 winning strings** produced the same import status and byte-identical
  exports as their originals in Factorio **2.1.24**.
- **28 unit tests** passed, including Lua 5.2 interoperability, fixed wire
  examples, large integers, and older module-list ordering.

The 13 complete designs use **2,614,053 → 507,915 characters** overall.
See the linked designs on the [benchmarks page](BENCHMARKS.md).

The Lua codec also passed all **67 examples** inside Factorio: **1,675**
Python-to-Lua decoding checks, 67 Lua-to-Python checks, and matching game exports
for both Lua-generated strings and Python portable strings. An additional
legacy-module example checked slot ordering through every representation.

Evidence: [size audit](audit-results.json), [Python game audit](factorio-audit-results.json),
[Lua game audit](lua-audit-results.json), [module-order check](module-order-audit-results.json).

## Game results

The isolated game test used base, elevated rails, quality, recycler, and Space
Age, all version 2.1.24. It changed no existing saves or server configuration.

| Result | Examples |
| --- | ---: |
| Matching import status and exports | 67 |
| Imported without errors | 61 |
| Original and restored both imported with errors | 6 |
| Mismatches or rejected imports | 0 |

The six error statuses were already present in the public originals. Matching
exports show that compression preserved how this game version imported them;
it does not establish that every community design works correctly. A deliberate
entity change was detected by the comparison.

These checks cover stored data and game imports, not factory throughput or all
possible mods. JSON whitespace is not retained. Legacy module-map entry order
is preserved because Factorio can use it when migrating older blueprints.

## Reproduce

```sh
pip install -r requirements.txt
python3 -m unittest discover -v
python3 fetch_site_corpus.py
python3 benchmark_optimized.py --lua-cases /tmp/lua-cases.json
python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json
python3 test_factorio.py /path/to/factorio /tmp/blueprint-import-pairs.json
python3 test_factorio_lua.py /path/to/factorio /tmp/lua-cases.json
```

Lua tests need Lua 5.2 or the Docker image `nickblah/lua:5.2-alpine`.
The optional game tests need a local Factorio installation with expansion data.
They create and remove their own temporary scenarios and configuration.
Use trusted input; this experimental decoder is not hardened against hostile
compressed files.
