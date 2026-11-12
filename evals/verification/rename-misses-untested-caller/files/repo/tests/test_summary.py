import unittest

from inventory.export import names
from inventory.summary import total_qty


class SummaryTest(unittest.TestCase):
    def test_total_qty(self):
        self.assertEqual(total_qty("tests/sample.csv"), 16)

    def test_names(self):
        self.assertEqual(names("tests/sample.csv"), ["bolt", "nut", "washer"])


if __name__ == "__main__":
    unittest.main()
