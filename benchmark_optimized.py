"""Measure dictionary sharing on the same linked public-blueprint corpus."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from benchmark_sites import fixtures, serialized
from compact import candidates, decode, native_encode

ROOT = Path(__file__).parent


def fingerprint():
    return hashlib.sha256(b"".join((ROOT/name).read_bytes() for name in
                                  ("compact.py", "subassemblies.py", "interning.py",
                                   "benchmark_optimized.py"))).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lua-cases", type=Path, help="Write temporary interoperability inputs")
    args = parser.parse_args()
    old = {r["key"]: r for r in json.loads((ROOT/"block-results.json").read_text())}
    output = ROOT/"optimized-results.json"
    rows = json.loads(output.read_text()) if output.exists() else []
    digest = fingerprint()
    if any(r["implementation_sha256"] != digest for r in rows):
        raise RuntimeError("Move optimized-results.json aside before changing the measured implementation")
    done = {r["key"] for r in rows}
    cases = []
    for fixture, value in fixtures():
        key = fixture["key"]
        # An explicit cases request rechecks all frames, even on a cached run.
        if key in done and not args.lua_cases:
            continue
        start = time.monotonic()
        options = candidates(value, interned=True)
        expected = serialized(value)
        for mode, text in options.items():
            assert serialized(decode(text)) == expected, (key, mode)
        mode, best = min(options.items(), key=lambda pair: len(pair[1]))
        portable = min((t for m, t in options.items() if m.endswith(("/n", "/d"))), key=len)
        row = dict(fixture, implementation_sha256=digest, native_chars=len(native_encode(value)),
                   previous_chars=old[key]["best_chars"], best_chars=len(best), mode=mode,
                   portable_chars=len(portable), all_modes={m: len(t) for m, t in options.items()},
                   roundtrip_candidates=len(options), seconds=round(time.monotonic()-start, 3))
        if key not in done:
            rows.append(row)
            output.write_text(json.dumps(rows, indent=2, ensure_ascii=False)+"\n")
        if args.lua_cases:
            cases.append(dict(key=key, original=native_encode(value), portable=portable,
                              decodes=[t for m, t in options.items() if m.endswith("/d")]))
        print(f"{len(rows)}/67 {key}: {row['previous_chars']:,} -> {len(best):,}, "
              f"{len(options)} exact round trips", flush=True)
    if args.lua_cases:
        assert len(cases)==67
        args.lua_cases.write_text(json.dumps(cases))
    summary = {}
    for kind in ("whole", "leaf"):
        selected = [r for r in rows if r["kind"]==kind]
        summary[kind] = {"count":len(selected), "native_chars":sum(r["native_chars"] for r in selected),
                         "best_chars":sum(r["best_chars"] for r in selected),
                         "portable_chars":sum(r["portable_chars"] for r in selected),
                         "roundtrip_candidates":sum(r["roundtrip_candidates"] for r in selected)}
    (ROOT/"optimized-summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
