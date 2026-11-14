"""Fetch pinned public examples; extract a size-spanning sample from the book."""
import hashlib
import json
from pathlib import Path
import urllib.request

from compact import native_decode, native_encode

ROOT = Path(__file__).parent
SHA = "cb56bf673eef3258819ef391d8f7a80763ae2952"
REPO = "https://raw.githubusercontent.com/redruin1/factorio-draftsman/" + SHA


def main():
    folder = ROOT / "corpus"
    folder.mkdir(exist_ok=True)
    manifest = []
    for path in ("examples/output/converted_image.blueprint",
                 "examples/output/lamp_image.blueprint",
                 "examples/output/sqrt_lut.blueprint",
                 "test/performance/huge_blueprint_book.txt"):
        data = urllib.request.urlopen(REPO + "/" + path).read()
        name = path.rsplit("/", 1)[-1]
        (folder / name).write_bytes(data)
        manifest.append({"file": name, "source": REPO + "/" + path,
                         "sha256": hashlib.sha256(data).hexdigest()})
        value = native_decode(data.decode())
        if "blueprint_book" in value:
            leaves = []

            def visit(node):
                if "blueprint" in node:
                    leaves.append({"blueprint": node["blueprint"]})
                for child in node.get("blueprint_book", {}).get("blueprints", []):
                    visit(child)

            visit(value)
            leaves.sort(key=lambda v: len(v["blueprint"].get("entities", [])))
            positions = sorted({round(i * (len(leaves) - 1) / 7) for i in range(8)})
            for i in positions:
                v = leaves[i]
                name = f"book-sample-{i:03d}.blueprint"
                (folder / name).write_text(native_encode(v))
                print(name, len(v["blueprint"].get("entities", [])), v["blueprint"].get("label"))
            print("Book:", len(leaves), "leaves; selected", len(positions))
        else:
            print(name, len(value.get("blueprint", {}).get("entities", [])))
    (folder / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
