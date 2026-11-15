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
    rows = [row for row in json.loads((ROOT / "block-results.json").read_text())
            if row["kind"] == "whole"]
    original = sum(row["native_chars"] for row in rows)
    compact = sum(row["best_chars"] for row in rows)
    lines = ["# Benchmarks", "",
             f"These {len(rows)} public blueprint designs used **{100 * (1 - compact / original):.0f}% less text overall** "
             "after compression. Each name links to its public blueprint page.", "",
             "Sizes below count the characters in each string.", "",
             "| Blueprint | Factorio size | Compact size | Smaller by |",
             "| --- | ---: | ---: | ---: |"]
    for row in rows:
        name = NAMES[row["source_id"]]
        saving = 100 * (1 - row["best_chars"] / row["native_chars"])
        lines.append(f"| [{name}]({row['page']}) | {row['native_chars']:,} | "
                     f"{row['best_chars']:,} | {saving:.0f}% |")
    lines += [f"| **Total** | **{original:,}** | **{compact:,}** | "
              f"**{100 * (1 - compact / original):.0f}%** |", "",
              "The test includes factories, malls, power plants, balancers, and blueprint books. "
              "Results vary with how much repeated data each design contains.", "",
              "The original and restored blueprints produced identical exports in Factorio 2.1.24. "
              "[Accuracy checks](ACCURACY.md)", "",
              "For anyone reproducing the test: [measurements](block-results.csv), "
              "[exact source versions](site-corpus/sources.json), "
              "[test scripts](benchmark_blocks.py).", ""]
    (ROOT / "BENCHMARKS.md").write_text("\n".join(lines))
    print("Wrote BENCHMARKS.md")


if __name__ == "__main__":
    main()
