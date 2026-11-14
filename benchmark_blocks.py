"""Compare new motif modes against the frozen popular-blueprint measurements."""
import hashlib
import json
from pathlib import Path
import statistics
import time

from benchmark_sites import fixtures, serialized
from compact import COMPRESS, decode, pack, printable
from subassemblies import representations

ROOT = Path(__file__).parent


def fingerprint():
    return hashlib.sha256(b"".join((ROOT / name).read_bytes() for name in
                                  ("compact.py", "subassemblies.py", "benchmark_blocks.py"))).hexdigest()


def summarize(rows):
    summary = {}
    for kind in ("whole", "leaf"):
        selected = [r for r in rows if r["kind"] == kind]
        old = sum(r["previous_chars"] for r in selected)
        best = sum(r["best_chars"] for r in selected)
        controls = sum(r["best_control_chars"] for r in selected)
        native = sum(r["native_chars"] for r in selected)
        summary[kind] = {"count": len(selected), "previous_chars": old, "best_chars": best,
                         "extra_reduction_pct": 100 * (1 - best / old), "native_ratio": native / best,
                         "median_extra_reduction_pct": statistics.median(
                             100 * (1 - r["best_chars"] / r["previous_chars"]) for r in selected),
                         "control_chars": controls, "motif_extra_over_controls_pct": 100 * (1 - best / controls),
                         "improved_fixtures": sum(r["best_chars"] < r["previous_chars"] for r in selected),
                         "motif_wins_over_controls": sum(r["motif_chars"] < r["best_control_chars"] and
                                                        bool(r["motifs"]) for r in selected)}
    return summary


def main():
    baseline = {r["key"]: r for r in json.loads((ROOT / "site-results.json").read_text())}
    output = ROOT / "block-results.json"
    rows = json.loads(output.read_text()) if output.exists() else []
    digest = fingerprint()
    if any(r["implementation_sha256"] != digest for r in rows):
        raise RuntimeError("Implementation changed; move block-results.json aside before rerunning")
    done = {r["key"] for r in rows}
    for fixture, value in fixtures():
        if fixture["key"] in done:
            continue
        previous = baseline[fixture["key"]]
        assert fixture["source_sha256"] == previous["source_sha256"]
        print("Testing", fixture["kind"], fixture.get("leaf_title") or fixture["title"], flush=True)
        start = time.monotonic()
        forms, stats = representations(value, with_stats=True)
        options = {f"{form}/{codec}": "BX0:" + form + codec + printable(compress(pack(payload)))
                   for form, payload in forms.items() for codec, compress in COMPRESS.items()}
        expected = serialized(value)
        for mode, text in options.items():
            assert serialized(decode(text)) == expected, (fixture["key"], mode)
        lengths = {mode: len(text) for mode, text in options.items()}
        all_lengths = dict(previous["all_modes"], **lengths)
        mode, best = min(all_lengths.items(), key=lambda kv: kv[1])
        block_forms = {"r", "t", "u"}
        control = min(length for mode, length in all_lengths.items() if mode[0] not in block_forms)
        motif = min(length for mode, length in lengths.items() if mode[0] in block_forms)
        row = dict(fixture, implementation_sha256=digest, previous_chars=previous["best_chars"],
                   native_chars=previous["native_chars"], best_chars=best, mode=mode,
                   best_control_chars=control, motif_chars=motif, motifs=stats,
                   new_modes=lengths, all_modes=all_lengths, roundtrip_candidates=len(options),
                   seconds=round(time.monotonic() - start, 3))
        rows.append(row)
        output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
        print(f'  {row["previous_chars"]:,} -> {best:,} '
              f'({100*(1-best/row["previous_chars"]):.1f}% extra), '
              f'control {control:,}, motif {motif:,}, {mode}, '
              f'{len(stats)} motif tables, {row["seconds"]}s', flush=True)
    summary = summarize(rows)
    (ROOT / "block-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
