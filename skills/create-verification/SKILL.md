---
name: create-verification
description: >-
  Generate a project-local verify-<app> skill that launches this repo's app and
  drives it the way a user does, then proves it by running it once. Use when asked
  to make a verification or control skill for a repo, when a project has no
  scripted way to prove UI, CLI, or service behavior, or when the verification
  skill suggests creating one. Not for one-off checks of a single change.
---

# Create a verification skill

A repo that an agent can launch, drive, and observe in one scripted recipe is a repo where "done" can be proven. This skill writes that recipe as a project-local skill, `verify-<app>`, for the next agent to read cold, mid-task, having never seen the app. Write for that reader: exact commands, real selectors, no placeholders.

## 1. Interview the repo, not the user

Answer from the code. Ask the user only for what you cannot observe (credentials, a private service).

- **Surface:** what does a user touch: web UI, CLI or TUI, desktop app, API, mobile app, library? Pick the primary one, note the rest.
- **Run:** the repo's own start command (package scripts, Makefile, README). Note ports, env vars, seed data, auth.
- **Drive:** an existing harness first (Playwright or Cypress specs, expect scripts, curl-able endpoints, a debug port). Otherwise a generic one: a browser for web, a terminal session (tmux or a PTY) for CLI and TUI, plain HTTP for services.
- **Observe:** what evidence can be captured: screenshots, terminal transcripts, response bodies, logs, exit codes, database state.
- **Isolate:** can two instances run side by side (ports, data dirs)? If not, the skill must say so and refuse to drive a shared instance rather than corrupt someone's session.

If the checkout does not build or start, fix that or report it precisely before generating. A recipe written against a broken base teaches wrong steps. Do not produce a placeholder skill for an app you could not run.

## 2. Write the skill

Create `verify-<app>/SKILL.md` in the host's project-local skills folder (for example `.claude/skills/` or `.agents/skills/`). Start from [references/verify-skill-template.md](references/verify-skill-template.md). The frontmatter `name` and a `description` naming the app, its surface, and when to use it, in the words a user would say, are required; without them the skill never registers.

Cover these sections, each filled from what the interview found:

- **Launch:** the exact command and how to tell it is ready: usable, not merely answering. Start from an empty data dir, including migrations and seed data. For a short-lived CLI there is no server: build once, then start each drive in its own isolated session.
- **Doctor:** one read-only check for "is this instance worth driving?": process up, right build, port owned by us, auth valid. Run it first whenever anything looks off.
- **Drive:** the recipe with real selectors and commands from this repo. Prefer stable handles (ARIA labels, data attributes, prompt strings, routes) over coordinates.
- **Evidence:** what to capture and where it goes. Proofs exercise the real user path, capture the action and the resulting state, and check side effects (files, rows, messages), not only what is visible. Mock only where a production boundary already isolates the external system. For a dry-run mode, observe what it actually skips instead of trusting its name.
- **Cleanup:** stop what you started, never by process name. Remove instances and scratch state, never the evidence.
- **Helpers:** any script you ship is executable and its invocation is shown in the skill body.

## 3. Seed the feature map

Add `verify-<app>/features/README.md` as an index, plus one file for each of the top three to five user-facing features, taken from routes, commands, menus, or docs. Each file has four sections: `Sub-features`, `How to get to it (user POV)`, `Driving it`, `Gotchas`, and states the observable end state that proves the feature works. If seed data lacks a precondition a journey needs, record that in `Gotchas`; never weaken the journey to make it pass.

## 4. Prove it before handing over

Follow your own skill once, as the next agent would: launch, run doctor, drive one mapped feature, capture evidence, clean up. After cleanup, confirm the evidence still exists where the skill says. Fix what fails, and run the cleanup after each failed attempt so broken runs do not strand processes or ports. A generated skill that was never run is a draft, not a deliverable.

Show the check can fail: on a scratch copy of the repo (never the working tree), break one behavior the check covers and confirm the check fails on that assertion, not on a crash elsewhere, then discard the copy. If that is impractical, say so under what remains unproven.

If you proved it in a stand-in (a container instead of a fresh machine, a local stack instead of a remote one), list every setup step the stand-in did that the real target will not. Those steps remain unverified.

## 5. Hand off

Tell the user what you generated and where, which feature you drove, the evidence path, and what remains unproven. Do not edit product code in the working tree. A behavior that is broken in the app is a finding to report, not something to hide in the recipe.
