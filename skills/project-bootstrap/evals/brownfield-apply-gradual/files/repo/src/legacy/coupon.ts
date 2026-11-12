// Old code copied from the admin app. Works, but nobody has cleaned it up.
var unused = 1;

export function applyCoupon(amount, coupon) {
  let result = amount;
  if (coupon.kind == 'fixed') {
    result = amount - coupon.amount;
  } else if (coupon.kind == 'percent') {
    result = amount - Math.floor(amount * coupon.rate / 100);
  }
  return result < 0 ? 0 : result;
}

export function parseCoupon(raw: any) {
  const data = JSON.parse(raw);
  let debug = data.code;
  return { kind: data.kind, amount: data.amount, rate: data.rate };
}
