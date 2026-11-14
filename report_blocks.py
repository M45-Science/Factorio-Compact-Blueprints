"""Report block-sharing results separately from graph/order/palette controls."""
import csv
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).parent


def escape(value):
    return str(value or "(unnamed)").replace("|", "\\|").replace("\n", " ")


def summarize(label, rows):
    old = sum(r["previous_chars"] for r in rows)
    new = sum(r["best_chars"] for r in rows)
    control = sum(r["best_control_chars"] for r in rows)
    return (f"| {label} | {len(rows)} | {old:,} | {new:,} | {100*(1-new/old):.2f}% | "
            f"{100*(1-new/control):.2f}% |")


def main():
    rows = json.loads((ROOT / "block-results.json").read_text())
    baseline = {r["key"]: r for r in json.loads((ROOT / "site-results.json").read_text())}
    assert len(rows) == len(baseline) == 67
    whole = [r for r in rows if r["kind"] == "whole"]
    leaf = [r for r in rows if r["kind"] == "leaf"]
    lines = ["# Repeated-subassembly experiment", "",
             "The codec now supports exact translated blocks within a blueprint and shared block "
             "dictionaries across book pages. The original 67-fixture popular-blueprint corpus and "
             "its ten original encoding candidates were retained as the baseline. Every new mode "
             "is optional; the encoder keeps the previous result whenever the new choices are larger.", "",
             "## Results", "",
             "`Extra reduction` measures the improvement over the previous prototype, not over native "
             "Factorio. `Block modes over controls` compares the final result with the best of the "
             "previous prototype and all new graph, ordering, and shared-settings controls.", "",
             "| Group | Fixtures | Previous chars | Best new chars | Extra reduction | Block modes over controls |",
             "| --- | ---: | ---: | ---: | ---: | ---: |",
             summarize("Complete downloads", whole),
             summarize("Complete books only", [r for r in whole if r["page_count"] > 1]),
             summarize("Individual sampled pages", leaf), "",
             "The block modes help some repeated production lines substantially, but add only a small "
             "aggregate gain over the other new modes. Much of the overall improvement is better "
             "ordering, relative wire references, and a shared settings palette. This experiment "
             "does not establish a limit on what other subassembly algorithms could achieve.", "",
             "## Complete downloads", "",
             "| Design | Previous prototype | Best new | Extra reduction | Native / new | Winning mode |",
             "| --- | ---: | ---: | ---: | ---: | --- |"]
    for r in whole:
        lines.append(f"| [{escape(r['title'])}]({r['page']}) | {r['previous_chars']:,} | "
                     f"{r['best_chars']:,} | {100*(1-r['best_chars']/r['previous_chars']):.2f}% | "
                     f"{r['native_chars']/r['best_chars']:.2f}× | `{r['mode']}` |")
    lines += ["", "## Cumulative controls", "",
              "Each stage keeps the smallest complete string available so far. These aggregates "
              "count complete downloads only. They distinguish improvements accompanying the "
              "subassembly implementation from improvements that need block modes.", "",
              "| Available representations | Combined chars | Extra reduction versus previous prototype |",
              "| --- | ---: | ---: |"]
    allowed = {"j", "s"}
    original = sum(r["previous_chars"] for r in whole)
    for label, additions in (("Previous prototype", set()), ("+ Relative graph references", {"g"}),
                             ("+ Spatial/adaptive ordering", {"o", "a"}),
                             ("+ Shared settings palette", {"p"}),
                             ("+ Local and shared block dictionaries", {"r", "t", "u"})):
        allowed |= additions
        total = sum(min(length for mode, length in r["all_modes"].items() if mode[0] in allowed)
                    for r in whole)
        lines.append(f"| {label} | {total:,} | {100*(1-total/original):.2f}% |")
    lines += ["", "## Implementation", "",
              "`subassemblies.py` matches disjoint spatial cells after translating each cell's "
              "minimum X/Y to the origin. A block is a sequence of entity-settings palette IDs "
              "and relative positions. Its instances carry block ID and translation. Explicit "
              "columns retain the original row permutation, entity numbers, coordinate numeric "
              "types, and negative zero. No entity IDs are discarded or reassigned in the decoded JSON.", "",
              "Local matching tries 37 square, rectangular, and full-axis strip dimensions. "
              "A reuse estimate shortlists three; actual zlib-compressed size, including the "
              "permutation, selects among these and the flat controls per entity/tile array. "
              "A second search tries eight common cell/strip dimensions across the whole book, "
              "including cells unique within one page but repeated on another. Global dictionaries "
              "share both settings and exact blocks. Final complete-string selection tries the "
              "same five compressors used in the original benchmark.", "",
              "Legacy `connections` entity IDs and `neighbours` use typed relative-row references. "
              "Modern blueprint-level wire lists are delta-coded in separate columns. Their "
              "order and endpoint IDs are retained exactly. Modern wire graphs are not yet part "
              "of the reusable block dictionary. Unknown fields and unsupported shapes retain "
              "literal values or use the prior encoding.", "",
              "| Mode | Representation |",
              "| --- | --- |",
              "| `j`, `s` | Previous JSON and structural encodings |",
              "| `g` | Flat columns with relative graph references |",
              "| `o` | Spatially sorted columns plus original-order permutation |",
              "| `a` | Per-array adaptive choice between `g` and `o` |",
              "| `p` | Adaptive flat columns with a book-wide settings palette |",
              "| `r` | Per-array adaptive local block dictionary |",
              "| `t` | Book-wide sharing of the locally selected blocks/settings |",
              "| `u` | Book-wide block search, including cross-page-only repeats |", "",
              "The controls do not freeze each block mode's exact cell traversal while removing "
              "only its dictionary: different spatial orders can contribute to the block-mode "
              "gain. Thus `block modes over controls` is an incremental transport comparison, "
              "not a perfectly isolated estimate of dictionary deduplication alone.", "",
              "## Validation and limits", "",
              f"All **{sum(r['roundtrip_candidates'] for r in rows):,} new encoding candidates across "
              f"{len(rows)} fixtures** reconstructed identical parsed JSON, including numeric types "
              "and signed zero. The 670 original candidates remain in the frozen baseline results. "
              "Twelve unit tests cover mixed-entity repeated blocks, arbitrary entity order, sparse "
              "IDs, internal and external references, global wires, mod fields, translated pages "
              "with different IDs, nested books, tiles, numeric precision, and random layouts. "
              "No string was imported into a running Factorio instance during that initial run. "
              "See [the accuracy audit](ACCURACY.md) for subsequent game-import validation.", "",
              "The matcher handles exact translations, not rotations, reflections, approximate "
              "matches, or block-plus-exception patches. Cell sizes are heuristic and their phases "
              "are not searched. Original-order permutations and instance/dictionary overhead can "
              "outweigh the savings, particularly when the earlier compressor already captures "
              "the repetition. The source sampling limits and overlap between whole books and "
              "sampled pages remain those in `SITE_RESULTS.md`.", "",
              "The decoder remains a trusted-input research tool; the extra search and compressor "
              "candidates also increase encoding cost. `BX0:` is still experimental.", "",
              "## Reproduce", "", "```sh",
              "python3 -m unittest -v test_compact.py test_subassemblies.py",
              "python3 benchmark_blocks.py", "python3 report_blocks.py", "```", "",
              "`site-results.json` remains the frozen previous-prototype baseline. The block "
              "benchmark resumes from `block-results.json` and rejects an implementation-fingerprint "
              "mismatch; move that file aside before changing encoder code and rerunning. "
              "`block-summary.json` holds aggregates and `block-results.csv` holds a flat table. "
              "`block-local-results.json` and `block-local-summary.json` retain the initial "
              "within-page-only experiment.", "",
              "## Sampled individual pages", "",
              "| Source | Page | Previous | Best new | Extra reduction | Winner |",
              "| --- | --- | ---: | ---: | ---: | --- |"]
    for r in leaf:
        lines.append(f"| [{escape(r['title'])}]({r['page']}) | {escape(r.get('leaf_title'))} | "
                     f"{r['previous_chars']:,} | {r['best_chars']:,} | "
                     f"{100*(1-r['best_chars']/r['previous_chars']):.2f}% | `{r['mode']}` |")
    (ROOT / "BLOCK_RESULTS.md").write_text("\n".join(lines) + "\n")
    fields = ["key", "kind", "title", "leaf_title", "page", "native_chars", "previous_chars",
              "best_control_chars", "motif_chars", "best_chars", "mode", "seconds", "roundtrip_candidates"]
    with (ROOT / "block-results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote BLOCK_RESULTS.md and block-results.csv")


if __name__ == "__main__":
    main()
