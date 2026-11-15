# Benchmarks

These 13 public blueprint designs used **80% less text overall** after compression. Each name links to its public blueprint page.

Sizes below count the characters in each string.

| Blueprint | Factorio size | Compact size | Smaller by |
| --- | ---: | ---: | ---: |
| [Nilaus Master Class](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | 489,893 | 94,932 | 81% |
| [Raynquist Belt Balancers](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 214,821 | 54,454 | 75% |
| [Nauvis Space Age Mall](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | 467,309 | 70,572 | 85% |
| [Little Witch Nuclear Plant](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | 10,545 | 3,276 | 69% |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | 2,885 | 1,388 | 52% |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 2,697 | 1,284 | 52% |
| [Nilaus Base-in-a-Book (0.17)](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 68,381 | 20,550 | 70% |
| [Fulgora Mall](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | 91,889 | 22,676 | 75% |
| [GSXR Automatic Mall](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | 16,141 | 7,166 | 56% |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | 53,617 | 17,154 | 68% |
| [Tileable Factories](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 695,609 | 144,994 | 79% |
| [Nilaus Base-in-a-Book](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 68,313 | 20,550 | 70% |
| [ElderAxe Quick Start Base](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 431,953 | 68,342 | 84% |
| **Total** | **2,614,053** | **527,338** | **80%** |

The test includes factories, malls, power plants, balancers, and blueprint books. Results vary with how much repeated data each design contains.

The original and restored blueprints produced identical exports in Factorio 2.1.24. [Accuracy checks](ACCURACY.md)

For anyone reproducing the test: [measurements](block-results.csv), [exact source versions](site-corpus/sources.json), [test scripts](benchmark_blocks.py).
