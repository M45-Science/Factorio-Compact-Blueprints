"""Benchmark whole site downloads and deterministic, deduplicated book samples."""
import hashlib
import json
from pathlib import Path
import statistics
import time

from compact import candidates, decode, native_decode, native_encode

ROOT = Path(__file__).parent


def leaves(node, path=()):
    if "blueprint" in node:
        yield path, {"blueprint": node["blueprint"]}
    for i, child in enumerate(node.get("blueprint_book", {}).get("blueprints", [])):
        yield from leaves(child, path + (i,))


def size(value):
    bp = value.get("blueprint", {})
    return len(bp.get("entities", [])) + len(bp.get("tiles", []))


def serialized(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def fixtures():
    seen = set()
    for source in json.loads((ROOT / "site-corpus/sources.json").read_text()):
        text = (ROOT / "site-corpus" / source["file"]).read_text().strip()
        value = native_decode(text)
        pages = list(leaves(value))
        placements = sum(size(v) for _, v in pages)
        base = {"source_id": source["id"], "title": source["title"], "favorites": source["favorites"],
                "page": source["page"], "source_sha256": source["sha256"]}
        if placements <= 100000:
            yield dict(base, kind="whole", key=source["id"] + "/whole", source_chars=len(text),
                       page_count=len(pages)), value
        else:
            print("Sampling only (>100,000 placements):", source["title"], placements, flush=True)
        if len(pages) <= 1:
            continue
        eligible = sorted(((path, v) for path, v in pages if size(v) >= 20),
                          key=lambda pair: (size(pair[1]), pair[0]))
        if not eligible:
            continue
        ranks = sorted({round(i * (len(eligible) - 1) / 4) for i in range(5)})
        for rank in ranks:
            path, v = eligible[rank]
            digest = hashlib.sha256(serialized(v).encode()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            yield dict(base, kind="leaf", key=source["id"] + "/" + "/".join(map(str, path)),
                       leaf_path=list(path), leaf_title=v["blueprint"].get("label"),
                       rank=rank, eligible_pages=len(eligible), page_count=1), v


def summary(rows):
    result = {}
    for kind in ("whole", "leaf"):
        selected = [r for r in rows if r["kind"] == kind]
        if not selected:
            continue
        ratios = [r["native_chars"] / r["best_chars"] for r in selected]
        native = sum(r["native_chars"] for r in selected)
        best = sum(r["best_chars"] for r in selected)
        json_only = sum(r["best_json_chars"] for r in selected)
        zlib_only = sum(r["structure_zlib_chars"] for r in selected)
        result[kind] = {"count": len(selected), "median_ratio": statistics.median(ratios),
                        "min_ratio": min(ratios), "max_ratio": max(ratios),
                        "total_native_chars": native, "total_best_chars": best,
                        "aggregate_ratio": native / best, "aggregate_reduction_pct": 100 * (1 - best / native),
                        "best_json_chars": json_only, "structure_vs_best_json_ratio": json_only / best,
                        "structure_zlib_chars": zlib_only, "zlib_aggregate_ratio": native / zlib_only}
    return result


def main():
    output = ROOT / "site-results.json"
    rows = json.loads(output.read_text()) if output.exists() else []
    done = {r["key"] for r in rows}
    for fixture, value in fixtures():
        if fixture["key"] in done:
            continue
        print("Testing", fixture["kind"], fixture.get("leaf_title") or fixture["title"], flush=True)
        start = time.monotonic()
        # Keep the original experiment frozen for before/after comparisons.
        options = candidates(value, repeated=False)
        expected = serialized(value)
        for mode, text in options.items():
            assert serialized(decode(text)) == expected, (fixture["key"], mode)
        mode, best = min(options.items(), key=lambda item: len(item[1]))
        native = len(native_encode(value))
        pages = list(leaves(value))
        row = dict(fixture, native_chars=native, best_chars=len(best), mode=mode,
                   best_json_chars=min(len(t) for m, t in options.items() if m.startswith("j/")),
                   structure_zlib_chars=len(options["s/d"]),
                   entities=sum(len(v["blueprint"].get("entities", [])) for _, v in pages),
                   tiles=sum(len(v["blueprint"].get("tiles", [])) for _, v in pages),
                   all_modes={m: len(t) for m, t in options.items()},
                   seconds=round(time.monotonic() - start, 3), roundtrip_candidates=len(options))
        rows.append(row)
        output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
        print(f'  {native:,} -> {len(best):,}, {native / len(best):.2f}x, {row["seconds"]}s', flush=True)
    result = summary(rows)
    (ROOT / "site-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
