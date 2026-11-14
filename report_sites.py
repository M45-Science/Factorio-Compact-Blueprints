"""Generate the reviewable results table from saved benchmark measurements."""
import csv
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).parent


def esc(text):
    return str(text or "(unnamed)").replace("|", "\\|").replace("\n", " ")


def group_row(label, rows):
    ratios = [r["native_chars"] / r["best_chars"] for r in rows]
    return (f"| {label} | {len(rows)} | {statistics.median(ratios):.2f}× | "
            f"{sum(r['native_chars'] for r in rows) / sum(r['best_chars'] for r in rows):.2f}× |")


def main():
    rows = json.loads((ROOT / "site-results.json").read_text())
    sources = json.loads((ROOT / "site-corpus/sources.json").read_text())
    whole = [r for r in rows if r["kind"] == "whole"]
    leaves = [r for r in rows if r["kind"] == "leaf"]
    lines = ["# Popular blueprint-site benchmark", "",
             "The unchanged codec was tested against 16 curated public site posts, spanning "
             "balancers, malls, starter bases, nuclear power, oil processing, rail blocks, "
             "circuit-controlled production, and Space Age designs. No synthetic layouts or image "
             "blueprints are included in these results.", "",
             "## Findings", "",
             "| Group | Fixtures | Median reduction factor | Combined-size reduction factor |",
             "| --- | ---: | ---: | ---: |",
             group_row("Individual pages sampled from books", leaves),
             group_row("Entity-led sampled pages (entities > tiles)", [r for r in leaves if r["entities"] > r["tiles"]]),
             group_row("Tile-led sampled pages", [r for r in leaves if r["entities"] <= r["tiles"]]),
             group_row("Complete books", [r for r in whole if r["page_count"] > 1]),
             group_row("Single-blueprint site posts", [r for r in whole if r["page_count"] == 1]),
             group_row("All complete site downloads", whole), ""]
    n = sum(r["native_chars"] for r in whole)
    b = sum(r["best_chars"] for r in whole)
    j = sum(r["best_json_chars"] for r in whole)
    d = sum(r["structure_zlib_chars"] for r in whole)
    lines += [f"Complete downloads totaled **{n:,} native characters → {b:,} prototype characters**, "
              f"a **{100 * (1 - b/n):.1f}%** reduction. Keeping zlib level 9 and only changing the representation "
              f"gave **{n/d:.2f}×** reduction. The best JSON-only modern-compressor candidates totaled "
              f"{j:,} characters; structural encoding was another **{j/b:.2f}×** smaller than those.", "",
              "The practical result is roughly 2× for a median individual gameplay page, with larger "
              "gains for books and regular layouts. Large tile patterns create the extreme outliers; "
              "they should not be treated as typical production blueprints.", "",
              "## Complete downloads", "",
              "Native sizes below use consistent zlib-9 re-encoding of the site's parsed JSON. "
              "The exact downloaded string length is also recorded; one site's older string was "
              "larger than its re-encoded baseline.", "",
              "| Source | Favorites | Pages | Downloaded | Native baseline | Prototype | Smaller | Structured + zlib |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in whole:
        lines.append(f"| [{esc(r['title'])}]({r['page']}) | {r['favorites']:,} | {r['page_count']} | "
                     f"{r['source_chars']:,} | {r['native_chars']:,} | {r['best_chars']:,} | "
                     f"{r['native_chars']/r['best_chars']:.2f}× | {r['structure_zlib_chars']:,} |")
    lines += ["", "## Sampling and provenance", "",
              "Designs were selected by visible title, category, and favorites before compression was "
              "measured. Discovery used Factorio Blueprints, Factorio Prints/School, Blueprint Atlas, "
              "and FactorioBin. Direct HTTP downloads from those sites returned access errors in this "
              "environment. The tested bytes were therefore downloaded from the public "
              "[Factorio Prints mirror](https://github.com/motlin/factorio-blueprint-firebase-cdn), "
              "pinned to commit `1868b1efafa5e6603c42279974d292905ee8c82b`. These are Factorio Prints "
              "site posts; this run does not claim independent downloads from every discovery site.", "",
              "This is a varied convenience sample, not the global top 16, a random sample, or a "
              "cross-site popularity ranking. Mirror favorite counts range from 10 to 2,589; "
              "lower-favorite modern/circuit examples were included for variety. Counts may differ "
              "from indexed website pages because snapshots have different dates. The set also "
              "includes two versions of Base-in-a-Book, so the complete-book aggregate contains "
              "correlated designs.", "",
              "A complete site download is tested if it contains at most 100,000 entity+tile placements. "
              "Three larger books (Space Age Rail Blocks, Space Age Blueprints, and Nilaus Cityblock 2.0) "
              "were tested through sampled pages only. Within each multi-page book, pages with at "
              "least 20 placements are sorted by placement count (then array path). The smallest, "
              "25th-percentile, median, 75th-percentile, and largest ranks are selected. Identical "
              "parsed-JSON leaf pages are deduplicated across books, yielding 54 sampled pages. "
              "These pages also occur inside the whole books; the two groups must not be pooled "
              "as independent observations. This sampling favors size coverage and can include "
              "large tile-only pages and instructional pages.", "",
              f"All **{sum(r['roundtrip_candidates'] for r in rows)} encoding candidates across "
              f"{len(rows)} fixtures** passed exact parsed-JSON reconstruction, including numeric "
              "types and signed zero. The pre-existing five unit tests also passed. The codec was "
              "not changed for these measurements. No restored string was imported into a running "
              "Factorio instance during that initial run. See [the accuracy audit](ACCURACY.md) "
              "for subsequent game-import validation.", "",
              "All lengths count copied ASCII characters including prefixes. Native baseline: compact "
              "JSON, zlib level 9, padded Base64, `0` prefix. Prototype: best of uncompressed, zlib-9, "
              "Brotli-11, Zstandard-19, and LZMA-9, tried on both JSON and structural MessagePack, "
              "with `BX0:` header and unpadded Base64URL. Selecting the smallest of these is "
              "computationally more expensive than native export. No external dictionary is used.", "",
              "## Reproduce", "", "```sh", "python3 fetch_site_corpus.py", "python3 benchmark_sites.py",
              "python3 report_sites.py", "```", "",
              "The benchmark resumes from `site-results.json`. Remove that file to rerun measurements "
              "after changing codec code or the corpus. Source hashes, exact download URLs, favorites, "
              "tags, and source titles are in `site-corpus/sources.json`. Per-candidate lengths, "
              "timings, entity/tile counts, and book paths are in `site-results.json`; aggregates are "
              "in `site-summary.json`. A flat table is in `site-results.csv`.", "",
              "## Sampled individual pages", "",
              "| Source | Page | Entities | Tiles | Native | Prototype | Smaller |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in leaves:
        name = r.get("leaf_title") or "(unnamed)"
        lines.append(f"| [{esc(r['title'])}]({r['page']}) | {esc(name)} | {r['entities']:,} | "
                     f"{r['tiles']:,} | {r['native_chars']:,} | {r['best_chars']:,} | "
                     f"{r['native_chars']/r['best_chars']:.2f}× |")
    (ROOT / "SITE_RESULTS.md").write_text("\n".join(lines) + "\n")
    fields = ["key", "kind", "title", "leaf_title", "favorites", "page", "page_count", "entities", "tiles",
              "source_chars", "native_chars", "best_chars", "best_json_chars", "structure_zlib_chars", "mode", "seconds"]
    with (ROOT / "site-results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote SITE_RESULTS.md and site-results.csv")


if __name__ == "__main__":
    main()
