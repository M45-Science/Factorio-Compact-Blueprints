# Popular blueprint-site benchmark

The unchanged codec was tested against 16 curated public site posts, spanning balancers, malls, starter bases, nuclear power, oil processing, rail blocks, circuit-controlled production, and Space Age designs. No synthetic layouts or image blueprints are included in these results.

## Findings

| Group | Fixtures | Median reduction factor | Combined-size reduction factor |
| --- | ---: | ---: | ---: |
| Individual pages sampled from books | 54 | 2.09× | 4.23× |
| Entity-led sampled pages (entities > tiles) | 48 | 2.04× | 3.76× |
| Tile-led sampled pages | 6 | 5.11× | 9.69× |
| Complete books | 9 | 3.52× | 4.60× |
| Single-blueprint site posts | 4 | 2.48× | 3.29× |
| All complete site downloads | 13 | 2.88× | 4.51× |

Complete downloads totaled **2,614,053 native characters → 579,191 prototype characters**, a **77.8%** reduction. Keeping zlib level 9 and only changing the representation gave **3.55×** reduction. The best JSON-only modern-compressor candidates totaled 1,473,062 characters; structural encoding was another **2.54×** smaller than those.

The practical result is roughly 2× for a median individual gameplay page, with larger gains for books and regular layouts. Large tile patterns create the extreme outliers; they should not be treated as typical production blueprints.

## Complete downloads

Native sizes below use consistent zlib-9 re-encoding of the site's parsed JSON. The exact downloaded string length is also recorded; one site's older string was larger than its re-encoded baseline.

| Source | Favorites | Pages | Downloaded | Native baseline | Prototype | Smaller | Structured + zlib |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | 560 | 110 | 489,893 | 489,893 | 109,718 | 4.47× | 130,580 |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 612 | 184 | 214,821 | 214,821 | 60,969 | 3.52× | 69,420 |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | 981 | 7 | 467,309 | 467,309 | 76,070 | 6.14× | 117,902 |
| [Compact, smart 1.1 GW 2x4 nuclear plant "little witch"](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | 10 | 1 | 10,545 | 10,545 | 3,665 | 2.88× | 4,022 |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | 1,457 | 1 | 2,885 | 2,885 | 1,388 | 2.08× | 1,542 |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 344 | 2 | 2,697 | 2,697 | 1,290 | 2.09× | 1,430 |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 236 | 45 | 75,985 | 68,381 | 24,108 | 2.84× | 26,640 |
| [Fulgora Mall - 4 planets tech, normal quality](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | 94 | 1 | 91,889 | 91,889 | 23,712 | 3.88× | 28,564 |
| [GSXR - Automatic MALL of ALL items.](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | 85 | 1 | 16,141 | 16,141 | 8,181 | 1.97× | 9,997 |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | 31 | 8 | 53,617 | 53,617 | 19,369 | 2.77× | 22,096 |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 943 | 149 | 695,609 | 695,609 | 154,521 | 4.50× | 198,846 |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 2,589 | 45 | 68,313 | 68,313 | 24,092 | 2.84× | 26,630 |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 891 | 21 | 431,953 | 431,953 | 72,108 | 5.99× | 98,929 |

## Sampling and provenance

Designs were selected by visible title, category, and favorites before compression was measured. Discovery used Factorio Blueprints, Factorio Prints/School, Blueprint Atlas, and FactorioBin. Direct HTTP downloads from those sites returned access errors in this environment. The tested bytes were therefore downloaded from the public [Factorio Prints mirror](https://github.com/motlin/factorio-blueprint-firebase-cdn), pinned to commit `1868b1efafa5e6603c42279974d292905ee8c82b`. These are Factorio Prints site posts; this run does not claim independent downloads from every discovery site.

This is a varied convenience sample, not the global top 16, a random sample, or a cross-site popularity ranking. Mirror favorite counts range from 10 to 2,589; lower-favorite modern/circuit examples were included for variety. Counts may differ from indexed website pages because snapshots have different dates. The set also includes two versions of Base-in-a-Book, so the complete-book aggregate contains correlated designs.

A complete site download is tested if it contains at most 100,000 entity+tile placements. Three larger books (Space Age Rail Blocks, Space Age Blueprints, and Nilaus Cityblock 2.0) were tested through sampled pages only. Within each multi-page book, pages with at least 20 placements are sorted by placement count (then array path). The smallest, 25th-percentile, median, 75th-percentile, and largest ranks are selected. Identical parsed-JSON leaf pages are deduplicated across books, yielding 54 sampled pages. These pages also occur inside the whole books; the two groups must not be pooled as independent observations. This sampling favors size coverage and can include large tile-only pages and instructional pages.

All **670 encoding candidates across 67 fixtures** passed exact parsed-JSON reconstruction, including numeric types and signed zero. The pre-existing five unit tests also passed. The codec was not changed for these measurements. No restored string was imported into a running Factorio instance during that initial run. See [the accuracy audit](ACCURACY.md) for subsequent game-import validation.

All lengths count copied ASCII characters including prefixes. Native baseline: compact JSON, zlib level 9, padded Base64, `0` prefix. Prototype: best of uncompressed, zlib-9, Brotli-11, Zstandard-19, and LZMA-9, tried on both JSON and structural MessagePack, with `BX0:` header and unpadded Base64URL. Selecting the smallest of these is computationally more expensive than native export. No external dictionary is used.

## Reproduce

```sh
python3 fetch_site_corpus.py
python3 benchmark_sites.py
python3 report_sites.py
```

The benchmark resumes from `site-results.json`. Remove that file to rerun measurements after changing codec code or the corpus. Source hashes, exact download URLs, favorites, tags, and source titles are in `site-corpus/sources.json`. Per-candidate lengths, timings, entity/tile counts, and book paths are in `site-results.json`; aggregates are in `site-summary.json`. A flat table is in `site-results.csv`.

## Sampled individual pages

| Source | Page | Entities | Tiles | Native | Prototype | Smaller |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 32 | 0 | 1,125 | 873 | 1.29× |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 196 | 0 | 2,217 | 1,133 | 1.96× |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | Moduled Advanced Oil Refning | 351 | 4 | 3,965 | 1,928 | 2.06× |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | (unnamed) | 559 | 0 | 5,293 | 1,622 | 3.26× |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | City Block with Concrete | 96 | 13,456 | 50,149 | 1,145 | 43.80× |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 1-8 TU balancer | 20 | 0 | 665 | 462 | 1.44× |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 1-9 TU balancer | 45 | 0 | 961 | 637 | 1.51× |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 8-8 corner balancer | 76 | 0 | 1,081 | 568 | 1.90× |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 8-8 TU balancer | 119 | 0 | 1,541 | 766 | 2.01× |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 128-128 balancer (128x72) | 7,315 | 0 | 60,981 | 7,569 | 8.06× |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Early Game (Layer 1) | 2,395 | 44 | 24,345 | 5,324 | 4.57× |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Late Game (Layer 7) | 6,428 | 44 | 77,261 | 21,869 | 3.53× |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 6 | 6,769 | 44 | 78,941 | 20,098 | 3.93× |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 5 | 6,792 | 44 | 76,145 | 18,693 | 4.07× |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | Layer 4 | 7,339 | 44 | 79,217 | 18,220 | 4.35× |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 11. Plastic | 104 | 0 | 1,205 | 590 | 2.04× |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 11. Sulfuric Acid | 159 | 0 | 1,737 | 850 | 2.04× |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 1. Red Science & Green Circuits | 23 | 0 | 713 | 488 | 1.46× |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 15. Blue Circuit Module (2 Red Belts) | 96 | 0 | 1,321 | 712 | 1.86× |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 8. High Tech Shop | 169 | 0 | 1,977 | 1,072 | 1.84× |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 13. Blue Science | 274 | 0 | 2,781 | 1,062 | 2.62× |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 15. Blue Circuits (2 Blue Belts) | 580 | 0 | 5,037 | 1,828 | 2.76× |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | 1x Roboport Block | 20 | 0 | 713 | 442 | 1.61× |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | 1st Biochambers | 129 | 0 | 3,301 | 2,386 | 1.38× |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 956 | 0 | 12,205 | 4,146 | 2.94× |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 1,392 | 0 | 16,925 | 5,038 | 3.36× |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | (unnamed) | 7,863 | 0 | 108,653 | 30,790 | 3.53× |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3][item=turbo-transport-belt][item=speed-module-3][planet=fulgora] | 404 | 0 | 5,905 | 3,130 | 1.89× |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3][item=foundry][item=speed-module-3][item=stack-inserter] | 450 | 0 | 6,237 | 3,244 | 1.92× |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-2][item=express-transport-belt][item=speed-module-2] | 544 | 0 | 7,073 | 3,518 | 2.01× |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-3,quality=legendary][item=foundry,quality=legendary][item=cryogenic-plant][item=stack-inserter,quality=legendary] | 610 | 0 | 8,133 | 4,130 | 1.97× |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [item=assembling-machine-2][item=fast-transport-belt][item=speed-module] | 769 | 0 | 8,817 | 4,156 | 2.12× |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | [virtual-signal=signal-item-parameter]Generic Train with Schedule | 21 | 0 | 733 | 544 | 1.35× |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Recycling Excess Modules | 104 | 0 | 3,033 | 1,877 | 1.62× |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Jellynut Processing | 168 | 0 | 2,501 | 1,344 | 1.86× |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | 1.4 GW Fusion Power | 387 | 0 | 3,701 | 1,524 | 2.43× |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | Heavy Promethium Cruiser | 4,067 | 10,676 | 87,749 | 12,898 | 6.80× |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | Throughput | 20 | 0 | 2,345 | 1,854 | 1.26× |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 1920/s | 85 | 0 | 1,561 | 942 | 1.66× |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 6/s | 201 | 0 | 2,669 | 1,150 | 2.32× |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 120/s | 369 | 0 | 5,765 | 2,834 | 2.03× |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | Nauvis | 6,814 | 0 | 94,521 | 19,454 | 4.86× |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 1. Red Science & Green Circuits | 23 | 0 | 705 | 481 | 1.47× |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 13. Blue Science | 274 | 0 | 2,777 | 1,058 | 2.62× |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Belt Throughput Monitor | 21 | 0 | 1,117 | 853 | 1.31× |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Basic Smelting - Steel | 294 | 0 | 2,949 | 1,285 | 2.29× |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Plastic Block (Upgradeable) | 706 | 0 | 8,145 | 3,670 | 2.22× |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Smelting Block - Brick/Concrete | 651 | 800 | 9,345 | 2,737 | 3.41× |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | Nauvis Base - Phase 3 | 21,887 | 0 | 204,217 | 37,452 | 5.45× |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Science Lab Extension | 116 | 0 | 1,753 | 874 | 2.01× |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Power Array (Left) | 184 | 666 | 5,165 | 1,661 | 3.11× |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 5-Mall | 563 | 666 | 9,737 | 3,857 | 2.52× |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Rail Block Connection | 2,376 | 843 | 42,701 | 18,450 | 2.31× |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | Concrete Layout | 0 | 17,047 | 61,421 | 780 | 78.74× |
