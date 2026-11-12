#!/usr/bin/env bash
# Read-only diagnostic script for the project-bootstrap skill.
# Checks available host runtimes/tools and audits a target directory against the 10-Pillar setup checklist.
# Pillar 9 (observability) lives in code, not files, so it is not checked here.

set -euo pipefail

TARGET_DIR="${1:-.}"
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: Directory '$TARGET_DIR' does not exist." >&2
  exit 1
fi
TARGET_ABS="$(cd "$TARGET_DIR" && pwd)"

echo "=== Project Bootstrap Diagnostic ==="
echo "Target Directory: $TARGET_ABS"
echo ""

echo "--- 1. Host Toolchain Availability ---"
check_cmd() {
  local cmd="$1"
  if command -v "$cmd" >/dev/null 2>&1; then
    local ver
    ver="$("$cmd" --version 2>&1 | grep -v '^[[:space:]]*$' | grep -v '^---' | head -n 1 || true)"
    printf "  [FOUND] %-14s %s\n" "$cmd" "$ver"
  else
    printf "  [MISS]  %-14s\n" "$cmd"
  fi
}

for tool in git mise node npm pnpm bun python3 uv go rustc cargo java gradle dotnet docker lefthook pre-commit gitleaks copier; do
  check_cmd "$tool"
done

echo ""
echo "--- 2. Repository State & Manifests ---"
file_count="$(cd "$TARGET_ABS" && find . -maxdepth 2 -not -path './.*' -type f | wc -l | tr -d ' ')"
echo "  Visible files (depth <= 2): $file_count"

check_any() {
  local label="$1"
  shift
  local found=()
  for pattern in "$@"; do
    # shellcheck disable=SC2086
    for match in "$TARGET_ABS"/$pattern; do
      if [[ -e "$match" ]]; then
        found+=("${match#"$TARGET_ABS"/}")
      fi
    done
  done
  # ${arr[@]+...} keeps bash 3.2 (macOS) from failing on an empty array under set -u.
  found+=(${EMBEDDED[@]+"${EMBEDDED[@]}"})
  EMBEDDED=()
  if (( ${#found[@]} > 0 )); then
    printf "  [OK]    %-32s -> %s\n" "$label" "${found[*]}"
  else
    printf "  [NONE]  %-32s\n" "$label"
  fi
}

shopt -s nullglob

# Many projects keep tool settings inside a manifest instead of a separate file.
# Appends "<file>[tool,...]" to EMBEDDED for each tool the pattern finds.
EMBEDDED=()
find_embedded() {
  local file="$1" pattern="$2" tools
  [[ -f "$TARGET_ABS/$file" ]] || return 0
  tools="$(grep -Eo "$pattern" "$TARGET_ABS/$file" | tr -d '"[]' | sed -E 's/^tool\.//; s/[.>=<~^ ].*$//' | sort -u | paste -sd, - || true)"
  [[ -n "$tools" ]] && EMBEDDED+=("$file[$tools]")
  return 0
}

check_any "Pillar 1: Package Manifest" \
  "package.json" "pyproject.toml" "requirements*.txt" "setup.py" "setup.cfg" "go.mod" "Cargo.toml" "build.gradle.kts" "build.gradle" "pom.xml" "pubspec.yaml" "Package.swift" "*.sln" "*.csproj"

check_any "Pillar 1: Lockfile" \
  "pnpm-lock.yaml" "bun.lock" "bun.lockb" "package-lock.json" "yarn.lock" "uv.lock" "poetry.lock" "go.sum" "Cargo.lock" "gradle.lockfile" "pubspec.lock"

check_any "Pillar 2: Monorepo / Template" \
  "pnpm-workspace.yaml" "turbo.json" "nx.json" ".copier-answers.yml"

check_any "Pillar 3: Dev Env & Reproducibility" \
  "mise.toml" ".mise.toml" ".tool-versions" ".nvmrc" ".python-version" "rust-toolchain.toml" ".editorconfig" ".devcontainer/devcontainer.json" "compose.yaml" "docker-compose.yml" "Makefile" "justfile" "Taskfile.yml" ".env.example"

# Rust and Go ship their formatter, linter and test runner with the toolchain.
[[ -f "$TARGET_ABS/Cargo.toml" ]] && EMBEDDED+=("Cargo.toml[built-in: rustfmt,clippy]")
[[ -f "$TARGET_ABS/go.mod" ]] && EMBEDDED+=("go.mod[built-in: gofmt,go vet]")
find_embedded "pyproject.toml" '\[tool\.(ruff|black|pyright|mypy|basedpyright)[]\.]'
find_embedded "package.json" '"(eslint|prettier|@biomejs/biome|typescript|oxlint)"'
check_any "Pillar 4: Format / Lint / Types" \
  "biome.json" "biome.jsonc" "eslint.config.*" ".eslintrc*" ".prettierrc*" "tsconfig.json" "ruff.toml" ".ruff.toml" "pyrightconfig.json" "mypy.ini" ".golangci.yml" ".golangci.yaml" "clippy.toml" "detekt.yml" "analysis_options.yaml" ".dependency-cruiser.*"

[[ -f "$TARGET_ABS/Cargo.toml" ]] && EMBEDDED+=("Cargo.toml[built-in: cargo test]")
[[ -f "$TARGET_ABS/go.mod" ]] && EMBEDDED+=("go.mod[built-in: go test]")
find_embedded "pyproject.toml" '\[tool\.pytest[]\.]|"pytest[^"]*"'
find_embedded "package.json" '"(vitest|jest|mocha|@playwright/test)"'
check_any "Pillar 5: Testing Config" \
  "vitest.config.*" "jest.config.*" "playwright.config.*" "pytest.ini" "conftest.py"

check_any "Pillar 6: Git & Hooks" \
  ".git" ".gitignore" "lefthook.yml" ".pre-commit-config.yaml" ".husky" ".github/PULL_REQUEST_TEMPLATE.md" ".github/CODEOWNERS"

check_any "Pillar 7: Security & Supply Chain" \
  ".gitleaks.toml" "renovate.json" ".github/renovate.json" ".github/dependabot.yml" "deny.toml"

check_any "Pillar 8: CI/CD & Release" \
  ".github/workflows/*.yml" ".github/workflows/*.yaml" ".gitlab-ci.yml" "Dockerfile" ".dockerignore" "release-please-config.json" ".changeset/config.json" ".goreleaser.yaml"

check_any "Pillar 10: Docs & AI Governance" \
  "README.md" "LICENSE" "CONTRIBUTING.md" "AGENTS.md" "CLAUDE.md" "GEMINI.md" "docs/adr" ".agents"
