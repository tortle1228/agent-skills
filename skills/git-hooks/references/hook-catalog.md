# Git Hooks Reference Catalog and Anti-Patterns

Arguments for every hook as specified in `githooks(5)`, plus practical troubleshooting.

## 1. Built-in Git hook arguments and exit codes

### Client-side hooks

| Hook | Triggered by | Arguments (`$1`, `$2`, `$3`) and `stdin` | Effect of a non-zero exit |
| :--- | :--- | :--- | :--- |
| `pre-commit` | `git commit` | None | Aborts the commit |
| `prepare-commit-msg` | `git commit` (before the editor) | `$1`: message file path, `$2`: source (`message`, `template`, `merge`, `squash`, `commit`), `$3`: commit SHA | Aborts the commit |
| `commit-msg` | `git commit`, `git merge` | `$1`: path to the temporary message file | Rejects the commit |
| `post-commit` | After `git commit` | None | No effect (notification only) |
| `pre-merge-commit` | Before a `git merge` commit | None | Aborts the merge commit |
| `pre-rebase` | `git rebase` | `$1`: upstream, `$2`: branch being rebased (optional) | Aborts the rebase |
| `post-checkout` | `git switch`, `git checkout`, `git clone` | `$1`: previous HEAD, `$2`: new HEAD, `$3`: branch checkout flag (`1` = branch, `0` = file) | No effect |
| `post-merge` | `git merge` (`git pull`) | `$1`: squash merge flag (`1` or `0`) | No effect |
| `pre-push` | `git push` | `$1`: remote name, `$2`: remote URL / `stdin`: `<local_ref> <local_oid> <remote_ref> <remote_oid>` (one per line) | Aborts the push |
| `post-rewrite` | `commit --amend`, `rebase` | `$1`: `amend` or `rebase` / `stdin`: `<old_sha> <new_sha>` | No effect |
| `pre-auto-gc` | `git gc --auto` | None | Postpones automatic GC |
| `applypatch-msg` | `git am` | `$1`: commit log file | Aborts `git am` |
| `pre-applypatch` | `git am` (after applying the patch) | None | Aborts the patch commit |
| `post-applypatch` | After `git am` | None | No effect |
| `sendemail-validate` | `git send-email` | `$1`: body file, `$2`: SMTP header file | Aborts sending |

### Server-side and special hooks

| Hook | Triggered when | Arguments and `stdin` | Effect of a non-zero exit |
| :--- | :--- | :--- | :--- |
| `pre-receive` | A push is received (once per push) | `stdin`: `<old_oid> <new_oid> <ref_name>` | Rejects the whole push |
| `update` | A push is received (once per ref) | `$1`: `<ref_name>`, `$2`: `<old_oid>`, `$3`: `<new_oid>` | Rejects only that ref |
| `proc-receive` | Special push protocol handling | Packet-line protocol | Custom handling |
| `post-receive` | After all refs are updated | `stdin`: `<old_oid> <new_oid> <ref_name>` | No effect (CI/notification trigger) |
| `post-update` | After all refs are updated | `$@`: updated ref names | No effect |
| `push-to-checkout` | A push to a checked-out remote branch | `$1`: new commit SHA | Can reject the push |
| `reference-transaction` | Every ref transaction state change | `$1`: `preparing`, `prepared`, `committed`, `aborted` | Can abort during `preparing`/`prepared` |
| `fsmonitor-watchman` | Filesystem monitor queries | `$1`: version (`1` or `2`), `$2`: timestamp/token | Falls back to a full scan |

## 2. Common anti-patterns and fixes

### Pitfall 1: False positives and misses from reading working-tree files (partial staging bug)
- **Cause**: If `pre-commit` reads working-tree files directly, as in `grep "SECRET" "$file"`, unstaged local experiments block the commit, or a secret that was staged and then deleted only in the working tree gets committed.
- **Fix**: Always pipe the index blob (`git show :"$file"`) into the check. When running auto-fixing formatters, protect partial staging with Lefthook's `stage_fixed: true`, `lint-staged`, or the `pre-commit` framework.

### Pitfall 2: Wrong commit subject length for non-ASCII text under `/bin/sh` (`dash`)
- **Cause**: On Debian/Ubuntu, `/bin/sh` is `dash`, where `${#msg}` returns the UTF-8 byte count rather than the character count (one Korean character is 3 bytes), so even a short Korean subject can be judged too long.
- **Fix**: Count characters with `printf '%s' "$header" | wc -m` under a UTF-8 locale.

### Pitfall 3: Missing zero-SHA handling in `pre-push` for new or deleted branches
- **Cause**: The first push of a new branch sends `<remote_oid>` as `0000000000000000000000000000000000000000` (forty `0`s), and a branch deletion push sends `<local_oid>` as forty `0`s.
- **Fix**:
  - If `<local_oid>` is all `0`s, it is a deletion push; skip the commit checks.
  - If `<remote_oid>` is all `0`s, compute only the new unpushed commits with `git rev-list "$local_oid" --not --remotes="$remote_name"`.

### Pitfall 4: Adopting `gitleaks` in a legacy repository stalls work because of old commits
- **Fix**:
  1. In `pre-commit`, run only `gitleaks protect --staged --redact` instead of scanning the whole history, so only new leaks are blocked.
  2. Manage existing false positives and legacy findings separately with a `gitleaks detect --report-path .gitleaks-baseline.json` baseline or `.gitleaksignore`.
