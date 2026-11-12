import unittest

from inventory.loader import load_rows


class LoaderTest(unittest.TestCase):
    def test_reads_all_rows(self):
        self.assertEqual(len(load_rows("tests/sample.csv")), 3)


if __name__ == "__main__":
    unittest.main()
