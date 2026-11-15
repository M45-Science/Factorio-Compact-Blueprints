"""Generate a short benchmark table using linked public blueprint designs."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

NAMES = {
    "-MIMpsZJa9WHxI4H6fcD": "Nilaus Master Class",
    "-ML5RsMXhj7tnbbzs02H": "Raynquist Belt Balancers",
    "-Ln7bpxs1Mmtyv9yx8x5": "Nauvis Space Age Mall",
    "-MQ9-6LlT_g5PGsGXkyX": "Little Witch Nuclear Plant",
    "-K_Me61B1oQ_Dmjbde9B": "All the Inserters",
    "-Kp6dxRcQbpr7UrzJC6x": "Plastic and Sulfuric Acid",
    "-LrxBIuzRGB9jKLgPRqH": "Nilaus Base-in-a-Book (0.17)",
    "-OX4QBKmwEZ6dIBJY5C5": "Fulgora Mall",
    "-OFo0h6eKudNzNzkh9zL": "GSXR Automatic Mall",
    "-OL_E6IO4gmQUdqFgTjq": "Space Platform Factory",
    "-OBdq3vJ2slIWEDAXEeM": "Tileable Factories",
    "-LI0gc-a-2_VLWR-tx1d": "Nilaus Base-in-a-Book",
    "-MK-xIWwMHTIBuSh3ZWQ": "ElderAxe Quick Start Base",
}


def main():
    rows = [row for row in json.loads((ROOT / "optimized-results.json").read_text())
            if row["kind"] == "whole"]
    assert len(rows) == 13, "expected all 13 complete public designs"
    original = sum(row["native_chars"] for row in rows)
    compact = sum(row["best_chars"] for row in rows)
    lines = ["# Benchmarks", "",
             f"These {len(rows)} public blueprint designs used **{100 * (1 - compact / original):.0f}% less text overall** "
             f"after compression: about {original/compact:.0f}:1, or roughly one-fifth the original length. "
             "Each name links to its public blueprint page.", "",
             "Sizes below count the characters in each string.", "",
             "| Blueprint | Factorio size | Compact size | Smaller by | Ratio |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for row in rows:
        name = NAMES[row["source_id"]]
        saving = 100 * (1 - row["best_chars"] / row["native_chars"])
        lines.append(f"| [{name}]({row['page']}) | {row['native_chars']:,} | "
                     f"{row['best_chars']:,} | {saving:.0f}% | {row['native_chars']/row['best_chars']:.1f}:1 |")
    lines += [f"| **Total** | **{original:,}** | **{compact:,}** | "
              f"**{100 * (1 - compact / original):.0f}%** | **{original/compact:.1f}:1** |", "",
              "Ratios compare Factorio size to compact size: 5:1 means the compact string is one-fifth as long.", "",
              "The test includes factories, malls, power plants, balancers, and blueprint books. "
              "Results vary with how much repeated data each design contains.", "",
              "The original and restored blueprints produced identical exports in Factorio 2.1.24. "
              "[Accuracy checks](ACCURACY.md)", "",
              "For anyone reproducing the test: [measurements](optimized-results.csv), "
              "[exact source versions](site-corpus/sources.json), "
              "[test scripts](benchmark_optimized.py).", ""]
    example=json.loads((ROOT/'examples/master-class.json').read_text())
    source=(ROOT/'examples/master-class.factorio.txt').read_text().strip()
    encoded=(ROOT/'examples/master-class.compact.txt').read_text().strip()
    measurement=next(row for row in rows if row['key']==example['key'])
    assert len(encoded)==measurement['best_chars']==example['compact_chars']
    assert len(source)==measurement['native_chars']==example['original_chars']
    lines += ['## One example', '',
              f"[{example['name']}]({example['source']}) is a blueprint book: "
              f"**{len(source):,} → {len(encoded):,} characters**, or **{len(source)/len(encoded):.1f}:1** "
              '(about one-fifth the original length).', '',
              'Full strings: [Factorio string](examples/master-class.factorio.txt) · '
              '[compact string](examples/master-class.compact.txt).', '']
    (ROOT / "BENCHMARKS.md").write_text("\n".join(lines))
    print("Wrote BENCHMARKS.md")


if __name__ == "__main__":
    main()
