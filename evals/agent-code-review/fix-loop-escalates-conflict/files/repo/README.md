# shop

Small receipt service for one store, run by its staff (a handful of users).
Run tests with `pytest -q`.

## Tax policy (from accounting)

VAT is 10%. The VAT amount is always rounded **down** to whole won (floor),
to match the accounting system. Do not change this rule without sign-off from
the accounting team.
