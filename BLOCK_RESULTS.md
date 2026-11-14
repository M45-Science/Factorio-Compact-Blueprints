# Repeated-subassembly experiment

The codec now supports exact translated blocks within a blueprint and shared block dictionaries across book pages. The original 67-fixture popular-blueprint corpus and its ten original encoding candidates were retained as the baseline. Every new mode is optional; the encoder keeps the previous result whenever the new choices are larger.

## Results

`Extra reduction` measures the improvement over the previous prototype, not over native Factorio. `Block modes over controls` compares the final result with the best of the previous prototype and all new graph, ordering, and shared-settings controls.

| Group | Fixtures | Previous chars | Best new chars | Extra reduction | Block modes over controls |
| --- | ---: | ---: | ---: | ---: | ---: |
| Complete downloads | 13 | 579,191 | 527,338 | 8.95% | 0.55% |
| Complete books only | 9 | 542,245 | 492,832 | 9.11% | 0.59% |
| Individual sampled pages | 54 | 286,068 | 267,471 | 6.50% | 0.22% |

The block modes help some repeated production lines substantially, but add only a small aggregate gain over the other new modes. Much of the overall improvement is better ordering, relative wire references, and a shared settings palette. This experiment does not establish a limit on what other subassembly algorithms could achieve.

## Complete downloads

| Design | Previous prototype | Best new | Extra reduction | Native / new | Winning mode |
| --- | ---: | ---: | ---: | ---: | --- |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | 109,718 | 94,932 | 13.48% | 5.16× | `r/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 60,969 | 54,454 | 10.69% | 3.94× | `p/l` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | 76,070 | 70,572 | 7.23% | 6.62× | `t/l` |
| [Compact, smart 1.1 GW 2x4 nuclear plant "little witch"](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | 3,665 | 3,276 | 10.61% | 3.22× | `o/b` |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | 1,388 | 1,388 | 0.00% | 2.08× | `s/b` |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 1,290 | 1,284 | 0.47% | 2.10× | `p/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 24,108 | 20,550 | 14.76% | 3.33× | `t/l` |
| [Fulgora Mall - 4 planets tech, normal quality](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | 23,712 | 22,676 | 4.37% | 4.05× | `g/b` |
| [GSXR - Automatic MALL of ALL items.](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | 8,181 | 7,166 | 12.41% | 2.25× | `o/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | 19,369 | 17,154 | 11.44% | 3.13× | `p/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 154,521 | 144,994 | 6.17% | 4.80× | `r/b` |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 24,092 | 20,550 | 14.70% | 3.32× | `t/l` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 72,108 | 68,342 | 5.22% | 6.32× | `p/l` |

## Cumulative controls

Each stage keeps the smallest complete string available so far. These aggregates count complete downloads only. They distinguish improvements accompanying the subassembly implementation from improvements that need block modes.

| Available representations | Combined chars | Extra reduction versus previous prototype |
| --- | ---: | ---: |
| Previous prototype | 579,191 | 0.00% |
| + Relative graph references | 561,019 | 3.14% |
| + Spatial/adaptive ordering | 540,601 | 6.66% |
| + Shared settings palette | 530,251 | 8.45% |
| + Local and shared block dictionaries | 527,338 | 8.95% |

## Implementation

`subassemblies.py` matches disjoint spatial cells after translating each cell's minimum X/Y to the origin. A block is a sequence of entity-settings palette IDs and relative positions. Its instances carry block ID and translation. Explicit columns retain the original row permutation, entity numbers, coordinate numeric types, and negative zero. No entity IDs are discarded or reassigned in the decoded JSON.

Local matching tries 37 square, rectangular, and full-axis strip dimensions. A reuse estimate shortlists three; actual zlib-compressed size, including the permutation, selects among these and the flat controls per entity/tile array. A second search tries eight common cell/strip dimensions across the whole book, including cells unique within one page but repeated on another. Global dictionaries share both settings and exact blocks. Final complete-string selection tries the same five compressors used in the original benchmark.

Legacy `connections` entity IDs and `neighbours` use typed relative-row references. Modern blueprint-level wire lists are delta-coded in separate columns. Their order and endpoint IDs are retained exactly. Modern wire graphs are not yet part of the reusable block dictionary. Unknown fields and unsupported shapes retain literal values or use the prior encoding.

| Mode | Representation |
| --- | --- |
| `j`, `s` | Previous JSON and structural encodings |
| `g` | Flat columns with relative graph references |
| `o` | Spatially sorted columns plus original-order permutation |
| `a` | Per-array adaptive choice between `g` and `o` |
| `p` | Adaptive flat columns with a book-wide settings palette |
| `r` | Per-array adaptive local block dictionary |
| `t` | Book-wide sharing of the locally selected blocks/settings |
| `u` | Book-wide block search, including cross-page-only repeats |

The controls do not freeze each block mode's exact cell traversal while removing only its dictionary: different spatial orders can contribute to the block-mode gain. Thus `block modes over controls` is an incremental transport comparison, not a perfectly isolated estimate of dictionary deduplication alone.

## Validation and limits

All **2,345 new encoding candidates across 67 fixtures** reconstructed identical parsed JSON, including numeric types and signed zero. The 670 original candidates remain in the frozen baseline results. Twelve unit tests cover mixed-entity repeated blocks, arbitrary entity order, sparse IDs, internal and external references, global wires, mod fields, translated pages with different IDs, nested books, tiles, numeric precision, and random layouts. No string was imported into a running Factorio instance during that initial run. See [the accuracy audit](ACCURACY.md) for subsequent game-import validation.

The matcher handles exact translations, not rotations, reflections, approximate matches, or block-plus-exception patches. Cell sizes are heuristic and their phases are not searched. Original-order permutations and instance/dictionary overhead can outweigh the savings, particularly when the earlier compressor already captures the repetition. The source sampling limits and overlap between whole books and sampled pages remain those in `SITE_RESULTS.md`.

The decoder remains a trusted-input research tool; the extra search and compressor candidates also increase encoding cost. `BX0:` is still experimental.

## Reproduce

```sh
python3 -m unittest -v test_compact.py test_subassemblies.py
python3 benchmark_blocks.py
python3 report_blocks.py
```

`site-results.json` remains the frozen previous-prototype baseline. The block benchmark resumes from `block-results.json` and rejects an implementation-fingerprint mismatch; move that file aside before changing encoder code and rerunning. `block-summary.json` holds aggregates and `block-results.csv` holds a flat table. `block-local-results.json` and `block-local-summary.json` retain the initial within-page-only experiment.

## Sampled individual pages

| Source | Page | Previous | Best new | Extra reduction | Winner |
| --- | --- | ---: | ---: | ---: | --- |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 873 | 873 | 0.00% | `s/b` |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 1,133 | 1,084 | 4.32% | `o/b` |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | Moduled Advanced Oil Refning | 1,928 | 1,692 | 12.24% | `o/b` |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 1,622 | 1,336 | 17.63% | `o/b` |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | City Block with Concrete | 1,145 | 1,101 | 3.84% | `g/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 1-8 TU balancer | 462 | 462 | 0.00% | `s/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 1-9 TU balancer | 637 | 637 | 0.00% | `s/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 8-8 corner balancer | 568 | 568 | 0.00% | `s/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 8-8 TU balancer | 766 | 766 | 0.00% | `s/b` |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 128-128 balancer (128x72) | 7,569 | 6,673 | 11.84% | `o/b` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Early Game (Layer 1) | 5,324 | 5,012 | 5.86% | `r/b` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Late Game (Layer 7) | 21,869 | 21,378 | 2.25% | `r/b` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 6 | 20,098 | 19,533 | 2.81% | `r/b` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 5 | 18,693 | 18,238 | 2.43% | `r/b` |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 4 | 18,220 | 17,701 | 2.85% | `r/b` |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 11. Plastic | 590 | 590 | 0.00% | `s/b` |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 11. Sulfuric Acid | 850 | 850 | 0.00% | `s/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 1. Red Science & Green Circuits | 488 | 488 | 0.00% | `s/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 15. Blue Circuit Module (2 Red Belts) | 712 | 712 | 0.00% | `s/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 8. High Tech Shop | 1,072 | 1,072 | 0.00% | `s/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 13. Blue Science | 1,062 | 908 | 14.50% | `r/b` |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 15. Blue Circuits (2 Blue Belts) | 1,828 | 1,280 | 29.98% | `t/b` |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | 1x Roboport Block | 442 | 421 | 4.75% | `o/b` |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | 1st Biochambers | 2,386 | 2,382 | 0.17% | `g/b` |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 4,146 | 3,852 | 7.09% | `g/b` |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 5,038 | 4,920 | 2.34% | `g/b` |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 30,790 | 27,413 | 10.97% | `g/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3][item=turbo-transport-belt][item=speed-module-3][planet=fulgora] | 3,130 | 3,076 | 1.73% | `o/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3][item=foundry][item=speed-module-3][item=stack-inserter] | 3,244 | 3,190 | 1.66% | `o/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-2][item=express-transport-belt][item=speed-module-2] | 3,518 | 3,429 | 2.53% | `o/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3,quality=legendary][item=foundry,quality=legendary][item=cryogenic-plant][item=stack-inserter,quality=legendary] | 4,130 | 4,109 | 0.51% | `g/b` |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-2][item=fast-transport-belt][item=speed-module] | 4,156 | 3,857 | 7.19% | `o/b` |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | [virtual-signal=signal-item-parameter]Generic Train with Schedule | 544 | 544 | 0.00% | `s/b` |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Recycling Excess Modules | 1,877 | 1,712 | 8.79% | `g/b` |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Jellynut Processing | 1,344 | 1,344 | 0.00% | `s/b` |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | 1.4 GW Fusion Power | 1,524 | 1,524 | 0.00% | `s/b` |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Heavy Promethium Cruiser | 12,898 | 12,137 | 5.90% | `g/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | Throughput | 1,854 | 1,801 | 2.86% | `g/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 1920/s | 942 | 902 | 4.25% | `p/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 6/s | 1,150 | 1,114 | 3.13% | `r/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 120/s | 2,834 | 2,754 | 2.82% | `g/b` |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | Nauvis | 19,454 | 18,149 | 6.71% | `g/b` |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 1. Red Science & Green Circuits | 481 | 481 | 0.00% | `s/b` |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 13. Blue Science | 1,058 | 905 | 14.46% | `r/b` |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Belt Throughput Monitor | 853 | 852 | 0.12% | `o/b` |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Basic Smelting - Steel | 1,285 | 985 | 23.35% | `p/b` |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Plastic Block (Upgradeable) | 3,670 | 3,430 | 6.54% | `o/b` |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Smelting Block - Brick/Concrete | 2,737 | 1,964 | 28.24% | `a/b` |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Nauvis Base - Phase 3 | 37,452 | 33,361 | 10.92% | `o/l` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Science Lab Extension | 874 | 870 | 0.46% | `g/b` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Power Array (Left) | 1,661 | 1,600 | 3.67% | `g/b` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 5-Mall | 3,857 | 3,705 | 3.94% | `p/b` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Rail Block Connection | 18,450 | 16,977 | 7.98% | `g/b` |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Concrete Layout | 780 | 757 | 2.95% | `p/b` |
