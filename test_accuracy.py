"""Additional mixed-precision and unfamiliar-field checks from publication audit."""
import json
import random
import unittest

from compact import pack, unpack
from subassemblies import representations, restore_blocks


class AccuracyTests(unittest.TestCase):
    def test_mixed_precision_layouts_and_unknown_fields(self):
        rng = random.Random(20261114)
        numbers = [-0.0, 0.0, 0, 1, 1.0, -1.0, 0.125, 1 / 3, 2**53, 2**60]
        for trial in range(150):
            rows = []
            for i in range(rng.randrange(1, 45)):
                row = {"entity_number": i * 29 + 3,
                       "name": rng.choice(["test-a", "test-b", "mod-item"]),
                       "position": {"x": rng.choice(numbers), "y": rng.choice(numbers)},
                       "tags": {"v": rng.choice(numbers), "mixed": [True, False, None, "☃"]}}
                if rng.random() < 0.5:
                    row["connections"] = {"1": {"red": [{"entity_id": rng.randrange(50) * 29 + 3}]}}
                rows.append(row)
            rng.shuffle(rows)
            value = {"blueprint": {"entities": rows,
                                  "wires": [[rows[0]["entity_number"], 1, rows[-1]["entity_number"], 2]]}}
            expected = json.dumps(value, sort_keys=True)
            for mode, form in representations(value).items():
                actual = restore_blocks(unpack(pack(form)))
                self.assertEqual(json.dumps(actual, sort_keys=True), expected, (trial, mode))
            self.assertEqual(json.dumps(value, sort_keys=True), expected)


if __name__ == "__main__":
    unittest.main()
