# Lua encoder and decoder

Copy [`lua/blueprint.lua`](lua/blueprint.lua) into your Factorio mod. It runs on
Lua 5.2 and uses Factorio's built-in compression helpers.

```lua
local blueprints = require("blueprint")

local compact = blueprints.encode_native(original_blueprint_string)
local restored = blueprints.decode_native(compact)
```

`restored` is a normal Factorio string that can be imported into an inventory
slot or pasted into the game's blueprint importer.

## Sharing strings with Python

Use `--portable` when a Python-generated string needs to be decoded inside
Factorio:

```sh
python3 compact.py encode blueprint.txt compact.txt --portable
```

Python can decode Lua-generated strings directly. Portable strings use zlib or
no compression. Python's default search also tries Brotli, Zstandard, and LZMA;
Lua needs external codec callbacks to read those compression choices.

## Options

```lua
-- Faster encoding: skip the repeated-block search.
local compact = blueprints.encode_native(original, {blocks = false})

-- Work with JSON instead of game strings.
local compact = blueprints.encode_json(json_text)
local json_text = blueprints.decode_json(compact)
```

The encoder searches flat, spatially ordered, shared-settings, repeated-block,
and shared-string representations. Its search is smaller than Python's; both
decoders understand all representation types. The Lua encoder can therefore
choose a different size while preserving the same blueprint.

Outside Factorio, uncompressed strings work without dependencies:

```lua
local compact = blueprints.encode_json(json_text, {codec = "n"})
local json_text = blueprints.decode_json(compact)
```

Other compressors can be supplied through `options.codecs`, keyed by `d`, `b`,
`z`, or `l`. Each entry has `encode(raw_bytes)` and `decode(compressed_bytes)`
callbacks. Native game-string conversion requires a deflate callback when
Factorio's helpers are unavailable.

## Preserving values

Use the string APIs above to retain empty arrays, nulls, floating-point values,
negative zero, and large integers. The module uses its own JSON reader to keep
these distinctions. Its lower-level `parse_json`, `to_json`, `encode`, and
`decode` APIs operate on that typed representation; ordinary untyped Lua tables
are not a replacement for it.

Use trusted input. This experimental decoder is not hardened against malicious
decompression or dictionary-expansion payloads.
