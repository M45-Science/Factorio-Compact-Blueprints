"""Recompute the frozen site measurements and optionally prepare game imports."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time

from benchmark_blocks import fingerprint, summarize
from benchmark_sites import fixtures, serialized, summary
from compact import candidates, decode, native_encode

ROOT = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-pairs", type=Path, help="Write temporary native import pairs (not for publication)")
    args = parser.parse_args()
    old_rows = json.loads((ROOT / "site-results.json").read_text())
    new_rows = json.loads((ROOT / "block-results.json").read_text())
    previous = {r["key"]: r for r in old_rows}
    blocks = {r["key"]: r for r in new_rows}
    if len(previous) != 67 or len(blocks) != 67:
        raise AssertionError("expected all 67 fixtures")
    for source in json.loads((ROOT / "site-corpus/sources.json").read_text()):
        text = (ROOT / "site-corpus" / source["file"]).read_text().strip()
        assert hashlib.sha256(text.encode()).hexdigest() == source["sha256"], source["id"]
    assert summary(old_rows) == json.loads((ROOT / "site-summary.json").read_text())
    assert summarize(new_rows) == json.loads((ROOT / "block-summary.json").read_text())
    total = 0
    pairs = []
    started = time.monotonic()
    for i, (fixture, value) in enumerate(fixtures(), 1):
        key = fixture["key"]
        old, new = previous[key], blocks[key]
        assert new["implementation_sha256"] == fingerprint(), "encoder differs from measured implementation"
        assert old["source_sha256"] == new["source_sha256"] == fixture["source_sha256"]
        options = candidates(value)
        assert set(options) == set(new["all_modes"])
        expected = serialized(value)
        for mode, text in options.items():
            assert len(text) == new["all_modes"][mode], (key, mode, "changed measurement")
            assert serialized(decode(text)) == expected, (key, mode, "round-trip mismatch")
            if mode in old["all_modes"]:
                assert len(text) == old["all_modes"][mode]
        winner = min(options, key=lambda mode: len(options[mode]))
        assert len(options[winner]) == new["best_chars"]
        assert len(native_encode(value)) == new["native_chars"]
        pairs.append({"key": key, "original": native_encode(value),
                      "restored": native_encode(decode(options[winner])), "mode": winner})
        total += len(options)
        print(f"{i}/67 {key}: {len(options)} round trips and saved lengths verified", flush=True)
    assert len(pairs) == 67
    if args.game_pairs:
        args.game_pairs.write_text(json.dumps(pairs))
    result = {"fixtures": len(pairs), "candidate_roundtrips": total,
              "all_saved_lengths_match": True, "source_hashes_match": True,
              "aggregate_summaries_match": True, "implementation_sha256": fingerprint(),
              "packages": {p: importlib.metadata.version(p) for p in ("msgpack", "Brotli", "zstandard")},
              "seconds": round(time.monotonic() - started, 3)}
    (ROOT / "audit-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
