---
name: agent-code-review
description: >-
  Review a code change like the senior developer who gets paged when it breaks,
  then report findings in plain language with a clear ship/fix verdict. Two
  modes: report-only ("review this", "review my PR / last commit / diff") lists
  findings and changes no code; fix-loop ("review and fix", "finish this up",
  or before you declare your own feature, bugfix or refactor done) runs an
  isolated reviewer, verifies each finding, fixes, and re-checks for at most 3
  rounds. Use this whenever someone asks for a code review, a PR review, a
  pre-merge check, or whether a change is safe or over-engineered, and before
  reporting multi-file or 30+ line changes as complete, even if they don't say
  "review".
---

# Agent Code Review

Order of importance: **correct, safe, holds under load, tested, fast, lean.**
The reviewer's job is to find what will break or cost someone later, prove it
with a concrete case, and propose the smallest fix. A review that ends in
endless ping-pong or a pile of style opinions is worse than no review, so this
skill caps the loop and drops anything without evidence.

## Pick the mode

- **report-only** — the user asks for a review of something (uncommitted
  changes, a commit, a branch, a PR, files). List findings; change no code.
- **fix-loop** — the user asks you to review *and* fix or finish, or you are
  about to call your own non-trivial work done. Review, fix, re-check (max 3
  rounds).
- Unsure? Use report-only. Changing code the user didn't ask you to change is
  harder to undo than an extra question.

## Step 0 — Skip check and entry gate

1. **Skip** when the change is only typos, comments, docs, formatter output,
   lockfiles or generated code. Say so in one line and stop.
2. **Run the deterministic checks first**: build, type check, lint, the tests
   that touch the change. Use the project's own commands (README, package
   scripts, Makefile, CI config). Machines catch syntax and formatting for
   free; don't spend review attention on them.
   - Failing in fix-loop: fix those first, then review.
   - Failing in report-only: report the failure as a finding.
   - No tests or no way to run them: continue, and say so in the report's *not checked* line.
3. **Fix the baseline**:
   - The *original* request, in the user's own words. Don't paraphrase it —
     a writer's summary carries the writer's interpretation into the review.
   - The exact change: `git diff`, `BASE..HEAD`, a PR, or named files.
     Nothing named: uncommitted changes, else the last commit.

## Step 1 — Isolated review

The writer of a change is the worst reviewer of it: they read what they meant,
not what they wrote. So the review runs in a **fresh context**.

- **Subagents available** (Claude Code Agent/Task, Codex subagents, Antigravity
  agents, …): start one read-only reviewer and give it
  [references/reviewer-brief.md](references/reviewer-brief.md) with the
  original request, the change range, the round number and, from round 2, the
  open findings. Don't give it your reasoning or your opinion of the code.
- **No subagents**: do the review yourself as a separate pass. Re-read the
  request and the diff from the top as if you had never seen them, follow the
  brief, and note "same-context review, no isolated reviewer" in the report's
  *not checked* line.
- In report-only mode on someone else's change you are already a fresh
  reviewer; a subagent is optional.

The brief makes the reviewer read the connected code (callers, callees,
tests), not only the diff, and check **spec first** (missing requirements,
unrequested features), then quality. A spec failure does not hide a security
hole or data loss: those are always reported.

## Step 2 — Triage and verify

Treat review output as claims to check, not orders.

1. **No concrete case, no finding.** Each finding must say "this input or
   situation leads to this wrong result". Drop vague worries, "consider…",
   style taste and nits. The reviewer's confidence score (keep ≥ 80) is a
   tiebreaker, not the test.
2. **Verify against the code** before accepting: the caller exists, the value
   really can be empty, the code really is unused, the test really would not
   catch it. Run it or grep it when you can.
3. **Push back** when a finding is wrong, adds layers the problem doesn't
   need, or conflicts with project rules. Record it as rejected with a
   one-line reason. No ritual agreement ("You're absolutely right!").
4. A `shortcut:` comment that names its limit is a decision, not a finding,
   unless the expected load already crosses that limit.
5. Sort what survives into **Must fix / Should fix / Nice to have** (see
   [references/report-format.md](references/report-format.md)).

report-only mode: go to the report.

## Step 3 — Fix loop (fix-loop mode only, max 3 rounds)

| Round | Reviewer scope | After the round |
| --- | --- | --- |
| 1 | Whole change: spec + every lens | Fix accepted Must/Should; rerun tests; round 2 if anything was fixed |
| 2 | Only what round 1 changed (regressions) + still-open findings | Clean → stop. Otherwise round 3 |
| 3 | Open blockers only. No new refactors or style | Resolved → stop. Not resolved → stop and escalate |

- Fix with the smallest change that works; prefer fixes that delete code.
  Rerun the tests after every round of fixes.
- **A new Critical** (security hole, data loss, crash, broken core requirement)
  found in any round is always reported, even in round 3. If it cannot be
  fixed inside the cap, stop and hand it to the user.
- **Escalate immediately** when the spec is ambiguous or a fix needs an
  architecture trade-off. Those are the user's decisions, not the loop's.
- **Done** only when all hold: tests green; no missing requirement; no open
  Must fix; no debug logging, hard-coded secrets or unintended file changes.

## Report

Always finish with the report in
[references/report-format.md](references/report-format.md), written entirely
in the user's language, **labels included** (a Korean user gets 판정, not
Verdict; English labels in a translated report read as half-finished). Its
parts: what the change does; numbered findings grouped by must / should /
nice, each with what it is, the problem, the fix and the cost of skipping it;
then the verdict, lines that can go, and what was not checked. fix-loop adds
iterations, fixed and rejected lines. The reader may never have seen this
code: short sentences, everyday words, explain a term the first time.
