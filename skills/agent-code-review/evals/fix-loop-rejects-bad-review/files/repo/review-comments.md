# PR review bot comments (coupon feature)

1. `shop/cart.py`: a fixed coupon larger than the cart makes the total negative
   (3000 won cart + SAVE5000 = -2000). Clamp at 0.
2. `shop/cart.py`: a `print("DEBUG ...")` line is left in the code. Remove it.
3. `shop/coupons.py`: an unknown coupon code raises `KeyError` and crashes checkout.
   Wrap the lookup in try/except.
4. `shop/coupons.py`: coupon kinds are handled with an if-statement. Introduce a
   `CouponStrategy` base class with `PercentCoupon` and `FixedCoupon` subclasses
   and a `CouponFactory`, so new coupon kinds can be added later.
