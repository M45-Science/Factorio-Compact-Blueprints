"""Generate a short benchmark table using linked public blueprint designs."""
import json
import html
from pathlib import Path
import textwrap

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
              "For anyone reproducing the test: [measurements](block-results.csv), "
              "[exact source versions](site-corpus/sources.json), "
              "[test scripts](benchmark_blocks.py).", ""]
    example=json.loads((ROOT/'examples/oil-refining.json').read_text())
    source=(ROOT/'examples/oil-refining.factorio.txt').read_text().strip()
    encoded=(ROOT/'examples/oil-refining.compact.txt').read_text().strip()
    lines += ['## One example', '',
              f"[{example['name']}]({example['source']}) is a mid-sized individual blueprint: "
              f"**{len(source):,} → {len(encoded):,} characters**, or **{len(source)/len(encoded):.1f}:1** "
              '(less than half the original length).', '',
              '<details>', '<summary>Compare the strings side by side</summary>', '',
              '<table>', '<tr><th>Factorio string</th><th>Compact string</th></tr>',
              '<tr><td valign="top"><pre>'+html.escape('\n'.join(textwrap.wrap(source,40,break_on_hyphens=False)))+
              '</pre></td><td valign="top"><pre>'+html.escape('\n'.join(textwrap.wrap(encoded,40,break_on_hyphens=False)))+
              '</pre></td></tr>', '</table>', '',
              'The display is wrapped to fit. Copyable files: '
              '[Factorio string](examples/oil-refining.factorio.txt) · '
              '[compact string](examples/oil-refining.compact.txt).', '', '</details>', '']
    (ROOT / "BENCHMARKS.md").write_text("\n".join(lines))
    print("Wrote BENCHMARKS.md")


if __name__ == "__main__":
    main()
