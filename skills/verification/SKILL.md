---
name: verification
description: >-
  Gate to pass before claiming work is done, fixed, passing, or ready. Requires
  fresh evidence from the real thing (a command run, an app driven, a value read),
  not "it compiles", "tests should pass", or a subagent's success report. Use it
  before saying done, fixed, works now, or all green; before committing, opening a
  PR, or handing work off; and when accepting delegated work, even if the user
  never says "verify".
---

# Verification

Evidence before claims. Unverified work has unknown correctness, and a wrong claim costs the reader far more than one extra check costs you. Observe the real behavior instead of inferring it from a proxy such as a compiler pass, a file timestamp, a cached screenshot, or an agent's self-report.

## The gate

Before you state any status, run these in order:

1. **Claim.** Write down exactly what you are about to say ("the export no longer drops blank rows").
2. **Proof.** Choose the command or user path that would fail if the claim were false.
3. **Run it fresh.** Run it now, after your last edit, in full. An earlier run proves an earlier state.
4. **Read it.** Read all the output: exit code, failure count, warnings, and whether it actually exercised the changed code.
5. **Report.** State the claim with its evidence, or state the real status. If a check did not run, say "not checked"; never round it up to a pass.

If you have not run the proof in this turn, you cannot claim it passes. Words like "should", "probably", and "seems to" mean step 3 was skipped.

## What each claim needs

| Claim | Required evidence | Not enough |
| --- | --- | --- |
| Tests pass | Test command output with 0 failures | An earlier run, "should pass" |
| Build works | Build command exits 0 | Lint or type check passing |
| Bug fixed | The original symptom, reproduced before and gone after | Code changed, tests unrelated to the symptom |
| Feature works | The feature driven the way a user reaches it | A unit test of an internal function |
| Regression test is real | It fails without the fix and passes with it | It passes once |
| Delegated work done | Your own look at the diff and a fresh run | The delegate says "success" |
| Requirements met | A line-by-line check against the request | Tests pass |

## Drive the real surface

Go to what the user touches. Follow callers outward from the changed code until you reach a surface:

| Surface | Prove it by |
| --- | --- |
| CLI or script | Running it with the changed flag or input; read stdout and the exit code |
| HTTP or service | Starting it, calling the changed route, reading the response and side effects (rows, files) |
| UI | Launching the app, clicking through the path, and capturing a screenshot or DOM state |
| Library | Calling the public entry point the way a consumer would, not an internal helper |
| Docs, types, or tests only | `SKIP`: no runtime surface; say so and stop |

For a bug fix, reproduce the symptom before you change anything, so "gone" means something. When a check passes the first time, make sure it could have failed: run it against the old behavior or probe an adjacent edge case (empty input, bad flag, interrupted run).

Capture raw evidence (output, response body, screenshot path), not "I observed that...". Run the real path, not a test-only shortcut. Where a dry run or mock is the only safe option, say which part it skipped.

## Use the project's recipe

Look for an existing way to run the app before inventing one: a project-local `verify-*` skill, a Makefile target, a package script, a README quickstart. Use it.

If the project has a runnable app but no recipe, and you would otherwise rediscover the launch steps on every task, suggest the `create-verification` skill once. This skill works without it, so never block on it.

## Report

End the work with one verdict per claim:

- `PASS`: the proof ran fresh and confirmed the claim. Show the command and the decisive output.
- `FAIL`: the proof ran and contradicted the claim. Show it and keep working, or report it plainly.
- `BLOCKED`: the proof could not run (service down, missing credentials, no launcher after about 15 minutes). Name what is missing. A blocked check is never a pass.
- `SKIP`: no runtime surface to observe. Say so in one line with the reason and stop; a docs-only change needs no further report.

List what you did not check at the end, including anything mocked or out of scope.

## Red flags

Stop and run the check if you notice yourself:

| Thought | Reality |
| --- | --- |
| "Should work now" | Run it. |
| "I'm confident" | Confidence is not evidence. |
| "The linter passed" | A linter is not a compiler, and neither is a running app. |
| "The agent said it succeeded" | Verify independently. |
| "Just this once" | The check you skip is the one that fails. |
| Writing "Done!" before any command ran | The order is evidence first, then the word. |

This applies before every commit, push, PR, and handoff, and to every sentence that implies success.
