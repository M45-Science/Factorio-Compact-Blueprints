# Benchmarks

These 13 public blueprint designs used **80% less text overall** after compression: about 5:1, or roughly one-fifth the original length. Each name links to its public blueprint page.

Sizes below count the characters in each string.

| Blueprint | Factorio size | Compact size | Smaller by | Ratio |
| --- | ---: | ---: | ---: | ---: |
| [Nilaus Master Class](https://www.factorio.school/view/-MIMpsZJa9WHxI4H6fcD) | 489,893 | 94,932 | 81% | 5.2:1 |
| [Raynquist Belt Balancers](https://www.factorio.school/view/-ML5RsMXhj7tnbbzs02H) | 214,821 | 54,454 | 75% | 3.9:1 |
| [Nauvis Space Age Mall](https://www.factorio.school/view/-Ln7bpxs1Mmtyv9yx8x5) | 467,309 | 70,572 | 85% | 6.6:1 |
| [Little Witch Nuclear Plant](https://www.factorio.school/view/-MQ9-6LlT_g5PGsGXkyX) | 10,545 | 3,276 | 69% | 3.2:1 |
| [All the Inserters](https://www.factorio.school/view/-K_Me61B1oQ_Dmjbde9B) | 2,885 | 1,388 | 52% | 2.1:1 |
| [Plastic and Sulfuric Acid](https://www.factorio.school/view/-Kp6dxRcQbpr7UrzJC6x) | 2,697 | 1,284 | 52% | 2.1:1 |
| [Nilaus Base-in-a-Book (0.17)](https://www.factorio.school/view/-LrxBIuzRGB9jKLgPRqH) | 68,381 | 20,550 | 70% | 3.3:1 |
| [Fulgora Mall](https://www.factorio.school/view/-OX4QBKmwEZ6dIBJY5C5) | 91,889 | 22,676 | 75% | 4.1:1 |
| [GSXR Automatic Mall](https://www.factorio.school/view/-OFo0h6eKudNzNzkh9zL) | 16,141 | 7,166 | 56% | 2.3:1 |
| [Space Platform Factory](https://www.factorio.school/view/-OL_E6IO4gmQUdqFgTjq) | 53,617 | 17,154 | 68% | 3.1:1 |
| [Tileable Factories](https://www.factorio.school/view/-OBdq3vJ2slIWEDAXEeM) | 695,609 | 144,994 | 79% | 4.8:1 |
| [Nilaus Base-in-a-Book](https://www.factorio.school/view/-LI0gc-a-2_VLWR-tx1d) | 68,313 | 20,550 | 70% | 3.3:1 |
| [ElderAxe Quick Start Base](https://www.factorio.school/view/-MK-xIWwMHTIBuSh3ZWQ) | 431,953 | 68,342 | 84% | 6.3:1 |
| **Total** | **2,614,053** | **527,338** | **80%** | **5.0:1** |

Ratios compare Factorio size to compact size: 5:1 means the compact string is one-fifth as long.

The test includes factories, malls, power plants, balancers, and blueprint books. Results vary with how much repeated data each design contains.

The original and restored blueprints produced identical exports in Factorio 2.1.24. [Accuracy checks](ACCURACY.md)

For anyone reproducing the test: [measurements](block-results.csv), [exact source versions](site-corpus/sources.json), [test scripts](benchmark_blocks.py).

## One example

[Advanced Oil Refining](https://factorio.menzies.io/prints/-MIMpsZJa9WHxI4H6fcD?page=2%2F2) is a mid-sized individual blueprint: **3,965 → 1,692 characters**, or **2.3:1** (less than half the original length).

<details>
<summary>Compare the strings side by side</summary>

<table>
<tr><th>Factorio string</th><th>Compact string</th></tr>
<tr><td valign="top"><pre>0eNrFXdtu48gR/ZWBns0F+940FgH2A4IAeQ0GA1m
iPcTSkkBJkzgD/3tIeSxRl3KdKkXefVisveapS1c
1q7tON39OHtptveqaxWZy/3PSzJaL9eT+Xz8n6+Z
pMW2H321eVvXkftJs6ufJ3WQxfR5+WjZt0dWPzaL
uXiavd5NmMa//M7k3r3fsow/1tJcyesgCD61XdT0
vnpfzbVsXbvSwAx5edf1zs03zo9m8XMLwr1/vJvV
i02ya+s363Q8v3xbb54e66806QDWrutgsi6duuV3
MexGr5bp/rLenF95DFeVv4W7y0v+Hsb+F10G5Eyx
7hPUhgruM4BgEwwF4BoDVIMD+sJw7IqOL5XRJDID
jADJsTOCMqRhdAqeLKRkEzyIYBiGyCFyEJhbBwS7
NnEsNF6wVq01gEDKLEGF7jGEN4gLWsOlnMgfBTgG
GC1XD5o3lYtWwuWvxidV4dmLl4tawyWPZqZXNYOt
xkxJrEhe6hs1Fy02whp0QLBuxbAZZNmLZNLYV/tJ
hX8KOi13LZpDjJlrLv8gtbpJjTeJi17IZ7bi51rI
Z7biItWwSOrYkYJPQJdyxkXUsXiDY43S8m8ybrp6
9/UG8BM3NwpZNTl/itekhpksCzODFqSEg2PrWsBB
4gUsh4BUuhYCXuCXr1QiXqJQ2Ca6SKYQMF5YUAl7
cEgihhEtTCsHApSmFgE+5iRvX4ODCktIGL24pBDx
OK9aeiFemlDoJr0wpCHy6NWzqBUGZS+gTBWUuBSE
ocx1nUhSUuZQ+gjKXghCUuYE1KeA1KqVPxCtlCgI
vGkb6UCZlvGam9KnwmpmASHhxYNjpIQkKXkofi5f
dFAS+t2DZeid5vGam9Al4zUxB4NsLIzDKJEHpyyZ
myng1TxlX4dU8AZHZxRqb29loanjCK9niVTuljyC
KjycKdk2RDzH9XM+b7XNRt/3fd82sWC3bS9Xn8Vv
0bjJbLhZvEtbDn5jhX109H2+MN/1PeSx994t08gs
TzevX14v242WLK2n77SXoUTZtn1cXAC0Jt7N90y3
bbw/19+mPZtkNz8yabrZtNt/6/zffAz023Xrz7az
x8Nhum/mh89A2T983xbJpJ29+XW+mQ6PFlP0/wy+
eV9NuuhnETH6fvAp87ynHHtJ/3eNOn3rfThd/XvC
CV466Px31TKmSUVXSiSpnQwIplig9DjPQ+wgUvec
fmsXO8+fqVLQ6/nKEPDbtpu6IxtnHIbHdxcOogfb
1YmMBf5G7SjZfVOa0M3e+ZN8PUN4hDt213VicdOX
6fLwkwPIC/FUCHC/AXCXAswKuww8s/nUOiiz+dSO
ceP+UVwnIvAB3lYCKFxCvEWDKkpdQXSeBT+RD+ai
TwGfyoZrTSeBT+VAP6SRwJf9hLopUj5Yr+QvLQnD
L1cKxEImpc8rD87eucrYPfXk5VDZHVU44L3L+Jil
yjKPKR1NmeJeZ9F+F7jJTCGyznh1DtlnPBhLbrGe
jedSsXz9P27Zop5eiKbI4Xr4TeRab/iJygDQ0vLO
iYtMK1DFhOmZWx6zY3wB1rCAdLRsytlSspjEdR4y
A2ff6uZ9V2mLVDtPJeYrvh+it19YDN6vj6Wj0drj
MAbt3lw20kKeKfVIEylNOuBg/GEVC4i8wEiLgTra
3czKejYe3IWlSgk0qCYu+19MfL8PCrJh109mfzeJ
Jb1pWEAYDliAV/OajfMWSH3gEIwzrEyPRAqA821F
y1G6DGZEpuAhwt48A5+QUSSwARiQNzs5I5e77FsT
/wc4gZ0+Cdka0siGjNMl7vaBuWRj/URf/zpzGv49
k/Fdy0iVmrS/RLjU1Eh5/q1e3j1mPzxTGfoI6Dm6
7k/71CoIqOPhB0bsGoaMwi4xVplE+TaNA7Z8bjxc
SJnxCcGS4VU8GR6Ug2WIjOGL0sM7Kt3dWMAruLWi
phSkK1DgEp2jGg9pJe34m6zLJR7jFZwK+yjisZG8
YHBHmHpAjmBQUZHAEM+4s/wnOqmBWA+WsWCrIzZi
zonT5Yb0q3M96ncN74/g31pAFWbQKJgboAIdHS7p
9tEQPEzTIaAkKxjboLDbxM6udoquu72SbmAVRpui
yi6b8mEjRFbwTZaizUAL2+n7GKZG2tmHpaodNpZL
SzsIQpIFOQc8n9fEwPZ+ECDjDn4KImhMHUKqmhO5
MkfZlBW8f061CzxRQumW4X0QiwP0iEsHCZxEoBDy
iPauNh08lUAj4eyOS84e9iBzlu0fYzJQTfIqBsjr
DJw8ohEpxbgCyTkBVMmzKVEZzGADK58riRwMo7QQ
rOksXBhehVfx6bIACfoCAMjxqqPLYsCTFGh7L6Co
rtCYjU7CrkkVjb8tSAQ1NPbY0+JkC6tS31RDwMe0
cfsKA0s4ruPQlBRY0xHwkzG0p4Px7YfgknHFPGa4
58lpi2lUMbWnonX6wgPoEdva1vCV6tWZZypCN3Ng
Yozg6gM0ORpDaFZc8hk1mdqoRUIpcKQvD8aUgH54
SKP8y+tzVhwQ+isOoPyQi2z0462DG055+PyWcbXc
EUvGkIMKD0Z/V5wRucUzgOCiwYwLWVDiZ3yjos9a
WOJlfJ8DgZH6dAAuT+XX4Dibz6/A9TObX4QeczK8
TEHEyv05Awsn8OgEZ5/LrBFQ4lV8lwJU4k18nwOB
Efp0AK2VWvmcFefeTk/MRHVTsO2l7dj/DkboGcDO
SBBCs4ClbL75FBaSrQAFfrNjEnCvPuaASb/BhLvD
oPSfkFWLS/qbhhttbOUEIGxbv5Pwg0I0evXiDtDr
I95JAq8XUJXbMk5wdAvoRvoqC1K2S9tu5kQkKcgA
2MuwVQZabF4JiFYy9B4L0NIDlRmZE/AEb06AXg7S
rTGoYlasqd4NF1aoeHq97xz9N16KF1Yj6c3T1Mf3
qTsd0i+n8x3Qx6wub4fFVt5zV6/UVnAsruCZp3zn
30HzBcn/21Y+nrpxU3EnnoQyS3KREAV8MePZWpZK
z2YEB4j8nPgQXNDlReLCXNVnOU1HcQAaDQ873B4M
jgwUdaXIF9mspAAFPphKN5ogl83HY7kvMG8dtsvK
OLxYeSVGpYvGR4EqVHN+ADkP8pGFQHJUFIy6h7Wf
SWYo+LhgilbwIx0KE5f4YbgrIaKbui+8bhwh/DRb
3zpTcgmVFA8kSiywXZAJikZUlQI5oY4zULclbgGC
Ycm86x45phTXWMH009x5hozBiFkHrkr0j0w3WJf+
e9n86Wo8Uuznuw2+qnCDMuu28PrlVqgjDMu7Dj6y
coOwPwI7XRsPU9eHHVoALrpwNo6+t3OlXam7gB/0
CCgjQmWt3R1Z/ISStU4qxVyqtV3ZU2vdRLlXWhHK
0dlUPzzFMvGaA/LDZ/Y6UiNV0Bd6v8D5JZ+qTAOL
rFd4RKwpRfJKKAwQvL+EsjRBM4mCS0LzEmSfdld+
X1iQidkvJHidTX3goMZyKwxFvxlcfW+hKaetqX2C
QiNgdPnsc0laP3mxFXWzq8MuxqOtVXam4GAS7G9S
x3Lj98Qdauyzf3DIlpl2lgIaolc6U4nMRpsSQDXi
igPSoQc8kkEFn5LdtgAEjoKB54YgEOTIWRiaCX2q
gRySJT1Wg0ZLBuyTosZbfcwGOtUXvuSD9ZhXHFcB
w4b9uZVjtnEI7LOQkX72ysoixQX59ATrgEb1cgYx
G/ttYbLJZxXYWGjSVAhobcf4SqcQZ7oz8nAMYNA7
+0AA5spIbnEpZ3PHf2WJz2SmOJoBB4xSfI0CDJqH
fW6ANz/KDE2jQSMizTkFac17CntVJkNBndRIE/Fm
dAAGBVidAwKDVCZBQaHUSJBxanQQJiVYnQcKi1Um
Q0GhVEoKER6uTICHS8hK+3k02TfvrK9dnU8+vK6P
NgPK++zn977SbF73gWVdv6qKtH4cjCeTDmmevkQu
L/frmmMGP+y+e303a6UPd9r/7+85J8y9//GqSffl
H0375Z/24eOuQ/ai79dtrLRuffJViMmUM8fX1f1u
VG6k=</pre></td><td valign="top"><pre>BX0:obG9wSERWcDAAdh7HzJOjStbBXaQ6c_KjP6P
_W2s2etENDEUsfrTxCI-RVH8Ha7GDVJIlaKKKNVM
Gq_d6me-dP5r9skj0g3lTFH4MDRAWoAiTUSWAHxM
Kwi1ApqKqpObVJgc_npnYe2BfYqU0u3y99ko4A3Z
coHZ1nEI5IVc653YypnlKrmxFbxHN24vZg6zTf4Q
3grh3bYKifzGSbtqrN1vXiXpfbvU5p9n7sBoBNF2
jDQxusJISuZzbNbLtSLwkdysUAk_XQPeqVb7lI8A
xv3H0BNha2v09-hWuS5w3qBptgxgREG9qru-8bPM
aLP48udoO6ZaYVuZG9pbq-txzKLYgpDImDyNxpNP
srDZwt93rkgbJdwWE_0BiM7tlR9YYlfk0wgEpp5O
h6wsLkDHtsa042fAM_iSM8st3rxL5lo2RFztmwAu
YaJdqx_CTEbrDtlltfWqt2f3ngaIxXevZc_D6-0s
nXsGlM8h0lzB-SXeMb5UVgzh2Kg_B4KiRxYGLQnI
4uHFEv9f-gJYSe3Q83bogg_aLVnNIsbiAJPLgmg5
RRiQR3pqVo-HENusFwxSlYhNkKYvsjk2LTBGgjwu
FQYPIOOnS3HuFB5Nf6RQVMw66uRtSidsLAXmUHR7
sRzHkgUMPEzzdZ4I4USh_TnNJsT10FPs2y6ar-Zm
WSqoowudcftIjEVkaCO7xFQnBr69n8q72480C3DS
CeTjjgQac39nSo6AMdq_djwoUQBLFQpVkT1wYfrs
Jn2-iZTDNMVDU0zyjS1JyKlo7E0-LxrI14cVf1Tr
MgUg3LDS0hBWyYOPyK36nE1oPEBLuJyUKwVaJI3V
kccbcRBlPu6j4raOH90uDqcIqn3zLauIdsE6vj4_
9_HaA7jeqYGSb7EEz196PnDYJIDkvr394u-Al3FN
rfYWbGk1oJgIrqeShpQNV5nIcKcQCYaEHy5R7kou
t8FFYRVfJRRQQH4zMpTHTzW7u06zusFXsGl0WvDj
7t9cYnJa1LTy8CWd4hs_qfnjt8ipoiUuTI-Mdv3_
5IeXIyh5r8UGpDlNBlhxg2ql-WzpznkhwkDeQs-v
ChdAtSOrl6bIUk2i2ep-VTMZ3Z1ZXGkoX5I-py-o
mq2hdrpJtEWSAZWR7qwyAPEWWQcfel-eNvvhn_ZW
HdlylR0tnTJT3UjB0M-w81pQ1sDZ3P0Ef770Us74
UOdBgG4iLg6A-HIk5tEalO5w4Q4xlAg1GDI1ZcOE
A5VGXam0KsPEGilhEeXgDXAzQqNuJSvToJqjeU7u
6I6zGQDNHYn-BEgq9lTE3onpKMUhoQjKVIrb1LZz
ZcRwtuLyI8JfZaY3r_KGJsDXg6WGYBhAythUuFvY
VT0TRVrvz1dJ70V0g5I4fIkpPRnY4RTlbKBijb4x
zZW9Y_rippRnaTVXsGYhveYS2klXyGNQqjQWkw7i
Mf--e6Fcv6AscHSOX1cO9RpwVT-saiwhaV0M1IZX
mFQRVKl9ajBoPVNpu1OZwSafcYdLlrodVkoVg0h7
kaQDbLVGHsMmDruWk1jEVwmNITzN2o1NqbD3oL1I
gcAc4YZ8--V2-84ANOjcljdxqN1m2SGfqcNEY-Jk
3JyaFwaAFzdvjif6OV0LPXcy70UzlgYpqrd8-3rR
9ejzdN0ONo44HNdPMzmbe1QUVapO3jz9Grqp2Rjo
6amofFqBChCQ</pre></td></tr>
</table>

The display is wrapped to fit. Copyable files: [Factorio string](examples/oil-refining.factorio.txt) · [compact string](examples/oil-refining.compact.txt).

</details>
