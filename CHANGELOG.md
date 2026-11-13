# Changelog

## 0.3.0

- work-tracking: decides once whether a repo tracks work in GitHub Issues, a single `ROADMAP.md`, or commits only, asks where to record it, and writes a short "Work tracking" section after you confirm.
- project-bootstrap: the scaffold now creates only `README.md` and `AGENTS.md`. ADRs, a `CLAUDE.md` bridge, `ROADMAP.md`, and research notes need a request. The Standard Production column of the checklist no longer requires Dockerfile, Renovate, structured logging, health endpoints, or compose, matching the preset text.
- project-instructions: the `CLAUDE.md` bridge is added only when the team uses Claude Code.
- git-hooks: installs `pre-commit` and `commit-msg` by default; `prepare-commit-msg`, `pre-push`, and the post-* hooks are added on request. Activation is recorded in an existing script, not a new document.
- Migration: ask explicitly for an ADR, a bridge, or the extra hooks if you relied on them being created by default.

## 0.2.0

- verification: a gate that requires fresh evidence from the real behavior before the agent claims work is done, fixed, or passing, with `PASS`, `FAIL`, `BLOCKED`, and `SKIP` verdicts.
- create-verification: generates a project-local `verify-<app>` skill (launch, doctor, drive, evidence, cleanup, feature map) and proves it by running it once and showing its check can fail on a scratch copy.
- The package description and keywords now mention verification, and the root READMEs no longer state a skill count.

## 0.1.3

- Releases are now published to npm from GitHub Actions with provenance.

## 0.1.2

- Eval cases moved to `evals/<skill>/` so Skills CLI installs no longer include test prompts and fixtures.

## 0.1.1

- project-bootstrap: the audit script no longer fails with "unbound variable" under bash 3.2, the default shell on macOS.

## 0.1.0

First release.

- Five agent skills in one package: `project-bootstrap`, `project-instructions`, `git-hooks`, `agent-code-review`, and `readme-writer`.
- project-bootstrap: 10-pillar checklist with Lean MVP, Standard Production, and Strict Enterprise presets; a read-only audit script that recognizes settings inside `pyproject.toml`/`package.json` and the built-in tooling of Rust and Go; temporary, project-local toolchains when a runtime is missing.
- project-instructions: create, audit, slim down, and sync agent instruction files, with a standard-library static auditor.
- git-hooks: hook-manager selection, staged-only checks, Conventional Commits with character-based subject length, protected-branch pre-push, and end-to-end verification.
- Installer for Codex and Claude Code: choose skills with a repeatable `--skill <name>`, list them with `agent-skills list`, and track each installation separately. `evals/` is excluded from the package and from installations.
