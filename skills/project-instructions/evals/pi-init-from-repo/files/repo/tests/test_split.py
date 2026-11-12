from decimal import Decimal

from settle import split


def test_split_keeps_total():
    shares = split(Decimal("10000"), 3)
    assert sum(shares) == Decimal("10000")
