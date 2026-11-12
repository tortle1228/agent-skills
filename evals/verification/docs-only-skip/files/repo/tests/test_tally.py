import unittest

from tally import count_blank


class CountBlankTest(unittest.TestCase):
    def test_counts_empty_strings(self):
        self.assertEqual(count_blank(["", "a", ""]), 2)


if __name__ == "__main__":
    unittest.main()
