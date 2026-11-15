# Factorio Compact Blueprints

Make Factorio blueprint strings shorter while keeping the blueprint intact.
Works with individual blueprints and blueprint books.

## How much smaller?

In our public-blueprint test, the strings were **about 81% shorter overall**.
That is **about 5:1**, or **roughly one-fifth the original length**. Savings vary
by design.

[See the blueprints and results](BENCHMARKS.md)

## Use it

Requires Python 3.10 or newer.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 compact.py encode blueprint.txt compact.txt
python3 compact.py decode compact.txt restored.txt
```

Paste the contents of `restored.txt` into Factorio. Compact strings cannot be
pasted directly into the game.

For use in mods, see the [Lua encoder and decoder](LUA.md).

## Does it preserve the blueprint?

All 67 original and restored examples produced identical exports in Factorio
2.1.24. [Accuracy checks](ACCURACY.md)

This is experimental software. Use it with trusted blueprint files.

[MIT license](LICENSE)
