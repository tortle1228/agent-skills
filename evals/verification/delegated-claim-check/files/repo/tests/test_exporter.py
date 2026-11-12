import unittest

from exporter import build_csv, validate


class ExporterTest(unittest.TestCase):
    def test_build_csv(self):
        rows = [{"id": 1, "name": "bolt", "qty": 5}]
        self.assertEqual(build_csv(rows), "id,name,qty\n1,bolt,5\n")

    def test_validate_rejects_negative_qty(self):
        with self.assertRaises(ValueError):
            validate([{"id": 2, "name": "nut", "qty": -1}])


if __name__ == "__main__":
    unittest.main()
