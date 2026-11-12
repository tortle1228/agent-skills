from decimal import ROUND_HALF_UP, Decimal


def split(total: Decimal, people: int) -> list[Decimal]:
    """Split a bill; amounts are always Decimal won, never float."""
    if people <= 0:
        raise ValueError("people must be positive")
    share = (total / people).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    shares = [share] * people
    shares[-1] = total - share * (people - 1)
    return shares
