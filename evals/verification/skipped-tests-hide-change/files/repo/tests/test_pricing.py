import os
import unittest

from pricing import parse_price


@unittest.skipUnless(os.environ.get("DB_URL"), "needs DB_URL")
class ParsePriceTest(unittest.TestCase):
    def test_half_up(self):
        self.assertEqual(parse_price("2.675"), 2.68)

    def test_plain(self):
        self.assertEqual(parse_price("3.10"), 3.1)


if __name__ == "__main__":
    unittest.main()
