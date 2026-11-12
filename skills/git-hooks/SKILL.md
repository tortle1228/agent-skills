---
name: git-hooks
description: >-
  Use this skill when setting up, auditing, or troubleshooting Git hooks
  (pre-commit, prepare-commit-msg, commit-msg, pre-push, post-checkout,
  post-merge) or hook managers (Lefthook, pre-commit/prek, Husky v9, or native
  core.hooksPath). Enforces fast staged-only checks (<5s), secret leak
  prevention, Conventional Commits validation, protected branch guards, and
  deterministic end-to-end verification.
---

# Git Hooks Setup and Governance

A standard procedure for building, auditing, and troubleshooting **fast Git hooks that developers have no reason to bypass**, matched to the repository's stack. For the arguments of every Git hook and common anti-patterns, see [hook-catalog.md](./references/hook-catalog.md).

## Step 0: Repository discovery

Inspect the target repository before changing anything:

1. **Git repository and existing hook setup**:
   - Find the root with `git rev-parse --show-toplevel`.
   - Check `git config --get core.hooksPath` and whether `.githooks/`, `.husky/`, `lefthook.yml`, or `.pre-commit-config.yaml` exist.
2. **Available tools**:
   - Run `command -v lefthook prek pre-commit gitleaks npx` to see which binaries are installed.
   - Read the linter and test commands in existing CI (`.github/workflows/`, `.gitlab-ci.yml`) so local hooks match CI rules.

## Step 1: Choose a hook manager

Pick one of the four strategies below based on the project and the runtimes already installed. Do not force a new runtime dependency the project does not need:

| Environment / requirement | Strategy | Template / script |
| :--- | :--- | :--- |
| **Language-agnostic default / zero external dependencies** | Built-in `core.hooksPath` + POSIX `.githooks/` | [install-hooks.sh](./scripts/install-hooks.sh) and [examples/githooks/](./examples/githooks/) |
| **Polyglot / monorepo / fast parallel runs** | `Lefthook` (`parallel: true`, `stage_fixed: true`) | [lefthook.yml](./examples/lefthook.yml) |
| **Python-centric / standard open-source hygiene hooks** | `pre-commit`, or its fast Rust-compatible alternative `prek` | [.pre-commit-config.yaml](./examples/.pre-commit-config.yaml) |
| **Pure Node.js / TypeScript single package** | `Husky v9` (`npx husky init`) + `lint-staged` + `commitlint` | `.husky/pre-commit` + `.husky/commit-msg` |

State the choice and the reason in one or two sentences in your final report: which runtimes were already present, how teammates will get the hooks after cloning, and why the obvious alternative was not picked. Hook setups outlive the conversation, and the next person to touch them needs to know whether the choice was deliberate.

## Step 2: Place rules by hook stage

Slow hooks get bypassed with `--no-verify`, so separate checks strictly by cost:

### 1. `pre-commit`: fast guard on the staged snapshot (target: 3-5 seconds)
- **Staged-only checks are mandatory**: inspect only Git index objects (`git diff --cached` / `git show :"$file"`, or the stash protection of `stage_fixed` or `lint-staged`) so unstaged working-tree edits are neither checked nor overwritten.
- **Required checks**:
  1. **Secret scan**: `gitleaks protect --staged --redact`, or built-in regexes (private key headers, AWS/GitHub/Slack tokens, blocking `.env`/`*.pem`/`*.key` files).
  2. **Merge conflict markers**: leftover `<<<<<<<`, `=======`, `>>>>>>>`.
  3. **Large blobs**: block large binaries not tracked by Git LFS (default limit 5 MB).
  4. **Filesystem compatibility and changed-file lint/format**: check case-only filename collisions and run only fast linters on changed file types.
- **Auto-fixing hooks must not leak unstaged work**: when a formatter rewrites files, a partially staged file holds both staged and unstaged edits. Naively running the formatter on the working tree and re-adding the file commits the unstaged half; restoring carelessly can delete it. Use a mechanism that isolates the index (`lint-staged` and `pre-commit` stash unstaged changes; with Lefthook `stage_fixed` or a custom script, confirm the behavior in the installed version, or format the index blob and write it back), and demonstrate with a partially staged file that the unstaged edit survives in the working tree and stays out of the commit.
- **Do not include**: whole-codebase lint, slow integration/E2E tests, or anything that needs the network.

### 2. `prepare-commit-msg`: non-blocking message helper
- **Duplicate guard is mandatory**: exit 0 immediately when the second argument (`$2`) is `merge`, `squash`, or `commit` (`--amend`).
- If the branch name (for example `feat/PROJ-123-auth`) contains an issue key, append a trailer (`Refs: PROJ-123`) to the message.

### 3. `commit-msg`: commit convention check (target: under 0.5 seconds)
- Ignore comment lines (`^#`) and let auto-generated commits (`Merge `, `Revert "`, `fixup! `, `squash! `) pass.
- Validate the **Conventional Commits** format (`<type>[optional (scope)][!]: <description>`) and the subject length counted in UTF-8 characters with `wc -m` (warn above 72, block above 100). Counting characters rather than bytes keeps non-ASCII subjects, such as Korean, from being rejected early.
- On failure, do not just exit: **print correct examples to `stderr`**.

### 4. `pre-push`: heavier gate before sharing with the remote
- Block direct pushes to protected branches (`main`, `master`, `production`), allowing an exception only through an explicit environment variable such as `ALLOW_PROTECTED_PUSH=1`.
- Block unpushed commits that contain `WIP:` or unsquashed `fixup!`/`squash!` commits.
- Place the unit test suite, full type check, and production build check here.

### 5. `post-checkout` and `post-merge`: non-blocking environment sync notices
- After a branch switch (`$3 = 1`) or a completed merge, detect changes between the previous and new HEAD to lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `uv.lock`, `go.sum`, `Cargo.lock`, and so on) and `migrations/`, and print a sync reminder.

## Step 3: Bootstrap and verify deterministically

Do not stop at checking that hook files exist; verify behavior with real Git commands:

1. **Installation and onboarding**:
   - For the native Git strategy, run `sh <this skill's directory>/scripts/install-hooks.sh <target_repo>`.
   - Record the activation command in the `package.json` `"prepare"` script, a `Makefile` target, or the onboarding section of `README.md` so teammates can enable hooks right after cloning.
2. **Verification checklist**:
   - [ ] Every hook script is executable (`chmod +x`) and `core.hooksPath` (or `.git/hooks/`) is wired up.
   - [ ] Staging a fake secret or conflict marker makes `pre-commit` exit non-zero.
   - [ ] `commit-msg` rejects a malformed message and accepts a valid Conventional Commit.
   - [ ] Local and CI duplication: local hooks can be bypassed with `--no-verify`, so key checks also run in the CI pipeline.
   - [ ] For `pre-push`, exercise it against a real (local bare) remote, including a first push of a new branch, where the remote SHA is all zeros.
3. **Report**: list the scenarios you actually ran with their results, the tool choice and reason, how to bypass in an emergency, and what still needs server-side enforcement (branch protection, required CI), since client hooks are optional by design.
