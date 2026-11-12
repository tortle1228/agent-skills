import pytest

from shop.db import connect
from shop.orders import add_order


def test_add_order_rejects_zero():
    with pytest.raises(ValueError):
        add_order(connect(), "kim", 0)
