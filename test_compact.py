import copy
import json
import random
import unittest

from compact import (candidates, coordinates, decode, encode, native_decode,
                     native_encode, sequence, transform, restore,
                     uncoordinates, unsequence)


class CodecTests(unittest.TestCase):
    def test_sequence_modes(self):
        rng = random.Random(45)
        cases = [[], [7], [4] * 1000, list(range(-400, 400, 3)),
                 [i // 20 for i in range(2000)],
                 [rng.randrange(-100000, 100000) for _ in range(500)],
                 [rng.randrange(3) for _ in range(1000)]]
        for _ in range(100):
            cases.append([rng.randrange(-100, 100) for _ in range(rng.randrange(100))])
        for values in cases:
            self.assertEqual(unsequence(sequence(values)), values)

    def test_numeric_types_and_precision(self):
        for values in ([1, 2.0, -0.0, 0, -12.5, 7.00390625],
                       [1 / 3, 1e100, -1e-100], [2**60, -2**60]):
            decoded = uncoordinates(coordinates(values))
            self.assertEqual(json.dumps(decoded), json.dumps(values))

    def test_metadata_wires_books_and_unknowns(self):
        bp = {"blueprint": {"item": "blueprint", "version": 2**63 + 5,
              "label": "Modded 🏭", "parameters": [{"anything": 123}],
              "entities": [
                  {"entity_number": 7, "name": "mod-a", "position": {"x": -1.5, "y": -0.0},
                   "quality": "mod-q", "control_behavior": {"a": [1, None, True]},
                   "connections": {"1": {"red": [{"entity_id": 903}]}}},
                  {"entity_number": 903, "name": "mod-a", "position": {"x": 2, "y": 3.0}}],
              "wires": [[7, 1, 903, 2]], "tiles": [
                  {"name": "mod-tile", "position": {"x": 0, "y": 0}}]}}
        book = {"blueprint_book": {"item": "blueprint-book", "blueprints": [
            dict(index=42, **bp), {"index": 99, "blueprint_book": {
                "blueprints": [dict(index=5, **copy.deepcopy(bp))]}}]}}
        original = copy.deepcopy(book)
        for name, text in candidates(book).items():
            self.assertEqual(decode(text), original, name)
        self.assertEqual(book, original)
        self.assertEqual(native_decode(native_encode(decode(encode(book)))), book)

    def test_fallback_and_marker_collision(self):
        for value in ({"blueprint": {"entities": [{"unexpected": 1}], "tiles": []}},
                      {"blueprint": {"entities": [{"entity_number": 1, "name": "x",
                       "position": {"x": 0, "y": 0, "z": 1}}]}},
                      {"arbitrary": 2**100, "fake-marker": ["BX0:", None]}):
            self.assertEqual(decode(encode(value)), value)

    def test_randomized_blueprints(self):
        rng = random.Random(450)
        for _ in range(100):
            entities = [{"name": rng.choice(["belt", "chest", "mod-x"]),
                         "entity_number": i * 7 + 9,
                         "position": {"x": rng.randrange(-100, 100) / 2,
                                      "y": rng.randrange(-100, 100) / 256},
                         "tags": {"variant": rng.randrange(5)}}
                        for i in range(rng.randrange(100))]
            value = {"blueprint": {"entities": entities}}
            self.assertEqual(restore(transform(value)), value)


if __name__ == "__main__":
    unittest.main()
