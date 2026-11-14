# Accuracy audit

Audited November 14, 2026, before the initial public publication.

The saved measurements reproduced exactly and the game-import comparison found
no differences between originals and reconstructed blueprints. No codec fixes
were needed during this audit.

## Recomputed measurements

- All **3,015 candidates across the 67 popular-site fixtures** reconstructed
  identical parsed JSON. Every saved per-mode length and winning size matched.
- All **140 candidates across the original 14 fixtures** also reconstructed
  identical parsed JSON and matched their saved lengths.
- Downloaded fixture hashes, the codec implementation fingerprint, and the
  published site/block summary calculations matched their recorded values.
- A fresh Python 3.12 virtual environment installed the pinned dependencies and
  passed **13 unit tests**, including 150 additional mixed-precision layouts
  checked through seven structural representations. It also reproduced the
  1,280-character example byte-for-byte.

The unchanged complete-download totals remain **2,614,053 native characters →
527,338 characters**, or **4.96× smaller**. Relative to the preceding structural
prototype, that is an **8.95%** additional reduction. Explicit block modes add
**0.55%** beyond the graph, ordering, and shared-settings controls. These are
curated-sample results, not a guarantee for arbitrary blueprints.

Machine-readable evidence: [site audit](audit-results.json),
[original-fixture audit](initial-audit-results.json),
[game audit](factorio-audit-results.json).

## Factorio import comparison

Factorio **2.1.24, build 87808, Linux headless** ran an isolated `--test-scenario`
with base, elevated rails, quality, recycler, and Space Age, all version 2.1.24.
No existing saves, server, mods directory, or user configuration were changed.

For each of the 67 popular-site fixtures, the test imported both the original
native blueprint JSON and the winning transport's reconstructed native string
into separate inventory slots. It compared import return codes and required
**byte-identical native exports from the game**.

| Result | Pairs |
| --- | ---: |
| Imported and re-exported identically | **67** |
| Imported without errors (`0`) | 61 |
| Imported with errors (`-1`), identical for both versions | 6 |
| Rejected by the importer (`1`) or threw an exception | 0 |
| Different import status or exported string | **0** |

The six import-error statuses were already present in the corresponding
originals. Their exact causes were not classified. Equal game exports show
that the transport introduced no difference in how this game version imported
them; they do not establish that those community designs are error-free.
The status meanings are documented in
[LuaItemStack.import_stack](https://lua-api.factorio.com/latest/classes/LuaItemStack.html#import_stack).

A negative control that deliberately changed a belt to an inserter was rejected
by the comparison as a re-export mismatch.

This verifies import equivalence, not factory throughput, successful placement
on every surface, or behavior under every possible mod combination. The Python
JSON checks preserve fields even if the game ignores or migrates them. JSON
whitespace and object key ordering are intentionally not retained.

## Reproduce

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -v
python3 fetch_corpus.py
python3 benchmark.py
python3 fetch_site_corpus.py
python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json
python3 test_factorio.py /path/to/factorio/bin/x64/factorio /tmp/blueprint-import-pairs.json
```

The optional engine check requires a compatible local Factorio installation
with the expansion data. The test creates and removes its own temporary
scenario, config, and mod-list files. Community payloads are fetched locally;
they are not included in this repository.

The `BX0:` format and decoder remain experimental trusted-input research tools.
They have not been hardened against hostile compressed inputs, and searching
all encoding modes costs more CPU than native export.
