from shop.cart import cart_total


def test_total():
    assert cart_total([1000, 2000]) == 3000
