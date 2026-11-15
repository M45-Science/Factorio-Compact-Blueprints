# Benchmarks

These 13 public blueprint designs used **81% less text overall** after compression: about 5:1, or roughly one-fifth the original length. Each name links to its public blueprint page.

Sizes below count the characters in each string.

| Blueprint | Factorio size | Compact size | Smaller by | Ratio |
| --- | ---: | ---: | ---: | ---: |
| [Nilaus Master Class](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | 489,893 | 91,190 | 81% | 5.4:1 |
| [Raynquist Belt Balancers](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 214,821 | 53,581 | 75% | 4.0:1 |
| [Nauvis Space Age Mall](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | 467,309 | 67,932 | 85% | 6.9:1 |
| [Little Witch Nuclear Plant](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | 10,545 | 3,261 | 69% | 3.2:1 |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | 2,885 | 1,388 | 52% | 2.1:1 |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 2,697 | 1,284 | 52% | 2.1:1 |
| [Nilaus Base-in-a-Book (0.17)](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 68,381 | 20,054 | 71% | 3.4:1 |
| [Fulgora Mall](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | 91,889 | 21,058 | 77% | 4.4:1 |
| [GSXR Automatic Mall](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | 16,141 | 6,665 | 59% | 2.4:1 |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | 53,617 | 16,678 | 69% | 3.2:1 |
| [Tileable Factories](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 695,609 | 138,326 | 80% | 5.0:1 |
| [Nilaus Base-in-a-Book](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 68,313 | 20,054 | 71% | 3.4:1 |
| [ElderAxe Quick Start Base](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 431,953 | 66,444 | 85% | 6.5:1 |
| **Total** | **2,614,053** | **507,915** | **81%** | **5.1:1** |

Ratios compare Factorio size to compact size: 5:1 means the compact string is one-fifth as long.

The test includes factories, malls, power plants, balancers, and blueprint books. Results vary with how much repeated data each design contains.

The original and restored blueprints produced identical exports in Factorio 2.1.24. [Accuracy checks](ACCURACY.md)

For anyone reproducing the test: [measurements](optimized-results.csv), [exact source versions](site-corpus/sources.json), [test scripts](benchmark_optimized.py).

## One example

[Nilaus Master Class](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) is a blueprint book: **489,893 → 91,190 characters**, or **5.4:1** (about one-fifth the original length).

<details>
<summary>Compare the strings side by side</summary>

<table>
<tr><th>Factorio string</th><th>Compact string</th></tr>
<tr><td valign="top"><pre>0eNrUvWtvHEmWJfhXCH7axSi63N5micYA1YUZoAf
9WFT2fhokhBAVUgaKIokgmbVZDf339RClCCfpN+y
c48GamS/1kBTHr1279rqPc//z8sP14+Zut715eP/
h9vYvlz/95/FP7i9/+p//SfyD/d9tr25vnv74fvv
5Zn29/7OH3+82lz9dbh82Xy7fXd6sv+z/3/r+fvP
lw/X25vPqy/rq1+3NZuUuv7673N583Px/lz+5r++
...</pre></td><td valign="top"><pre>BX0:il_Td6WFoAAATm1rRGAgAhARwAAAAQz1jM46
-A7_5dAEkoSkknF0nPMcDF3DyKi_8zIAfZ8UTKh2
kZLAC-KFVfvS3otKLmp5lUYp8w9r1bYIsjxhm54c
MN8gCNZqZKQ21F-acYL2PNNLa1K1f9SBkK1H3iPL
U-UPiIS0epoSxxjB3w7tb3lfitar35CB33xq-GuA
RdquqkUsui-BQPFbhStfLqgMZSukLCuP1J8ntIVg
...</pre></td></tr>
</table>

Previews show the first 240 characters. Full copyable strings: [Factorio string](examples/master-class.factorio.txt) · [compact string](examples/master-class.compact.txt).

</details>
