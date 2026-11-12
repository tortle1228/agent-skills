# Changelog

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
