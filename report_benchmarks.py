"""Build the detailed benchmark page from linked public-blueprint measurements."""
import json
from pathlib import Path
import statistics
from urllib.parse import urlencode

ROOT = Path(__file__).parent


def escape(text):
    return str(text or "(unnamed)").replace("|", "\\|").replace("\n", " ")


def group(label, rows):
    native = sum(r["native_chars"] for r in rows)
    best = sum(r["best_chars"] for r in rows)
    median = statistics.median(r["native_chars"] / r["best_chars"] for r in rows)
    return f"| {label} | {len(rows)} | {native:,} | {best:,} | {native/best:.2f}× | {median:.2f}× |"


def main():
    rows = json.loads((ROOT / "block-results.json").read_text())
    previous = {r["key"]: r for r in json.loads((ROOT / "site-results.json").read_text())}
    sources = {r["id"]: r for r in json.loads((ROOT / "site-corpus/sources.json").read_text())}
    assert len(rows) == len(previous) == 67
    whole = [r for r in rows if r["kind"] == "whole"]
    leaves = [r for r in rows if r["kind"] == "leaf"]
    lines = ["# Benchmarks", "",
             "All reported performance measurements on this page use **public gameplay blueprints**. "
             "There are no generated grids or image-art blueprints in this benchmark. Every design "
             "is linked to its public page; pinned source records and hashes allow the exact "
             "measured versions to be fetched even if a live page changes.", "",
             "## Results", "",
             "Lengths count every copied ASCII character, including prefixes. Native means compact "
             "blueprint JSON compressed with zlib level 9, padded Base64, and the `0` prefix. "
             "The new transport selects the shortest candidate. A larger factor means less text.", "",
             "| Group | Fixtures | Native chars | Transport chars | Combined reduction factor | Median factor |",
             "| --- | ---: | ---: | ---: | ---: | ---: |",
             group("Complete public downloads", whole),
             group("Complete books only", [r for r in whole if r["page_count"] > 1]),
             group("Sampled individual pages", leaves), "",
             "The complete downloads are nine books and four individual blueprints. Sampled pages "
             "also occur inside their books, so these groups overlap and must not be added together. "
             "Combined-size factors weight large files more heavily; the median reports each "
             "fixture's reduction factor with equal weight.", "",
             "## Complete public blueprints and books", "",
             "Each title opens the public design page. The pinned source record contains the exact "
             "blueprint string used in the measurement. `Previous` is the earlier structural "
             "prototype; `Transport` includes all current modes.", "",
             "| Public design | Pinned record | Pages | Native | Previous | Transport | Native / transport | Extra reduction |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in whole:
        s = sources[r["source_id"]]
        lines.append(f"| [{escape(r['title'])}]({r['page']}) | [source]({s['download']}) | "
                     f"{r['page_count']} | {r['native_chars']:,} | {r['previous_chars']:,} | "
                     f"{r['best_chars']:,} | {r['native_chars']/r['best_chars']:.2f}× | "
                     f"{100*(1-r['best_chars']/r['previous_chars']):.2f}% |")
    lines += ["", "## What produces the savings", "",
              "Each stage below keeps the smallest complete string seen so far. These totals "
              "cover the 13 complete downloads and separate explicit block modes from the "
              "accompanying wire, ordering, and shared-settings improvements.", "",
              "| Available representations | Total chars | Extra reduction from previous prototype |",
              "| --- | ---: | ---: |"]
    allowed = {"j", "s"}
    old = sum(r["previous_chars"] for r in whole)
    for label, additions in (("Previous structural prototype", set()),
                             ("+ Relative wire references", {"g"}),
                             ("+ Spatial/adaptive ordering", {"o", "a"}),
                             ("+ Shared settings palette", {"p"}),
                             ("+ Local and shared block dictionaries", {"r", "t", "u"})):
        allowed |= additions
        total = sum(min(n for m, n in r["all_modes"].items() if m[0] in allowed) for r in whole)
        lines.append(f"| {label} | {total:,} | {100*(1-total/old):.2f}% |")
    native = sum(r["native_chars"] for r in whole)
    best = sum(r["best_chars"] for r in whole)
    control = sum(r["best_control_chars"] for r in whole)
    raw_json = sum(previous[r["key"]]["best_json_chars"] for r in whole)
    zlib = sum(previous[r["key"]]["structure_zlib_chars"] for r in whole)
    lines += ["",
              f"All new modes together save **{100*(1-best/old):.2f}%** beyond the previous prototype. "
              f"Explicit block modes add **{100*(1-best/control):.2f}%** beyond the other controls. "
              "That incremental comparison can also include differences in cell traversal order; "
              "it is not a perfectly isolated estimate of dictionary deduplication alone.", "",
              f"For context, the original representation change with zlib alone totaled {zlib:,} "
              f"characters ({native/zlib:.2f}× smaller than native). Stronger compression of unchanged "
              f"JSON totaled {raw_json:,} characters. Current transport totals {best:,}. Thus the "
              "measured savings are not solely from changing compressors.", "",
              "## Sources and sampling", "",
              "The 16 site posts were chosen by visible title, category, and favorites before "
              "compression was measured. They cover malls, starter bases, production lines, "
              "nuclear power, oil, balancers, rail systems, circuits, and Space Age designs. "
              "This is a convenience sample, not a random sample or a global popularity ranking. "
              "It includes two related versions of Base-in-a-Book.", "",
              "The bytes come from the public [Factorio Prints mirror]"
              "(https://github.com/motlin/factorio-blueprint-firebase-cdn), pinned at "
              "`1868b1efafa5e6603c42279974d292905ee8c82b`. Direct website downloads were unavailable "
              "in the measurement environment. The [source manifest](site-corpus/sources.json) "
              "records public pages, exact downloads, hashes, and snapshot metadata.", "",
              "Complete downloads are measured up to 100,000 entity+tile placements. Three larger "
              "books are represented through sampled pages: Space Age Rail Blocks, Space Age "
              "Blueprints, and Nilaus Cityblock 2.0. For each multi-page book, pages with at least "
              "20 placements are sorted by placement count and array path. The smallest, 25th-percentile, "
              "median, 75th-percentile, and largest ranks are selected. Identical parsed-JSON pages "
              "are deduplicated across books, leaving 54 sampled pages.", "",
              "| Public source post | Exact measured source record | Coverage |",
              "| --- | --- | --- |"]
    for id, s in sources.items():
        measured = [r for r in rows if r["source_id"] == id]
        coverage = ("Complete download; " if any(r["kind"] == "whole" for r in measured) else "")
        coverage += f"{sum(r['kind']=='leaf' for r in measured)} sampled pages"
        lines.append(f"| [{escape(s['title'])}]({s['page']}) | [pinned source]({s['download']}) | {coverage} |")
    lines += ["", "## Validation and encoding settings", "",
              "All 3,015 candidates across these 67 fixtures reproduce identical parsed JSON, "
              "including numeric types and signed zero. The game audit compared all 67 original "
              "and reconstructed imports in Factorio 2.1.24 and found identical exports. Six "
              "pairs shared the same pre-existing import-error status. See the "
              "[accuracy audit](ACCURACY.md) for evidence and limits.", "",
              "Each representation tries uncompressed, zlib-9, Brotli-11, Zstandard-19, and LZMA-9. "
              "`site-results.json` records the ten earlier candidates; `block-results.json` adds "
              "35 graph/order/palette/block candidates. The current total is 45 candidates per "
              "fixture. Candidate search is more CPU-intensive than native export. Compressor "
              "versions are pinned in `requirements.txt`.", "",
              "The block matcher searches exact translated spatial cells and strips. It preserves "
              "original row order through explicit permutations. It does not search rotations, "
              "reflections, or approximate blocks with exceptions. Modern wire lists are encoded "
              "separately. [Detailed encoding controls](BLOCK_RESULTS.md#implementation)", "",
              "## Reproduce", "", "```sh", "python3 -m venv .venv", ". .venv/bin/activate",
              "python3 -m pip install -r requirements.txt", "python3 -m unittest discover -v",
              "python3 fetch_site_corpus.py", "python3 benchmark_sites.py", "python3 benchmark_blocks.py",
              "python3 report_benchmarks.py", "python3 audit.py --game-pairs /tmp/blueprint-import-pairs.json",
              "# Optional: requires a local Factorio installation with expansion data",
              "python3 test_factorio.py /path/to/factorio/bin/x64/factorio /tmp/blueprint-import-pairs.json",
              "```", "",
              "Benchmark scripts resume from saved JSON results. Move `site-results.json` and/or "
              "`block-results.json` aside to recompute them; preserve the former to retain the "
              "previous-prototype baseline. The block script rejects a changed implementation "
              "fingerprint. Downloaded community strings stay local; only links, hashes, and "
              "measurements are committed. Synthetic examples and unit fixtures do not contribute "
              "to these performance totals.", "",
              "Raw data: [baseline CSV](site-results.csv), [current CSV](block-results.csv), "
              "[baseline JSON](site-results.json), [current JSON](block-results.json). "
              "Earlier analyses: [structural comparison](SITE_RESULTS.md), "
              "[repeated-block comparison](BLOCK_RESULTS.md).", "",
              "## Sampled public blueprint pages", "",
              "The page links open the corresponding page in its public book. Array paths "
              "identify the exact measured page; source hashes identify the book snapshot.", "",
              "| Public page | Book | Array path | Native | Transport | Smaller |",
              "| --- | --- | --- | ---: | ---: | ---: |"]
    for r in leaves:
        path = "/".join(map(str, r["leaf_path"]))
        link = sources[r["source_id"]]["atlas_page"] + "?" + urlencode({"page": path})
        lines.append(f"| [{escape(r.get('leaf_title'))}]({link}) | [{escape(r['title'])}]({r['page']}) | "
                     f"`{path}` | {r['native_chars']:,} | {r['best_chars']:,} | "
                     f"{r['native_chars']/r['best_chars']:.2f}× |")
    (ROOT / "BENCHMARKS.md").write_text("\n".join(lines) + "\n")
    print("Wrote BENCHMARKS.md with links for all 16 public sources and 54 sampled pages")


if __name__ == "__main__":
    main()
