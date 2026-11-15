# Benchmarks

All reported performance measurements on this page use **public gameplay blueprints**. There are no generated grids or image-art blueprints in this benchmark. Every design is linked to its public page; pinned source records and hashes allow the exact measured versions to be fetched even if a live page changes.

## Results

Lengths count every copied ASCII character, including prefixes. Native means compact blueprint JSON compressed with zlib level 9, padded Base64, and the `0` prefix. The new transport selects the shortest candidate. A larger factor means less text.

| Group | Fixtures | Native chars | Transport chars | Combined reduction factor | Median factor |
| --- | ---: | ---: | ---: | ---: | ---: |
| Complete public downloads | 13 | 2,614,053 | 527,338 | 4.96× | 3.33× |
| Complete books only | 9 | 2,492,593 | 492,832 | 5.06× | 3.94× |
| Sampled individual pages | 54 | 1,211,230 | 267,471 | 4.53× | 2.31× |

The complete downloads are nine books and four individual blueprints. Sampled pages also occur inside their books, so these groups overlap and must not be added together. Combined-size factors weight large files more heavily; the median reports each fixture's reduction factor with equal weight.

## Complete public blueprints and books

Each title opens the public design page. The pinned source record contains the exact blueprint string used in the measurement. `Previous` is the earlier structural prototype; `Transport` includes all current modes.

| Public design | Pinned record | Pages | Native | Previous | Transport | Native / transport | Extra reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mi/-MIMpsZJa9WHxI4H6fcD.json) | 110 | 489,893 | 109,718 | 94,932 | 5.16× | 13.48% |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ml/-ML5RsMXhj7tnbbzs02H.json) | 184 | 214,821 | 60,969 | 54,454 | 3.94× | 10.69% |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ln/-Ln7bpxs1Mmtyv9yx8x5.json) | 7 | 467,309 | 76,070 | 70,572 | 6.62× | 7.23% |
| [Compact, smart 1.1 GW 2x4 nuclear plant "little witch"](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mq/-MQ9-6LlT_g5PGsGXkyX.json) | 1 | 10,545 | 3,665 | 3,276 | 3.22× | 10.61% |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-k_/-K_Me61B1oQ_Dmjbde9B.json) | 1 | 2,885 | 1,388 | 1,388 | 2.08× | 0.00% |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-kp/-Kp6dxRcQbpr7UrzJC6x.json) | 2 | 2,697 | 1,290 | 1,284 | 2.10× | 0.47% |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-lr/-LrxBIuzRGB9jKLgPRqH.json) | 45 | 68,381 | 24,108 | 20,550 | 3.33× | 14.76% |
| [Fulgora Mall - 4 planets tech, normal quality](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ox/-OX4QBKmwEZ6dIBJY5C5.json) | 1 | 91,889 | 23,712 | 22,676 | 4.05× | 4.37% |
| [GSXR - Automatic MALL of ALL items.](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-of/-OFo0h6eKudNzNzkh9zL.json) | 1 | 16,141 | 8,181 | 7,166 | 2.25× | 12.41% |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ol/-OL_E6IO4gmQUdqFgTjq.json) | 8 | 53,617 | 19,369 | 17,154 | 3.13× | 11.44% |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ob/-OBdq3vJ2slIWEDAXEeM.json) | 149 | 695,609 | 154,521 | 144,994 | 4.80× | 6.17% |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-li/-LI0gc-a-2_VLWR-tx1d.json) | 45 | 68,313 | 24,092 | 20,550 | 3.32× | 14.70% |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | [source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mk/-MK-xIWwMHTIBuSh3ZWQ.json) | 21 | 431,953 | 72,108 | 68,342 | 6.32× | 5.22% |

## What produces the savings

Each stage below keeps the smallest complete string seen so far. These totals cover the 13 complete downloads and separate explicit block modes from the accompanying wire, ordering, and shared-settings improvements.

| Available representations | Total chars | Extra reduction from previous prototype |
| --- | ---: | ---: |
| Previous structural prototype | 579,191 | 0.00% |
| + Relative wire references | 561,019 | 3.14% |
| + Spatial/adaptive ordering | 540,601 | 6.66% |
| + Shared settings palette | 530,251 | 8.45% |
| + Local and shared block dictionaries | 527,338 | 8.95% |

All new modes together save **8.95%** beyond the previous prototype. Explicit block modes add **0.55%** beyond the other controls. That incremental comparison can also include differences in cell traversal order; it is not a perfectly isolated estimate of dictionary deduplication alone.

For context, the original representation change with zlib alone totaled 736,598 characters (3.55× smaller than native). Stronger compression of unchanged JSON totaled 1,473,062 characters. Current transport totals 527,338. Thus the measured savings are not solely from changing compressors.

## Sources and sampling

The 16 site posts were chosen by visible title, category, and favorites before compression was measured. They cover malls, starter bases, production lines, nuclear power, oil, balancers, rail systems, circuits, and Space Age designs. This is a convenience sample, not a random sample or a global popularity ranking. It includes two related versions of Base-in-a-Book.

The bytes come from the public [Factorio Prints mirror](https://github.com/motlin/factorio-blueprint-firebase-cdn), pinned at `1868b1efafa5e6603c42279974d292905ee8c82b`. Direct website downloads were unavailable in the measurement environment. The [source manifest](site-corpus/sources.json) records public pages, exact downloads, hashes, and snapshot metadata.

Complete downloads are measured up to 100,000 entity+tile placements. Three larger books are represented through sampled pages: Space Age Rail Blocks, Space Age Blueprints, and Nilaus Cityblock 2.0. For each multi-page book, pages with at least 20 placements are sorted by placement count and array path. The smallest, 25th-percentile, median, 75th-percentile, and largest ranks are selected. Identical parsed-JSON pages are deduplicated across books, leaving 54 sampled pages.

| Public source post | Exact measured source record | Coverage |
| --- | --- | --- |
| [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mi/-MIMpsZJa9WHxI4H6fcD.json) | Complete download; 5 sampled pages |
| [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ml/-ML5RsMXhj7tnbbzs02H.json) | Complete download; 5 sampled pages |
| [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ln/-Ln7bpxs1Mmtyv9yx8x5.json) | Complete download; 5 sampled pages |
| [Compact, smart 1.1 GW 2x4 nuclear plant "little witch"](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mq/-MQ9-6LlT_g5PGsGXkyX.json) | Complete download; 0 sampled pages |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-k_/-K_Me61B1oQ_Dmjbde9B.json) | Complete download; 0 sampled pages |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-kp/-Kp6dxRcQbpr7UrzJC6x.json) | Complete download; 2 sampled pages |
| [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-lr/-LrxBIuzRGB9jKLgPRqH.json) | Complete download; 5 sampled pages |
| [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ol/-OLexShcZSLG8qYkOLiy.json) | 5 sampled pages |
| [Fulgora Mall - 4 planets tech, normal quality](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ox/-OX4QBKmwEZ6dIBJY5C5.json) | Complete download; 0 sampled pages |
| [GSXR - Automatic MALL of ALL items.](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-of/-OFo0h6eKudNzNzkh9zL.json) | Complete download; 0 sampled pages |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ol/-OL_E6IO4gmQUdqFgTjq.json) | Complete download; 5 sampled pages |
| [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-og/-OglzvHBH0h-t8JIZKyF.json) | 5 sampled pages |
| [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ob/-OBdq3vJ2slIWEDAXEeM.json) | Complete download; 5 sampled pages |
| [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-li/-LI0gc-a-2_VLWR-tx1d.json) | Complete download; 2 sampled pages |
| [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-ox/-OXRxN4v1U8dwIjSO4l4.json) | 5 sampled pages |
| [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | [pinned source](https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/1868b1efafa5e6603c42279974d292905ee8c82b/-mk/-MK-xIWwMHTIBuSh3ZWQ.json) | Complete download; 5 sampled pages |

## Validation and encoding settings

All 3,015 candidates across these 67 fixtures reproduce identical parsed JSON, including numeric types and signed zero. The game audit compared all 67 original and reconstructed imports in Factorio 2.1.24 and found identical exports. Six pairs shared the same pre-existing import-error status. See the [accuracy audit](ACCURACY.md) for evidence and limits.

Each representation tries uncompressed, zlib-9, Brotli-11, Zstandard-19, and LZMA-9. `site-results.json` records the ten earlier candidates; `block-results.json` adds 35 graph/order/palette/block candidates. The current total is 45 candidates per fixture. Candidate search is more CPU-intensive than native export. Compressor versions are pinned in `requirements.txt`.

The block matcher searches exact translated spatial cells and strips. It preserves original row order through explicit permutations. It does not search rotations, reflections, or approximate blocks with exceptions. Modern wire lists are encoded separately. [Detailed encoding controls](BLOCK_RESULTS.md#implementation)

## Reproduce

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -v
python3 fetch_site_corpus.py
python3 benchmark_sites.py
python3 benchmark_blocks.py
python3 report_benchmarks.py
python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json
# Optional: requires a local Factorio installation with expansion data
python3 test_factorio.py /path/to/factorio/bin/x64/factorio /tmp/blueprint-import-pairs.json
```

Benchmark scripts resume from saved JSON results. Move `site-results.json` and/or `block-results.json` aside to recompute them; preserve the former to retain the previous-prototype baseline. The block script rejects a changed implementation fingerprint. Downloaded community strings stay local; only links, hashes, and measurements are committed. Synthetic examples and unit fixtures do not contribute to these performance totals.

Raw data: [baseline CSV](site-results.csv), [current CSV](block-results.csv), [baseline JSON](site-results.json), [current JSON](block-results.json). Earlier analyses: [structural comparison](SITE_RESULTS.md), [repeated-block comparison](BLOCK_RESULTS.md).

## Sampled public blueprint pages

The page links open the corresponding page in its public book. Array paths identify the exact measured page; source hashes identify the book snapshot.

| Public page | Book | Array path | Native | Transport | Smaller |
| --- | --- | --- | ---: | ---: | ---: |
| [(unnamed)](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=7%2F2) | [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | `7/2` | 1,125 | 873 | 1.29× |
| [(unnamed)](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=6%2F4) | [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | `6/4` | 2,217 | 1,084 | 2.05× |
| [Moduled Advanced Oil Refning](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=2%2F2) | [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | `2/2` | 3,965 | 1,692 | 2.34× |
| [(unnamed)](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=17%2F3) | [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | `17/3` | 5,293 | 1,336 | 3.96× |
| [City Block with Concrete](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=9%2F7) | [Factorio Master Class (by Nilaus)](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | `9/7` | 50,149 | 1,101 | 45.55× |
| [1-8 TU balancer](https://factorio.menzies.io/prints/-ML5RsMXhj7tnbbzs02H?page=0%2F8) | [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | `0/8` | 665 | 462 | 1.44× |
| [1-9 TU balancer](https://factorio.menzies.io/prints/-ML5RsMXhj7tnbbzs02H?page=0%2F9) | [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | `0/9` | 961 | 637 | 1.51× |
| [8-8 corner balancer](https://factorio.menzies.io/prints/-ML5RsMXhj7tnbbzs02H?page=7%2F10) | [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | `7/10` | 1,081 | 568 | 1.90× |
| [8-8 TU balancer](https://factorio.menzies.io/prints/-ML5RsMXhj7tnbbzs02H?page=7%2F14) | [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | `7/14` | 1,541 | 766 | 2.01× |
| [128-128 balancer (128x72)](https://factorio.menzies.io/prints/-ML5RsMXhj7tnbbzs02H?page=9%2F7) | [Raynquist's Belt Balancers Fall 2025](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | `9/7` | 60,981 | 6,673 | 9.14× |
| [Early Game (Layer 1)](https://factorio.menzies.io/prints/-Ln7bpxs1Mmtyv9yx8x5?page=0) | [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | `0` | 24,345 | 5,012 | 4.86× |
| [Late Game (Layer 7)](https://factorio.menzies.io/prints/-Ln7bpxs1Mmtyv9yx8x5?page=6) | [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | `6` | 77,261 | 21,378 | 3.61× |
| [Layer 6](https://factorio.menzies.io/prints/-Ln7bpxs1Mmtyv9yx8x5?page=5) | [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | `5` | 78,941 | 19,533 | 4.04× |
| [Layer 5](https://factorio.menzies.io/prints/-Ln7bpxs1Mmtyv9yx8x5?page=4) | [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | `4` | 76,145 | 18,238 | 4.18× |
| [Layer 4](https://factorio.menzies.io/prints/-Ln7bpxs1Mmtyv9yx8x5?page=3) | [Everything you need for Nauvis (Space Age Mall crafts over 170 items from ores to endproduct)](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | `3` | 79,217 | 17,701 | 4.48× |
| [11. Plastic](https://factorio.menzies.io/prints/-Kp6dxRcQbpr7UrzJC6x?page=0) | [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | `0` | 1,205 | 590 | 2.04× |
| [11. Sulfuric Acid](https://factorio.menzies.io/prints/-Kp6dxRcQbpr7UrzJC6x?page=1) | [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | `1` | 1,737 | 850 | 2.04× |
| [1. Red Science & Green Circuits](https://factorio.menzies.io/prints/-LrxBIuzRGB9jKLgPRqH?page=1) | [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | `1` | 713 | 488 | 1.46× |
| [15. Blue Circuit Module (2 Red Belts)](https://factorio.menzies.io/prints/-LrxBIuzRGB9jKLgPRqH?page=41) | [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | `41` | 1,321 | 712 | 1.86× |
| [8. High Tech Shop](https://factorio.menzies.io/prints/-LrxBIuzRGB9jKLgPRqH?page=18) | [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | `18` | 1,977 | 1,072 | 1.84× |
| [13. Blue Science](https://factorio.menzies.io/prints/-LrxBIuzRGB9jKLgPRqH?page=34) | [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | `34` | 2,781 | 908 | 3.06× |
| [15. Blue Circuits (2 Blue Belts)](https://factorio.menzies.io/prints/-LrxBIuzRGB9jKLgPRqH?page=42) | [Nilaus' Base-in-a-Book complete 0.17](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | `42` | 5,037 | 1,280 | 3.94× |
| [1x Roboport Block](https://factorio.menzies.io/prints/-OLexShcZSLG8qYkOLiy?page=7) | [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | `7` | 713 | 421 | 1.69× |
| [1st Biochambers](https://factorio.menzies.io/prints/-OLexShcZSLG8qYkOLiy?page=26%2F0) | [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | `26/0` | 3,301 | 2,382 | 1.39× |
| [(unnamed)](https://factorio.menzies.io/prints/-OLexShcZSLG8qYkOLiy?page=22%2F13) | [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | `22/13` | 12,205 | 3,852 | 3.17× |
| [(unnamed)](https://factorio.menzies.io/prints/-OLexShcZSLG8qYkOLiy?page=26%2F19) | [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | `26/19` | 16,925 | 4,920 | 3.44× |
| [(unnamed)](https://factorio.menzies.io/prints/-OLexShcZSLG8qYkOLiy?page=25%2F10) | [Rail Blocks (SpaceAge) v4.14](https://www.factorio.school/view/-OLexShcZSLG8qYkOLiy) | `25/10` | 108,653 | 27,413 | 3.96× |
| [[item=assembling-machine-3][item=turbo-transport-belt][item=speed-module-3][planet=fulgora]](https://factorio.menzies.io/prints/-OL_E6IO4gmQUdqFgTjq?page=3) | [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | `3` | 5,905 | 3,076 | 1.92× |
| [[item=assembling-machine-3][item=foundry][item=speed-module-3][item=stack-inserter]](https://factorio.menzies.io/prints/-OL_E6IO4gmQUdqFgTjq?page=4) | [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | `4` | 6,237 | 3,190 | 1.96× |
| [[item=assembling-machine-2][item=express-transport-belt][item=speed-module-2]](https://factorio.menzies.io/prints/-OL_E6IO4gmQUdqFgTjq?page=1) | [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | `1` | 7,073 | 3,429 | 2.06× |
| [[item=assembling-machine-3,quality=legendary][item=foundry,quality=legendary][item=cryogenic-plant][item=stack-inserter,quality=legendary]](https://factorio.menzies.io/prints/-OL_E6IO4gmQUdqFgTjq?page=6) | [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | `6` | 8,133 | 4,109 | 1.98× |
| [[item=assembling-machine-2][item=fast-transport-belt][item=speed-module]](https://factorio.menzies.io/prints/-OL_E6IO4gmQUdqFgTjq?page=2) | [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | `2` | 8,817 | 3,857 | 2.29× |
| [[virtual-signal=signal-item-parameter]Generic Train with Schedule](https://factorio.menzies.io/prints/-OglzvHBH0h-t8JIZKyF?page=0%2F0) | [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | `0/0` | 733 | 544 | 1.35× |
| [Recycling Excess Modules](https://factorio.menzies.io/prints/-OglzvHBH0h-t8JIZKyF?page=0%2F12) | [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | `0/12` | 3,033 | 1,712 | 1.77× |
| [Jellynut Processing](https://factorio.menzies.io/prints/-OglzvHBH0h-t8JIZKyF?page=4%2F5) | [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | `4/5` | 2,501 | 1,344 | 1.86× |
| [1.4 GW Fusion Power](https://factorio.menzies.io/prints/-OglzvHBH0h-t8JIZKyF?page=5%2F8) | [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | `5/8` | 3,701 | 1,524 | 2.43× |
| [Heavy Promethium Cruiser](https://factorio.menzies.io/prints/-OglzvHBH0h-t8JIZKyF?page=1%2F15) | [Space Age Blueprints](https://www.factorio.school/view/-OglzvHBH0h-t8JIZKyF) | `1/15` | 87,749 | 12,137 | 7.23× |
| [Throughput](https://factorio.menzies.io/prints/-OBdq3vJ2slIWEDAXEeM?page=3%2F1) | [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | `3/1` | 2,345 | 1,801 | 1.30× |
| [1920/s](https://factorio.menzies.io/prints/-OBdq3vJ2slIWEDAXEeM?page=7%2F0) | [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | `7/0` | 1,561 | 902 | 1.73× |
| [6/s](https://factorio.menzies.io/prints/-OBdq3vJ2slIWEDAXEeM?page=6%2F25) | [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | `6/25` | 2,669 | 1,114 | 2.40× |
| [120/s](https://factorio.menzies.io/prints/-OBdq3vJ2slIWEDAXEeM?page=11%2F1) | [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | `11/1` | 5,765 | 2,754 | 2.09× |
| [Nauvis](https://factorio.menzies.io/prints/-OBdq3vJ2slIWEDAXEeM?page=1%2F1) | [Tileable factories, v0.60.0](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | `1/1` | 94,521 | 18,149 | 5.21× |
| [1. Red Science & Green Circuits](https://factorio.menzies.io/prints/-LI0gc-a-2_VLWR-tx1d?page=1) | [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | `1` | 705 | 481 | 1.47× |
| [13. Blue Science](https://factorio.menzies.io/prints/-LI0gc-a-2_VLWR-tx1d?page=34) | [Nilaus' Base-in-a-Book complete](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | `34` | 2,777 | 905 | 3.07× |
| [Belt Throughput Monitor](https://factorio.menzies.io/prints/-OXRxN4v1U8dwIjSO4l4?page=8%2F12) | [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | `8/12` | 1,117 | 852 | 1.31× |
| [Basic Smelting - Steel](https://factorio.menzies.io/prints/-OXRxN4v1U8dwIjSO4l4?page=1%2F1) | [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | `1/1` | 2,949 | 985 | 2.99× |
| [Plastic Block (Upgradeable)](https://factorio.menzies.io/prints/-OXRxN4v1U8dwIjSO4l4?page=8%2F14) | [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | `8/14` | 8,145 | 3,430 | 2.37× |
| [Smelting Block - Brick/Concrete](https://factorio.menzies.io/prints/-OXRxN4v1U8dwIjSO4l4?page=1%2F5) | [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | `1/5` | 9,345 | 1,964 | 4.76× |
| [Nauvis Base - Phase 3](https://factorio.menzies.io/prints/-OXRxN4v1U8dwIjSO4l4?page=6%2F2) | [Nilaus Cityblock 2.0](https://www.factorio.school/view/-OXRxN4v1U8dwIjSO4l4) | `6/2` | 204,217 | 33,361 | 6.12× |
| [Science Lab Extension](https://factorio.menzies.io/prints/-MK-xIWwMHTIBuSh3ZWQ?page=13) | [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | `13` | 1,753 | 870 | 2.01× |
| [Power Array (Left)](https://factorio.menzies.io/prints/-MK-xIWwMHTIBuSh3ZWQ?page=14) | [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | `14` | 5,165 | 1,600 | 3.23× |
| [5-Mall](https://factorio.menzies.io/prints/-MK-xIWwMHTIBuSh3ZWQ?page=4) | [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | `4` | 9,737 | 3,705 | 2.63× |
| [Rail Block Connection](https://factorio.menzies.io/prints/-MK-xIWwMHTIBuSh3ZWQ?page=17) | [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | `17` | 42,701 | 16,977 | 2.52× |
| [Concrete Layout](https://factorio.menzies.io/prints/-MK-xIWwMHTIBuSh3ZWQ?page=18) | [ElderAxe's Quick Start Base (v11.2.5)](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | `18` | 61,421 | 757 | 81.14× |
