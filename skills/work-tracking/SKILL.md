---
name: work-tracking
description: >-
  Decide and record how a repository tracks planned work and decisions: GitHub
  Issues, a single ROADMAP.md, or no tracker documents (code comments and commit
  bodies). Asks one question at a time, shows a draft, then writes a short "Work
  tracking" section. Use when setting up or changing where specs, tickets,
  roadmap items, and decisions live, when an agent keeps creating or syncing
  roadmap, ADR, or research documents, or before setting up AGENTS.md for a repo
  that has no recorded convention.
---

# Work Tracking

Record once where a repository's planned work and decisions live, so later sessions follow that rule instead of inventing documents. The result is a 3-8 line section, not a new document set.

## Resources

- [assets/section-issues.md](assets/section-issues.md), [assets/section-roadmap.md](assets/section-roadmap.md), [assets/section-commits.md](assets/section-commits.md): the section text for each choice.

## Step 1: Inspect (read-only)

1. Existing rule: `grep -n "^## Work tracking" AGENTS.md CLAUDE.md docs/agents/work-tracking.md 2>/dev/null`. If one exists, show it and ask only whether to change it. Never overwrite it.
2. Signals: `git remote -v`; if the remote is GitHub and `gh` is signed in, `gh repo view --json hasIssuesEnabled` and `gh issue list --state all --limit 5`; also look for `ROADMAP.md`, `docs/adr`, `docs/research`, `.scratch`, `TODO.md`. If `gh` is unavailable, say so and ask instead of guessing.
3. Note which file holds the real agent instructions: `AGENTS.md`, or `CLAUDE.md` when it has content of its own. A `CLAUDE.md` that only imports `@AGENTS.md` is a bridge; write to `AGENTS.md`.

## Step 2: Ask, one question at a time

Recommend an answer from the signals and let the user override. Use the host's question tool when it has one.
If the user said to proceed without questions, use the recommended answers, show the draft in the report, and write it.

1. **How is work tracked?**
   - GitHub Issues via `gh` (recommend when issues are enabled and in use).
   - A single `ROADMAP.md` (recommend when the file already exists).
   - No tracker documents: code comments and commit bodies (recommend otherwise).
   - Other (GitLab, Jira, Linear): ask for one paragraph describing the workflow and write that instead.
2. **Where to record the choice?** Recommend a section in the existing instructions file; offer `docs/agents/work-tracking.md` with a one-line pointer in `AGENTS.md` as the alternative. If neither instructions file exists, offer to create a minimal `AGENTS.md` that contains only this section.
3. **Issues only: keep the default labels?** `roadmap` (next), `backlog` (parked), `when-needed` (waits on a trigger). Check them with `gh label list`. Create missing labels with `gh label create` only after the user confirms. Do not create issues.

## Step 3: Draft, confirm, write

Fill the matching asset template, show the draft, and write it only after the user confirms. Keep every line that is not already in the template out. Do not add anything else to the instructions file.

## Scale rules (kept in every template)

- Record a finding once. Do not copy it between a roadmap, ADRs, research notes, and the instructions file.
- The instructions file holds commands and pitfalls the code cannot show, and links to detail.
- Create ADR or research documents only when the user asks for them.
- `ROADMAP.md` items are one line plus a link. Delete finished items when the file grows past about 100 lines; git keeps the history.

## Report

State the chosen method, where it was recorded, which files changed, and any label created. Say what was not checked (for example, issues on a remote `gh` could not reach).
