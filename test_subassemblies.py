import copy
import json
import random
import unittest
import zlib

from compact import candidates, decode, pack, unpack
from subassemblies import representations, restore_blocks


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def repeated_factory(nx=16, ny=8):
    rows = []
    for gy in range(ny):
        for gx in range(nx):
            for slot, (name, x, y) in enumerate([
                ("assembling-machine-3", 1.5, 1.5), ("fast-inserter", 1.5, 3.5),
                ("express-transport-belt", 1.5, 4.5), ("medium-electric-pole", 3.5, 3.5)]):
                row = {"entity_number": len(rows) * 7 + 11, "name": name,
                       "position": {"x": gx * 8 + x, "y": gy * 8 + y}}
                if slot == 0:
                    row.update(recipe="electronic-circuit", quality="rare")
                rows.append(row)
    return {"blueprint": {"item": "blueprint", "entities": rows}}


class BlockTests(unittest.TestCase):
    def assert_roundtrip(self, value):
        expected = canonical(value)
        forms = representations(value)
        for mode, form in forms.items():
            restored = restore_blocks(unpack(pack(form)))
            self.assertEqual(canonical(restored), expected, mode)

    def test_repeated_mixed_entity_blocks_are_selected(self):
        value = repeated_factory()
        original = copy.deepcopy(value)
        forms, stats = representations(value, with_stats=True)
        self.assertTrue(stats)
        self.assertEqual(forms["r"][1][0][1][0], 2)
        self.assertLess(len(zlib.compress(pack(forms["r"]), 9)),
                        len(zlib.compress(pack(forms["g"]), 9)))
        self.assertEqual(value, original)
        self.assert_roundtrip(value)

    def test_arbitrary_order_sparse_ids_internal_and_external_wires(self):
        value = repeated_factory(8, 4)
        rows = value["blueprint"]["entities"]
        for i, row in enumerate(rows):
            target = rows[(i + 5) % len(rows)]["entity_number"]
            row["connections"] = {"1": {"red": [{"entity_id": target, "circuit_id": 2},
                                                  {"entity_id": 999999999}]}}
            row["neighbours"] = [target, 999999999]
            row["tags"] = {"entity_id": target}  # Uninterpreted mod data stays literal.
        wires = [[rows[i]["entity_number"], i % 3 + 1, rows[(i + 4) % len(rows)]["entity_number"], 2]
                 for i in range(len(rows))]
        value["blueprint"]["wires"] = wires
        random.Random(45).shuffle(rows)
        self.assert_roundtrip(value)
        for mode, text in candidates(value).items():
            self.assertEqual(canonical(decode(text)), canonical(value), mode)

    def test_negative_positions_types_and_signed_zero(self):
        value = repeated_factory(8, 8)
        for i, row in enumerate(value["blueprint"]["entities"]):
            row["position"]["x"] -= 32
            row["position"]["y"] -= 32
            if i % 2:
                row["position"]["x"] = int(row["position"]["x"])
        value["blueprint"]["entities"][0]["position"] = {"x": -0.0, "y": 0}
        value["blueprint"]["entities"][1]["position"] = {"x": 0.0, "y": -0.0}
        self.assert_roundtrip(value)

    def test_nested_books_tiles_and_unsupported_shapes(self):
        tile = {"blueprint": {"tiles": [{"name": "mod-tile", "position": {"x": x, "y": y}}
                                        for y in range(16) for x in range(16)],
                              "entities": [{"name": "mod", "position": {"x": 0, "y": 1, "z": 2}}]}}
        value = {"blueprint_book": {"blueprints": [dict(index=12, **repeated_factory(4, 4)),
                  {"index": 84, "blueprint_book": {"blueprints": [dict(index=2, **tile)]}}]}}
        self.assert_roundtrip(value)

    def test_nonlattice_coordinates_fallback(self):
        value = repeated_factory(4, 4)
        value["blueprint"]["entities"][0]["position"] = {"x": 1/3, "y": 1e100}
        self.assert_roundtrip(value)

    def test_blocks_shared_between_pages_with_different_ids(self):
        rng = random.Random(451)
        rows = [{"entity_number": i * 11 + 5, "name": "mod-machine",
                 "tags": {"unique": i},
                 "position": {"x": rng.randrange(16) + 0.5,
                              "y": rng.randrange(16) + 0.5}}
                for i in range(40)]
        for i, row in enumerate(rows):
            row["connections"] = {"1": {"red": [{"entity_id": rows[(i + 1) % 40]["entity_number"]}]}}
        shifted = copy.deepcopy(rows)
        for row in shifted:
            row["entity_number"] += 10000
            row["connections"]["1"]["red"][0]["entity_id"] += 10000
            row["position"]["x"] += 64
            row["position"]["y"] += 32
        book = {"blueprint_book": {"blueprints": [
            {"index": 3, "blueprint": {"entities": rows}},
            {"index": 77, "blueprint": {"entities": shifted}}]}}
        forms, stats = representations(book, with_stats=True)
        self.assertEqual(len(forms["u"]), 5)
        self.assertTrue(any(s.get("cross_table_patterns", 0) > 0 for s in stats))
        self.assert_roundtrip(book)

    def test_randomized_layouts(self):
        rng = random.Random(450)
        for _ in range(30):
            value = repeated_factory(rng.randrange(1, 7), rng.randrange(1, 7))
            rows = value["blueprint"]["entities"]
            rng.shuffle(rows)
            for row in rows:
                if rng.random() < 0.1:
                    row["tags"] = {"extra": rng.randrange(10), "literal": [1, 2]}
            self.assert_roundtrip(value)


if __name__ == "__main__":
    unittest.main()
