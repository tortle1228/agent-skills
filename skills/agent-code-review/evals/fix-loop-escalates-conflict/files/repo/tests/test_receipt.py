from shop.receipt import receipt_lines


def test_lines():
    assert receipt_lines([("coffee", 4000)]) == ["coffee  4,000원"]
