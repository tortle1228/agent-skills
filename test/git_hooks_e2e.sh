#!/usr/bin/env bash
# End-to-end check for the git-hooks skill: installs its POSIX hooks into a throwaway
# repository with a local bare remote and runs 10 scenarios against real Git commands.
# Usage: bash test/git_hooks_e2e.sh <skill-dir>
set -euo pipefail

if [ $# -ne 1 ] || [ ! -f "$1/scripts/install-hooks.sh" ]; then
  echo "usage: $0 <git-hooks skill directory>" >&2
  exit 2
fi
SKILL_DIR=$(cd -- "$1" && pwd)

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Never read or write the developer's global/system Git config (hooksPath, templates, signing).
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE ALLOW_PROTECTED_PUSH ALLOW_WIP_PUSH GIT_HOOK_ALLOW_SECRET_FILES GIT_HOOK_MAX_FILE_SIZE_KB

REMOTE="$TMP/remote.git"
REPO="$TMP/work"
g() { git -C "$REPO" "$@"; }
# Runs a command that must fail; reports the reason when it unexpectedly succeeds.
expect_fail() {
  local why=$1; shift
  if "$@" >/dev/null 2>&1; then echo "  $why" >&2; return 1; fi
}

git init -q --bare -b main "$REMOTE"
git init -q -b main "$REPO"
g config user.name "Hook E2E"
g config user.email "hook-e2e@example.invalid"
g config commit.gpgsign false
printf '.env\n.env.*\n!.env.example\n*.pem\n*.key\n.githooks/*.local\n' > "$REPO/.gitignore"
printf '# fixture\n' > "$REPO/README.md"
g add .gitignore README.md
g commit -q -m "chore: initial commit"
g remote add origin "$REMOTE"
sh "$SKILL_DIR/scripts/install-hooks.sh" "$REPO" >/dev/null

t1() {
  printf 'AWS_KEY=AKIAIOSFODNN7EXAMPLE\n' > "$REPO/secret.txt"
  g add secret.txt
  expect_fail "pre-commit did not block the AWS key" g commit -m "feat: add config"
  g reset -q --hard HEAD; rm -f "$REPO/secret.txt"
}
t2() {
  printf 'normal line\n<<<<<<< HEAD\nmine\n=======\ntheirs\n>>>>>>> feature/branch\n' > "$REPO/conflict.txt"
  g add conflict.txt
  expect_fail "pre-commit did not block conflict markers" g commit -m "fix: resolve conflict"
  g reset -q --hard HEAD; rm -f "$REPO/conflict.txt"
}
t3() {
  printf 'PORT=3000\n' > "$REPO/.env"
  g add -f .env
  expect_fail "pre-commit did not block .env" g commit -m "chore: add env"
  g reset -q --hard HEAD; rm -f "$REPO/.env"
  printf 'PORT=3000\n' > "$REPO/.env.example"
  g add .env.example
  g commit -q -m "chore: add .env.example template"
}
t4() {
  printf 'clean staged line\n' > "$REPO/app.txt"
  g add app.txt
  printf 'UNSTAGED_SECRET=AKIAIOSFODNN7EXAMPLE\n' >> "$REPO/app.txt"
  g commit -q -m "feat: verify staged-only index inspection"
  g checkout -q -- app.txt
}
t5() {
  head -c 2048 /dev/zero | tr '\0' 'a' > "$REPO/large.txt"
  g add large.txt
  expect_fail "pre-commit did not block the oversized blob" env GIT_HOOK_MAX_FILE_SIZE_KB=1 git -C "$REPO" commit -m "chore: add large file"
  g reset -q --hard HEAD; rm -f "$REPO/large.txt"
}
t6() {
  printf 'hello\n' >> "$REPO/app.txt"
  g add app.txt
  expect_fail "commit-msg accepted a non-conventional message" g commit -m "update app.txt"
  expect_fail "commit-msg accepted a >100 char subject" g commit -m "feat: $(printf '%0105d' 0)"
  # 66 characters but 186 UTF-8 bytes: must be measured in characters and pass, even under LC_ALL=C.
  local msg="$TMP/korean-msg"
  printf 'feat: %s\n' "$(printf '한글제목%.0s' $(seq 15))" > "$msg"
  LC_ALL=C sh "$REPO/.githooks/commit-msg" "$msg" 2>/dev/null
}
t7() {
  g checkout -q -b feat/PROJ-101-auth
  g commit -q -m "feat(auth): 한글 커밋 메시지 및 티켓 자동 주입 검증"
  g log -1 --format='%B' | grep -q '^Refs: PROJ-101$' || { echo "  Refs: PROJ-101 not injected" >&2; return 1; }
  g commit -q --amend --no-edit
  [ "$(g log -1 --format='%B' | grep -c '^Refs: PROJ-101$')" -eq 1 ] || { echo "  ticket duplicated on --amend" >&2; return 1; }
}
t8() {
  g checkout -q main
  expect_fail "pre-push did not block push to main" g push origin main
  ALLOW_PROTECTED_PUSH=1 g push -q origin main 2>/dev/null
}
t9() {
  g checkout -q feat/PROJ-101-auth
  printf '{"lockfileVersion": 3}\n' > "$REPO/package-lock.json"
  g add package-lock.json
  g commit -q -m "fixup! feat(auth): 한글 커밋 메시지 및 티켓 자동 주입 검증"
  expect_fail "pre-push did not block the fixup! commit" g push origin feat/PROJ-101-auth
  g reset -q --soft HEAD~1
  g commit -q -m "chore(deps): lockfile 업데이트"
  g push -q origin feat/PROJ-101-auth 2>/dev/null
}
t10() {
  # Capture first: grep -q closing the pipe early would trip pipefail via SIGPIPE.
  local out
  out=$(g checkout main 2>&1)
  grep -q '\[post-checkout\] Notice' <<<"$out" || { echo "  post-checkout did not notify" >&2; return 1; }
  out=$(g merge --no-ff feat/PROJ-101-auth -m "Merge branch 'feat/PROJ-101-auth'" 2>&1)
  grep -q '\[post-merge\] Notice' <<<"$out" || { echo "  post-merge did not notify" >&2; return 1; }
}

names=(
  "pre-commit blocks a hardcoded AWS key"
  "pre-commit blocks merge conflict markers"
  "pre-commit blocks .env and allows .env.example"
  "pre-commit inspects only the staged blob, not unstaged edits"
  "pre-commit blocks blobs above GIT_HOOK_MAX_FILE_SIZE_KB"
  "commit-msg blocks non-conventional and >100 char subjects, counts UTF-8 characters"
  "prepare-commit-msg injects Refs: PROJ-101 once, also after --amend"
  "pre-push blocks main unless ALLOW_PROTECTED_PUSH=1"
  "pre-push blocks fixup! commits and allows a clean feature branch"
  "post-checkout and post-merge print dependency sync notices"
)
failed=0
for i in "${!names[@]}"; do
  n=$((i + 1))
  # Subshell with its own errexit: any failing step fails only this scenario.
  set +e; ( set -e; "t$n" ) >/dev/null; rc=$?; set -e
  if [ "$rc" -eq 0 ]; then echo "PASS $n: ${names[$i]}"; else echo "FAIL $n: ${names[$i]}"; failed=1; fi
done
exit "$failed"
