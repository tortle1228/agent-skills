import unittest

from pricing import apply_discount


class DiscountTest(unittest.TestCase):
    def test_ten_percent(self):
        self.assertEqual(apply_discount(200, 10), 180.0)

    def test_zero_percent(self):
        self.assertEqual(apply_discount(100, 0), 100.0)

    def test_half_price(self):
        self.assertEqual(apply_discount(50, 50), 25.0)


if __name__ == "__main__":
    unittest.main()
