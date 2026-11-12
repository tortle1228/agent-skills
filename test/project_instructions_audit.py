#!/usr/bin/env python3
"""Builds broken-repo and clean-repo fixtures in a temporary directory and asserts audit_instructions.py behavior.

Usage: python3 test/project_instructions_audit.py <path/to/audit_instructions.py>
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile



def write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def setup_broken_repo(root: pathlib.Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    write(root / "pnpm-lock.yaml", "lockfileVersion: '9.0'\n")
    write(
        root / "package.json",
        json.dumps({"name": "broken-fixture", "scripts": {"build": "tsc", "test": "vitest"}}),
    )
    write(root / "Makefile", "build:\n\techo ok\n")

    code_bloat = "\n".join(["```ts"] + [f"const line{i} = {i};" for i in range(18)] + ["```"])
    filler_lines = "\n".join([f"- Extra rule bullet {i} for root monolith size test." for i in range(15)])

    write(
        root / "AGENTS.md",
        f"""---
trigger: always_on
---
# Broken Instructions

- Always write clean, maintainable code and use meaningful variable names.
- Use 2 spaces for indentation and use single quotes.
- Install deps with `npm install` and run `pnpm run test:nonexistent` or `make deploy-missing`.
- Always call `src/deleted/legacyClient.ts` and read [Webhook Spec](docs/missing-webhook.md).
- NEVER modify files in migrations/ or production!
- Load local config from `/home/devuser/secret-config/env.json`.
- Test AWS key: AKIAIOSFODNN7EXAMPLE

{filler_lines}

{code_bloat}
""",
    )

    claude_extra = "\n".join([f"- Duplicate standalone Claude instruction {i}" for i in range(28)])
    write(
        root / "CLAUDE.md",
        f"""# Standalone Duplicate Claude Rules
@docs/nonexistent-import.md
{claude_extra}
""",
    )
    write(root / "CLAUDE.local.md", "# Unignored local override\n")
    write(root / ".cursorrules", "Legacy cursor rules content\n")
    write(
        root / ".agents/rules/bad-glob.md",
        """---
trigger: glob
description: "Missing globs field"
---
Body
""",
    )
    write(
        root / ".github/instructions/bad-copilot.instructions.md",
        """---
description: "Missing applyTo"
---
Body
""",
    )
    write(
        root / ".cursor/rules/unreachable.mdc",
        """---
alwaysApply: false
---
Body
""",
    )


def setup_clean_repo(root: pathlib.Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    write(root / "pnpm-lock.yaml", "lockfileVersion: '9.0'\n")
    write(
        root / "package.json",
        json.dumps(
            {
                "name": "clean-fixture",
                "scripts": {
                    "build": "tsc",
                    "test": "vitest",
                    "typecheck": "tsc --noEmit",
                    "lint": "biome check .",
                },
            }
        ),
    )
    write(root / ".gitignore", "node_modules/\nCLAUDE.local.md\n*.local.md\n")
    write(root / "src/lib/apiClient.ts", "export const apiClient = {};\n")
    write(root / "src/ui/tokens.css", ":root { --bg: #fff; }\n")
    write(root / "migrations/0001_init.sql", "-- initial schema\n")
    write(root / "docs/webhooks.md", "# Webhook Idempotency\n")
    write(
        root / ".agents/hooks.json",
        json.dumps(
            {
                "immutable-migrations": {
                    "PreToolUse": [
                        {
                            "matcher": "edit_file|write_file",
                            "hooks": [{"command": "./scripts/guard-migrations.sh"}],
                        }
                    ]
                }
            }
        ),
    )

    write(
        root / "AGENTS.md",
        """# Clean Repository Instructions

## Commands
- Install: `pnpm install` (never run `npm install` or `yarn install`)
- Build & Typecheck: `pnpm build && pnpm typecheck`
- Lint: `pnpm lint`
- Single Test: `pnpm vitest run <path/to/file.test.ts>`

## Architecture & Constraints
- All outbound HTTP calls must use `src/lib/apiClient.ts` instead of raw `fetch`.
- Existing files in `migrations/` are immutable (enforced by `.agents/hooks.json`).
- Before changing webhook handlers, review [docs/webhooks.md](docs/webhooks.md).
""",
    )
    write(root / "CLAUDE.md", "@AGENTS.md\n")
    write(root / "CLAUDE.local.md", "# Personal local notes (/home/myuser/sandbox allowed here)\n")

    write(
        root / ".agents/rules/ui.md",
        """---
trigger: glob
globs: "src/ui/**/*.tsx"
description: "UI token constraints"
---
- Use semantic variables from `src/ui/tokens.css`.
""",
    )
    write(
        root / ".claude/rules/ui.md",
        """---
paths:
  - "src/ui/**/*.tsx"
---
- Use semantic variables from `src/ui/tokens.css`.
""",
    )
    write(
        root / ".cursor/rules/ui.mdc",
        """---
description: "UI token constraints"
globs: ["src/ui/**/*.tsx"]
alwaysApply: false
---
- Use semantic variables from `src/ui/tokens.css`.
""",
    )
    write(
        root / ".github/instructions/ui.instructions.md",
        """---
applyTo: "src/ui/**/*.tsx"
description: "UI token constraints"
---
- Use semantic variables from `src/ui/tokens.css`.
""",
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: project_instructions_audit.py <path/to/audit_instructions.py>", file=sys.stderr)
        return 2
    auditor = pathlib.Path(sys.argv[1]).resolve()
    if not auditor.is_file():
        print(f"Auditor not found: {auditor}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="project-instructions-audit-") as base:
        return run(auditor, pathlib.Path(base))


def run(auditor: pathlib.Path, base: pathlib.Path) -> int:
    broken_dir = base / "broken-repo"
    clean_dir = base / "clean-repo"
    setup_broken_repo(broken_dir)
    setup_clean_repo(clean_dir)

    # 1. Run against broken-repo
    proc_broken = subprocess.run(
        [sys.executable, str(auditor), str(broken_dir), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc_broken.returncode == 1, f"Expected exit code 1 for broken-repo, got {proc_broken.returncode}"
    broken_data = json.loads(proc_broken.stdout)
    found_codes = {f["code"] for f in broken_data["findings"]}

    expected_codes = {
        "UNSUPPORTED_FRONTMATTER",
        "STALE_REPO_PATH",
        "STALE_LINK_PATH",
        "STALE_IMPORT_PATH",
        "DEAD_PACKAGE_SCRIPT",
        "DEAD_MAKE_TARGET",
        "LOCKFILE_MANAGER_MISMATCH",
        "MISPLACED_LINTER_RULE",
        "GENERIC_FILLER_RULE",
        "PROSE_ONLY_SAFETY_GUARD",
        "HARDCODED_LOCAL_PATH",
        "POTENTIAL_SECRET_EXPOSURE",
        "INLINE_CODE_BLOAT",
        "UNBRIDGED_MULTI_TOOL_DUPLICATION",
        "UNIGNORED_LOCAL_OVERRIDE",
        "LEGACY_RULE_FILE",
        "MISSING_FRONTMATTER_FIELD",
        "UNREACHABLE_CURSOR_RULE",
    }
    missing = expected_codes - found_codes
    assert not missing, f"Missing expected finding codes: {missing}\nActual: {sorted(found_codes)}"
    print(f"PASS broken-repo check passed! Detected all {len(expected_codes)} expected defect categories ({len(broken_data['findings'])} total findings).")

    # 2. Run against clean-repo with --strict
    proc_clean = subprocess.run(
        [sys.executable, str(auditor), str(clean_dir), "--strict"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_clean.returncode != 0:
        print("FAIL clean-repo failed --strict audit:\n", proc_clean.stdout, proc_clean.stderr)
        return 1
    print("PASS clean-repo --strict check passed with 0 errors and 0 warnings!")
    print("\n--- Sample Clean Repo Markdown Report ---")
    print(proc_clean.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
