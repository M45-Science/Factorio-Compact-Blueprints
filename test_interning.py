import copy
import json
import unittest

import msgpack

from compact import candidates, decode, pack, unpack, varint
from interning import expand, intern
from test_subassemblies import repeated_factory


class DictionaryTests(unittest.TestCase):
    def test_legacy_module_map_order(self):
        rows = [{"entity_number": i+1, "name": "assembling-machine-3",
                 "position": {"x": i*4, "y": 0},
                 "items": ({"speed-module": 1, "productivity-module": 3} if i%2 == 0
                           else {"productivity-module": 3, "speed-module": 1})}
                for i in range(16)]
        value = {"blueprint": {"entities": rows}}
        for mode, frame in candidates(value, interned=True, codecs=["n"]).items():
            restored = decode(frame)["blueprint"]["entities"]
            for a, b in zip(rows, restored):
                self.assertEqual(list(a["items"]), list(b["items"]), mode)

    def test_nested_values_keys_and_existing_references(self):
        value = [{"a-long-repeated-key": {"name": "repeated-prototype", "value": [True, None, -0.0]},
                  "ref": msgpack.ExtType(1, b"\x02")} for _ in range(100)]
        for strings in (False, True):
            encoded = intern(value, strings_only=strings)
            self.assertLess(len(pack(encoded)), len(pack(value)))
            restored = expand(unpack(pack(encoded)))
            self.assertEqual(pack(restored), pack(value))
            restored[0]["a-long-repeated-key"]["value"][0] = False
            self.assertTrue(restored[1]["a-long-repeated-key"]["value"][0])

    def test_invalid_dictionary_references(self):
        for payload in (([], msgpack.ExtType(2, b"\x00")),
                        ([msgpack.ExtType(2, b"\x00")], None),
                        (["abc"], msgpack.ExtType(2, b"\x80")),
                        (["abc"], msgpack.ExtType(2, varint(100)))):
            with self.assertRaises(ValueError):
                expand(payload)

    def test_all_dictionary_transports(self):
        value = {"blueprint_book": {"blueprints": [
            dict(index=7, **repeated_factory(4, 4)), dict(index=93, **repeated_factory(8, 4))]}}
        original = copy.deepcopy(value)
        options = candidates(value, interned=True)
        self.assertEqual(len(options), 125)
        for mode, text in options.items():
            self.assertEqual(json.dumps(decode(text), sort_keys=True), json.dumps(value, sort_keys=True), mode)
        self.assertEqual(value, original)

    def test_literal_number_extension(self):
        for raw in (b"18446744073709551616", b"-0.0", b"1e-100", b"-9223372036854775809"):
            self.assertEqual(unpack(pack(msgpack.ExtType(3, raw))), json.loads(raw))
        for raw in (b"null", b"true", b"01", b"1e999", b" 12 "):
            with self.assertRaises(ValueError):
                unpack(pack(msgpack.ExtType(3, raw)))


if __name__ == "__main__":
    unittest.main()
