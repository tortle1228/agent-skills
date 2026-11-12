#!/usr/bin/env sh
# Bootstrap installer for language-agnostic POSIX Git hooks (.githooks + core.hooksPath)
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)
TEMPLATE_DIR="${SKILL_DIR}/examples/githooks"
TARGET_DIR="${1:-$(pwd)}"

if ! git -C "$TARGET_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  printf '[install-hooks] ERROR: target path is not a Git repository: %s\n' "$TARGET_DIR" >&2
  printf '  -> Run git init first, then try again.\n' >&2
  exit 1
fi

REPO_ROOT=$(git -C "$TARGET_DIR" rev-parse --show-toplevel)
DEST_HOOKS="${REPO_ROOT}/.githooks"

mkdir -p "$DEST_HOOKS"

for hook in pre-commit prepare-commit-msg commit-msg pre-push post-checkout post-merge; do
  cp "${TEMPLATE_DIR}/${hook}" "${DEST_HOOKS}/${hook}"
  chmod +x "${DEST_HOOKS}/${hook}"
done

git -C "$REPO_ROOT" config core.hooksPath .githooks

printf '[install-hooks] Git hooks installed and enabled.\n'
printf '  - Repository root: %s\n' "$REPO_ROOT"
printf '  - core.hooksPath : %s\n' "$(git -C "$REPO_ROOT" config --get core.hooksPath)"
printf '  - Enabled hooks  : pre-commit, prepare-commit-msg, commit-msg, pre-push, post-checkout, post-merge\n'
