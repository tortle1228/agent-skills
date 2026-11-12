# Common Cross-Language Configuration Snippets

Copy and adapt these minimal configurations when bootstrapping a repository. Git hook configuration is owned by the `git-hooks` skill (see SKILL.md).

---

## 1. `.editorconfig`
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.{py,rs}]
indent_size = 4

[*.go]
indent_style = tab
indent_size = 4

[Makefile]
indent_style = tab
```

---

## 2. `mise.toml` (Unified Runtime Pinning & Task Runner)
```toml
[tools]
# Uncomment and pin the runtimes used in this project (versions below are examples;
# check the current LTS/stable release before pinning):
# node = "22"
# pnpm = "10"
# python = "3.12"
# uv = "latest"
# go = "1.23"
# gitleaks = "latest"

[tasks.check]
description = "Run formatting, linting, typecheck, and tests"
run = [
  # Add canonical project verification commands here
]
```

---

## 3. `renovate.json` (Low-Noise Grouped Dependency Updates)
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    ":semanticCommits",
    "group:allNonMajor"
  ],
  "schedule": ["before 6am on monday"],
  "labels": ["dependencies"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

---

## 4. Minimal GitHub Actions CI Template (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      # Pin actions to a full commit SHA of the current release, with the tag in a comment.
      - uses: actions/checkout@<sha> # vN
      # Add runtime setup (e.g., pnpm/action-setup, astral-sh/setup-uv, actions/setup-go, dtolnay/rust-toolchain)
      # Run: install -> format --check -> lint -> typecheck -> test
```
