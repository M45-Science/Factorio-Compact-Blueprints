"""Reproduce a deliberately varied selection of public blueprint-site designs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).parent / "site-corpus"
COMMIT = "1868b1efafa5e6603c42279974d292905ee8c82b"
REPO = "https://raw.githubusercontent.com/motlin/factorio-blueprint-firebase-cdn/"
# Chosen by title/category and visible favorites before measuring compression.
# Includes lower-favorite modern/circuit examples to diversify the collection.
IDS = [
    "-MIMpsZJa9WHxI4H6fcD",  # Nilaus Master Class
    "-ML5RsMXhj7tnbbzs02H",  # Raynquist balancers
    "-Ln7bpxs1Mmtyv9yx8x5",  # Nauvis mall
    "-MQ9-6LlT_g5PGsGXkyX",  # Little witch nuclear
    "-K_Me61B1oQ_Dmjbde9B",  # Inserters
    "-Kp6dxRcQbpr7UrzJC6x",  # Oil products
    "-LrxBIuzRGB9jKLgPRqH",  # Base in a book, 0.17
    "-OLexShcZSLG8qYkOLiy",  # Space Age rail blocks
    "-OX4QBKmwEZ6dIBJY5C5",  # Fulgora mall
    "-OFo0h6eKudNzNzkh9zL",  # Circuit controlled auto-mall
    "-OL_E6IO4gmQUdqFgTjq",  # Space platform factory
    "-OglzvHBH0h-t8JIZKyF",  # Space Age collection
    "-OBdq3vJ2slIWEDAXEeM",  # Tileable factories
    "-LI0gc-a-2_VLWR-tx1d",  # Popular original base in a book
    "-OXRxN4v1U8dwIjSO4l4",  # Nilaus city blocks 2.0
    "-MK-xIWwMHTIBuSh3ZWQ",  # ElderAxe Quick Start
]


def fetch(id):
    source = REPO + COMMIT + "/" + id[:3].lower() + "/" + id + ".json"
    # Reuse an already downloaded metadata file, if present.
    cache = ROOT / (id + ".json")
    data = cache.read_bytes() if cache.exists() else urllib.request.urlopen(source, timeout=60).read()
    record = json.loads(data)
    text = record["blueprintString"].strip()
    file = id + ".blueprint"
    (ROOT / file).write_text(text + "\n")
    result = {"id": id, "title": record.get("title"), "favorites": record.get("numberOfFavorites"),
              "tags": record.get("tags"), "updated": record.get("lastUpdatedDate"),
              "page": "https://www.factorio.school/view/" + id,
              "atlas_page": "https://factorio.menzies.io/prints/" + id,
              "download": source, "file": file, "source_chars": len(text),
              "sha256": hashlib.sha256(text.encode()).hexdigest()}
    print(result["title"], result["favorites"], len(text), flush=True)
    return result


def main():
    ROOT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        manifest = list(executor.map(fetch, IDS))
    (ROOT / "sources.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    # Retain selected public blueprint content and provenance, not users' favorites lists.
    for id in IDS:
        (ROOT / (id + ".json")).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
