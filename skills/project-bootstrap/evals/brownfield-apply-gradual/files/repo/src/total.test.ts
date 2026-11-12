import { describe, expect, it } from 'vitest';
import { total } from './total';
import { applyCoupon } from './legacy/coupon';

describe('total', () => {
  it('sums price times quantity', () => {
    expect(total([{ price: 1000, qty: 2 }, { price: 500, qty: 1 }])).toBe(2500);
  });
  it('applies a coupon', () => {
    expect(applyCoupon(2500, { kind: 'fixed', amount: 500 })).toBe(2000);
  });
});
