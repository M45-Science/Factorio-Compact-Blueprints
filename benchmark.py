"""Report complete printable lengths, with exact parsed-JSON round-trip checks."""
import json
from pathlib import Path
import random
import time

from compact import (candidates, decode, json_bytes, native_decode, native_encode,
                     transform, pack, restore)

ROOT = Path(__file__).parent


def synthetic():
    def blueprint(entities):
        return {"blueprint": {"item": "blueprint", "version": 562949953421312,
                              "entities": entities}}

    for name, width, height, spacing in (("synthetic-belt-grid", 100, 100, 1),
                                         ("synthetic-solar-grid", 100, 100, 3)):
        entities = [{"entity_number": y * width + x + 1,
                     "name": "transport-belt" if spacing == 1 else "solar-panel",
                     "position": {"x": x * spacing + 0.5, "y": y * spacing + 0.5}}
                    for y in range(height) for x in range(width)]
        yield name, blueprint(entities)
    rng = random.Random(45)
    entities = [{"entity_number": i + 1, "name": "constant-combinator",
                 "position": {"x": rng.randrange(-10000, 10000) + 0.5,
                              "y": rng.randrange(-10000, 10000) + 0.5},
                 "tags": {"random": rng.randbytes(16).hex()}}
                for i in range(1000)]
    yield "synthetic-random-control", blueprint(entities)


def main():
    rows = []
    examples = [(p.stem, native_decode(p.read_text()))
                for p in sorted((ROOT / "corpus").glob("*.blueprint"))]
    examples += list(synthetic())
    for name, value in examples:
        start = time.monotonic()
        options = candidates(value, repeated=False)
        # Compare normalized serialized trees; retains numeric types and signed zero.
        expected = json.dumps(value, sort_keys=True, ensure_ascii=False)
        for mode, text in options.items():
            assert json.dumps(decode(text), sort_keys=True, ensure_ascii=False) == expected, (name, mode)
        native = len(native_encode(value))
        best_json = min((t for m, t in options.items() if m.startswith("j/")), key=len)
        best_structure = min((t for m, t in options.items() if m.startswith("s/")), key=len)
        best_mode, best = min(options.items(), key=lambda kv: len(kv[1]))
        row = {"name": name, "native_chars": native, "best_json_chars": len(best_json),
               "best_structure_chars": len(best_structure), "best_chars": len(best),
               "ratio": round(native / len(best), 3), "mode": best_mode,
               "json_bytes": len(json_bytes(value)),
               "structured_bytes": len(pack(transform(value))),
               "all_modes": {m: len(t) for m, t in options.items()},
               "seconds": round(time.monotonic() - start, 3)}
        rows.append(row)
        print(f'{name:30s} {native:>9,} -> {len(best):>8,}  {row["ratio"]:>7.2f}x  '
              f'JSON-only {len(best_json):>8,}  {best_mode}  {row["seconds"]}s', flush=True)
        (ROOT / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
    print("Every candidate round-tripped every fixture.")


if __name__ == "__main__":
    main()
