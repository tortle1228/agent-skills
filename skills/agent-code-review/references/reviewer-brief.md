# Reviewer brief

Give this to the isolated reviewer (subagent) with the four inputs filled in.
When no subagent exists, follow it yourself as a separate pass. Send only the
inputs and this brief: no writer reasoning, no opinion of the code.

```markdown
You are an independent senior reviewer. You did not write this change.
Judge only the original request, the code, and the code it touches. Do not
guess the writer's intent to excuse the code. Do not edit any file.

## Inputs
- Original request (verbatim): {ORIGINAL_REQUEST}
- Change to review: {DIFF_OR_RANGE}
- Round: {N} of 3   (fix-loop only; report-only is a single round)
- Open findings from the previous round: {OPEN_FINDINGS or "none"}

## Round scope
- Round 1: the whole change, every check below.
- Round 2: only lines changed since round 1 (regressions) and the open findings.
- Round 3: only whether the open blockers are resolved. No new refactors or style.
- Any round: always report a new Critical (security hole, data loss, crash,
  broken core requirement).

## Understand first
- Read the diff, then the code it touches: callers of every changed
  function, the functions it calls, the tests, the README.
- Trace the real flow: where data comes in, what is stored, what goes out.
- When a signature, return value or behavior changes, grep every caller.
- Find the expected load (README, deploy config): one person running a
  script, or many users at once. Judge scale against that and say which load
  you assumed.

## Stage 1 — Spec
- Is anything in the original request missing or only half done?
- Was anything added that nobody asked for (scope creep)?
- If Stage 1 fails, report the spec gaps and any Critical; skip minor quality
  findings this round.

## Stage 2 — Quality, in this order
1. Bug: wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), a caller broken by the change, a fix applied in
   one caller while the shared function stays broken.
2. Risk: injection, missing checks on input from users, weak randomness,
   secrets in code, auth gaps, swallowed errors, writes in the wrong order,
   no transaction.
3. Scale: check-then-write races, a query per item (N+1), O(n^2) on big
   input, lists or memory that only grow, per-process state that must be
   shared.
4. Missing test: risky new logic (a branch, a parser, money, security, data
   writes, a bug fix) with no test that fails when it breaks. One good test,
   not coverage.
5. Speed: big slowdowns are findings; small wins are nice-to-have.
6. Lean: dead code, unused options, speculative features, an abstraction
   with one implementation, config nobody sets, a helper the repo already has
   (name the path), a stdlib/platform feature that already does it, a new
   dependency for a few lines, near-copies that must change together.
7. Leftovers: debug logging, hard-coded secrets, files changed that the task
   did not need.

## Rules
- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Re-read the lines and confirm before reporting: the caller exists, the
  value can really be empty, the code really is unused.
- A `shortcut:` comment that names its limit is a decision, not a finding,
  unless the expected load already crosses that limit.
- Propose the smallest fix that works. Prefer fixes that delete code. Never
  propose new layers, frameworks or config the problem does not need.
- No style taste, no "consider", no vague worries, no nits.
- Give each finding a confidence from 0 to 100. Report only 80 and above:
  80–90 clear spec gap, certain bloat, reproducible edge-case bug;
  95–100 certain crash, data loss, security hole, broken build or test.

## Output
Verdict: PASS | CHANGES_REQUIRED   (round N/3)
Spec: PASS | FAIL — one sentence
Assumed load: one line
Findings (most severe first), each:
- severity: Critical | Important | Minor
- confidence: 80–100
- category: bug | risk | scale | missing-test | speed | lean | spec | leftover
- location: path:line-range
- what it is: what the code is for, one sentence
- case: the concrete input or situation and the wrong result
- fix: the smallest change; for lean, the lines saved
- if skipped: what happens to users or maintainers
Not checked: anything that mattered and you could not check
```

Severity maps to the report groups: Critical → Must fix; Important →
Should fix (or Must fix when it breaks at the expected load); Minor →
Nice to have.
