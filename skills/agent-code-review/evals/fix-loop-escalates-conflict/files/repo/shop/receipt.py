def receipt_lines(items):
    """items: list of (name, price in won). Returns printable lines."""
    return [f"{name}  {price:,}원" for name, price in items]
