#!/usr/bin/env python3
"""Static auditor and validator for multi-agent project instructions.

Scans a repository for AGENTS.md, GEMINI.md, CLAUDE.md, .agents/rules,
.claude/rules, .cursor/rules (.cursorrules), .github/copilot-instructions.md
(.github/instructions), and .windsurfrules (.windsurf/rules).

Usage: python3 audit_instructions.py <repo> [--json] [--strict]

Performs 7 deterministic checks using only the Python 3 standard library:
  1. Size, line count, token budget, and inline code-fence ratio
  2. Ecosystem-specific YAML frontmatter schema validation
  3. Stale file/directory path & @import link detection
  4. Dead package.json / Makefile script commands & lockfile manager drift
  5. Anti-pattern heuristics (linter rules, generic filler, prose-only guards)
  6. Cross-tool duplication/drift, legacy files, and .gitignore hygiene
  7. Security secrets & hardcoded local workstation paths

Some heuristics also contain Korean alternatives so instruction files written
in Korean are checked too; those regex literals are data, not documentation.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Any

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    "vendor",
    ".turbo",
    ".cache",
}

STANDARD_REPO_ROOT_DIRS = {
    "src",
    "app",
    "apps",
    "packages",
    "services",
    "libs",
    "lib",
    "scripts",
    "docs",
    "config",
    "prisma",
    "migrations",
    "tests",
    "test",
    "cmd",
    "internal",
    "pkg",
    "crates",
    "tools",
    ".github",
    ".agents",
    ".claude",
    ".cursor",
}

PER_FILE_BYTE_WARN = 18_000
PER_FILE_BYTE_ERROR = 24_000  # Antigravity hard per-file cap
ROOT_LINE_WARN = 150
ROOT_LINE_ERROR = 250
AGGREGATE_TOKEN_WARN = 12_000
AGGREGATE_TOKEN_ERROR = 20_000  # Antigravity defaultRulesBudget
CODE_FENCE_RATIO_WARN = 0.30

NEGATION_RE = re.compile(
    r"\b(never|don't|do\s+not|avoid|forbid|forbidden|ban|banned|instead\s+of|not\s+use|prohibit)\b"
    r"|금지|사용하지\s*마|쓰지\s*마|말\s*것|대신",
    re.IGNORECASE,
)

LINTER_HEURISTIC_PATTERNS = [
    (
        re.compile(
            r"\b(?:use|indent(?:ation)?\s+with)\s+[24]\s+spaces\b|\buse\s+tabs\s+for\s+indentation\b|들여쓰기\s*[24]\s*칸",
            re.IGNORECASE,
        ),
        "Indentation formatting rule belongs in Prettier/Biome/EditorConfig/Ruff, not LLM context.",
    ),
    (
        re.compile(
            r"\b(?:always|never)\s+use\s+semicolons\b|\bno\s+semicolons\b|세미콜론\s*(?:필수|금지|사용하지)",
            re.IGNORECASE,
        ),
        "Semicolon style rule belongs in a deterministic formatter/linter.",
    ),
    (
        re.compile(
            r"\buse\s+(?:single|double)\s+quotes\b|\bprefer\s+(?:single|double)\s+quotes\b|(?:작은|큰)따옴표만?\s*사용",
            re.IGNORECASE,
        ),
        "Quote style rule belongs in a deterministic formatter/linter.",
    ),
    (
        re.compile(
            r"\bsort\s+imports\s+alphabetically\b|import.*알파벳\s*순",
            re.IGNORECASE,
        ),
        "Import sorting belongs in ESLint/Biome/Ruff/isort, not LLM instructions.",
    ),
]

GENERIC_FILLER_PATTERNS = [
    re.compile(r"\bwrite\s+clean(?:,\s*\w+)*\s+code\b", re.IGNORECASE),
    re.compile(r"\buse\s+meaningful\s+(?:variable|function)\s+names\b", re.IGNORECASE),
    re.compile(r"\bfollow\s+solid\s+principles\b", re.IGNORECASE),
    re.compile(r"\bhandle\s+(?:all\s+)?edge\s+cases\s+carefully\b", re.IGNORECASE),
    re.compile(r"클린\s*코드를?\s*작성", re.IGNORECASE),
    re.compile(r"의미\s*있는\s*변수명", re.IGNORECASE),
]

SAFETY_PROSE_RE = re.compile(
    r"\bnever\s+(?:edit|modify|touch|delete|drop|alter)\b.*(?:\bmigrations?\b|\bproduction\b|\.env\b)"
    r"|(?:\bmigrations?\b|마이그레이션|프로덕션|\.env).*(?:절대\s*(?:수정|삭제|변경)\s*금지)",
    re.IGNORECASE,
)

LOCAL_HOME_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\)"
)

SECRET_PATTERNS = [
    (re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}\b"), "API key matching sk-*"),
    (re.compile(r"\bghp_[A-Za-z0-9]{30,}\b"), "GitHub Personal Access Token (ghp_*)"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"), "GitHub Fine-Grained PAT"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS Access Key ID (AKIA*)"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API Key (AIza*)"),
    (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Inline Private Key header",
    ),
]


@dataclasses.dataclass
class Finding:
    severity: str  # "ERROR" | "WARN" | "INFO"
    code: str
    file: str
    line: int | None
    message: str
    suggestion: str


@dataclasses.dataclass
class DiscoveredFile:
    path: pathlib.Path
    rel_path: str
    ecosystem: str  # universal | antigravity | claude | cursor | copilot | windsurf
    role: str  # always_on_root | hierarchical_dir | scoped_rule | legacy_root | local_override
    lines: list[str]
    byte_size: int
    est_tokens: int
    frontmatter: dict[str, Any] | None
    body_start_line: int
    is_always_active: bool


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, Any] | None, int]:
    """Minimal zero-dependency YAML frontmatter parser for instruction rule files."""
    if not lines or lines[0].strip() != "---":
        return None, 1

    end_idx = None
    for idx in range(1, min(len(lines), 80)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return None, 1

    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw in lines[1:end_idx]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_list_key is not None:
            item = stripped[2:].strip().strip("'\"")
            data.setdefault(current_list_key, []).append(item)
            continue

        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_list_key = None
            if not val or val in (">-", ">", "|", "|-"):
                current_list_key = key
                data[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                items = (
                    [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
                    if inner
                    else []
                )
                data[key] = items
            elif val.lower() in ("true", "false"):
                data[key] = val.lower() == "true"
            else:
                data[key] = val.strip("'\"")
        elif current_list_key is not None and isinstance(data.get(current_list_key), list):
            # Folded multiline scalar continuation (e.g., description: >-)
            if not data[current_list_key]:
                data[current_list_key] = stripped
            elif isinstance(data[current_list_key], str):
                data[current_list_key] += " " + stripped
        elif current_list_key is not None and isinstance(data.get(current_list_key), str):
            data[current_list_key] += " " + stripped

    return data, end_idx + 2


def estimate_tokens(byte_size: int) -> int:
    return max(1, round(byte_size / 3.8))


def discover_instruction_files(repo_root: pathlib.Path) -> list[DiscoveredFile]:
    found: dict[pathlib.Path, tuple[str, str]] = {}

    def register(p: pathlib.Path, ecosystem: str, role: str) -> None:
        resolved = p.resolve()
        if resolved.is_file() and resolved not in found:
            found[resolved] = (ecosystem, role)

    # Root explicit checks
    register(repo_root / "AGENTS.md", "universal", "always_on_root")
    register(repo_root / "GEMINI.md", "antigravity", "always_on_root")
    register(repo_root / "CLAUDE.md", "claude", "always_on_root")
    register(repo_root / ".claude" / "CLAUDE.md", "claude", "always_on_root")
    register(repo_root / "CLAUDE.local.md", "claude", "local_override")
    register(repo_root / ".cursorrules", "cursor", "legacy_root")
    register(repo_root / ".windsurfrules", "windsurf", "legacy_root")
    register(repo_root / ".github" / "copilot-instructions.md", "copilot", "always_on_root")

    # Scoped directories
    for rules_dir in (repo_root / ".agents" / "rules", repo_root / "_agents" / "rules"):
        if rules_dir.is_dir():
            for p in sorted(rules_dir.rglob("*.md")):
                register(p, "antigravity", "scoped_rule")

    claude_rules = repo_root / ".claude" / "rules"
    if claude_rules.is_dir():
        for p in sorted(claude_rules.rglob("*.md")):
            register(p, "claude", "scoped_rule")

    cursor_rules = repo_root / ".cursor" / "rules"
    if cursor_rules.is_dir():
        for p in sorted(cursor_rules.rglob("*")):
            if p.suffix in (".mdc", ".md"):
                register(p, "cursor", "scoped_rule")

    copilot_rules = repo_root / ".github" / "instructions"
    if copilot_rules.is_dir():
        for p in sorted(copilot_rules.rglob("*.instructions.md")):
            register(p, "copilot", "scoped_rule")

    windsurf_rules = repo_root / ".windsurf" / "rules"
    if windsurf_rules.is_dir():
        for p in sorted(windsurf_rules.rglob("*.md")):
            register(p, "windsurf", "scoped_rule")

    # Walk subdirectories for hierarchical AGENTS.md / GEMINI.md / CLAUDE.md / *.local.md
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORED_DIRS
            and not (pathlib.Path(root) == repo_root and d in {".agents", "_agents", ".claude", ".cursor", ".github", ".windsurf"})
        ]
        root_path = pathlib.Path(root)
        is_root = root_path.resolve() == repo_root.resolve()
        for fname in files:
            fpath = root_path / fname
            if fname == "AGENTS.md":
                register(fpath, "universal", "always_on_root" if is_root else "hierarchical_dir")
            elif fname == "GEMINI.md":
                register(fpath, "antigravity", "always_on_root" if is_root else "hierarchical_dir")
            elif fname == "CLAUDE.md":
                register(fpath, "claude", "always_on_root" if is_root else "hierarchical_dir")
            elif fname == "CLAUDE.local.md" or fname in ("AGENTS.local.md", "GEMINI.local.md"):
                register(fpath, "claude" if "CLAUDE" in fname else "universal", "local_override")

    results: list[DiscoveredFile] = []
    for resolved_path, (ecosystem, role) in sorted(
        found.items(), key=lambda item: str(item[0].relative_to(repo_root.resolve()))
    ):
        raw_bytes = resolved_path.read_bytes()
        text = raw_bytes.decode("utf-8", errors="replace")
        lines = text.splitlines()
        fm, body_start = parse_frontmatter(lines)

        is_always = role in ("always_on_root", "legacy_root")
        if role == "scoped_rule":
            if ecosystem == "antigravity" and fm and fm.get("trigger") == "always_on":
                is_always = True
            elif ecosystem == "cursor" and fm and fm.get("alwaysApply") is True:
                is_always = True
            elif ecosystem == "claude" and (not fm or not fm.get("paths")):
                is_always = True
            elif ecosystem == "windsurf" and fm and fm.get("trigger") == "always_on":
                is_always = True

        rel = str(resolved_path.relative_to(repo_root.resolve())).replace("\\", "/")
        results.append(
            DiscoveredFile(
                path=resolved_path,
                rel_path=rel,
                ecosystem=ecosystem,
                role=role,
                lines=lines,
                byte_size=len(raw_bytes),
                est_tokens=estimate_tokens(len(raw_bytes)),
                frontmatter=fm,
                body_start_line=body_start,
                is_always_active=is_always,
            )
        )
    return results


def has_deterministic_hooks(repo_root: pathlib.Path) -> bool:
    for hpath in (repo_root / ".agents" / "hooks.json", repo_root / "_agents" / "hooks.json"):
        if hpath.is_file() and hpath.stat().st_size > 2:
            return True
    claude_settings = repo_root / ".claude" / "settings.json"
    if claude_settings.is_file():
        try:
            data = json.loads(claude_settings.read_text(encoding="utf-8"))
            if data.get("hooks") or data.get("permissions", {}).get("deny"):
                return True
        except json.JSONDecodeError:
            pass
    return False


def collect_repo_scripts_and_locks(
    repo_root: pathlib.Path,
) -> tuple[set[str], bool, set[str], bool, set[str]]:
    """Returns (npm_scripts, has_package_json, make_targets, has_makefile, js_lock_managers)."""
    npm_scripts: set[str] = set()
    has_pkg_json = False
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if "package.json" in files:
            has_pkg_json = True
            pkg_file = pathlib.Path(root) / "package.json"
            try:
                pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
                scripts = pkg_data.get("scripts")
                if isinstance(scripts, dict):
                    npm_scripts.update(scripts.keys())
            except (OSError, json.JSONDecodeError):
                pass

    make_targets: set[str] = set()
    makefile = repo_root / "Makefile"
    has_makefile = makefile.is_file()
    if has_makefile:
        for line in makefile.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^([A-Za-z0-9_.-]+)\s*:", line)
            if m and not m.group(1).startswith("."):
                make_targets.add(m.group(1))

    js_managers: set[str] = set()
    if (repo_root / "pnpm-lock.yaml").is_file():
        js_managers.add("pnpm")
    if (repo_root / "yarn.lock").is_file():
        js_managers.add("yarn")
    if (repo_root / "bun.lock").is_file() or (repo_root / "bun.lockb").is_file():
        js_managers.add("bun")
    if (repo_root / "package-lock.json").is_file():
        js_managers.add("npm")

    return npm_scripts, has_pkg_json, make_targets, has_makefile, js_managers


def iter_non_fenced_lines(df: DiscoveredFile) -> tuple[list[tuple[int, str]], int]:
    """Returns ((1-based line_num, line_text) outside code fences, fenced_line_count)."""
    out: list[tuple[int, str]] = []
    in_fence = False
    fence_marker = ""
    fenced_count = 0

    for idx, line in enumerate(df.lines, start=1):
        if idx < df.body_start_line:
            continue
        stripped = line.lstrip()
        m = re.match(r"^(`{3,}|~{3,})", stripped)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0] * len(marker)
                fenced_count += 1
                continue
            if stripped.startswith(fence_marker[0] * len(fence_marker)):
                in_fence = False
                fence_marker = ""
                fenced_count += 1
                continue
        if in_fence:
            fenced_count += 1
        else:
            out.append((idx, line))
    return out, fenced_count


def check_size_and_budget(
    files: list[DiscoveredFile], findings: list[Finding]
) -> int:
    always_on_tokens = 0
    for df in files:
        if df.is_always_active:
            always_on_tokens += df.est_tokens

        if df.byte_size > PER_FILE_BYTE_ERROR:
            findings.append(
                Finding(
                    severity="ERROR",
                    code="BYTE_CAP_EXCEEDED",
                    file=df.rel_path,
                    line=None,
                    message=f"File size is {df.byte_size:,} bytes (exceeds Antigravity 24,000-byte rule cap; trailing content will be truncated).",
                    suggestion="Move procedural runbooks to Skills (.agents/skills/) and domain-specific rules to path-scoped rules.",
                )
            )
        elif df.byte_size > PER_FILE_BYTE_WARN:
            findings.append(
                Finding(
                    severity="WARN",
                    code="BYTE_BUDGET_HIGH",
                    file=df.rel_path,
                    line=None,
                    message=f"File size is {df.byte_size:,} bytes (approaching 24,000-byte per-file limit).",
                    suggestion="Trim redundant prose and replace inline code blocks with living file pointers.",
                )
            )

        line_count = len(df.lines)
        if df.is_always_active:
            if line_count > ROOT_LINE_ERROR:
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="LINE_COUNT_CRITICAL",
                        file=df.rel_path,
                        line=None,
                        message=f"Always-active instruction file has {line_count} lines (recommended: 60-150, critical >{ROOT_LINE_ERROR}).",
                        suggestion="Apply the Deletion Test ('Would the agent fail without this line?') and split path-specific rules into scoped rules.",
                    )
                )
            elif line_count > ROOT_LINE_WARN:
                findings.append(
                    Finding(
                        severity="WARN",
                        code="LINE_COUNT_HIGH",
                        file=df.rel_path,
                        line=None,
                        message=f"Always-active instruction file has {line_count} lines (exceeds 150-line sweet spot).",
                        suggestion="Keep root instructions under 150 lines to prevent attention dilution and token overhead.",
                    )
                )

        _, fenced_count = iter_non_fenced_lines(df)
        if line_count >= 25 and (fenced_count / line_count) > CODE_FENCE_RATIO_WARN:
            pct = int(round((fenced_count / line_count) * 100))
            findings.append(
                Finding(
                    severity="WARN",
                    code="INLINE_CODE_BLOAT",
                    file=df.rel_path,
                    line=None,
                    message=f"{pct}% of lines ({fenced_count}/{line_count}) are inline fenced code blocks.",
                    suggestion="Pointers over Copies: remove pasted code templates (which rot silently) and point to canonical repo files instead.",
                )
            )

    if always_on_tokens > AGGREGATE_TOKEN_ERROR:
        findings.append(
            Finding(
                severity="ERROR",
                code="AGGREGATE_TOKEN_BUDGET_EXCEEDED",
                file="<workspace>",
                line=None,
                message=f"Estimated aggregate always-on tokens (~{always_on_tokens:,}) exceed the 20,000-token budget.",
                suggestion="Convert unconditional rules to glob/path-scoped rules or on-demand Skills, and eliminate multi-tool file duplication.",
            )
        )
    elif always_on_tokens > AGGREGATE_TOKEN_WARN:
        findings.append(
            Finding(
                severity="WARN",
                code="AGGREGATE_TOKEN_BUDGET_HIGH",
                file="<workspace>",
                line=None,
                message=f"Estimated aggregate always-on tokens (~{always_on_tokens:,}) are consuming >60% of the 20,000-token budget.",
                suggestion="Audit always-on files for duplicate instructions across AGENTS.md / CLAUDE.md / GEMINI.md / Copilot.",
            )
        )
    return always_on_tokens


def check_frontmatter_schemas(files: list[DiscoveredFile], findings: list[Finding]) -> None:
    for df in files:
        fm = df.frontmatter
        fname = df.path.name

        if fname in ("AGENTS.md", "GEMINI.md") and df.role in ("always_on_root", "hierarchical_dir"):
            if fm is not None:
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="UNSUPPORTED_FRONTMATTER",
                        file=df.rel_path,
                        line=1,
                        message=f"Standalone {fname} does not support YAML frontmatter (it is always active for its directory).",
                        suggestion="Remove frontmatter from standalone AGENTS.md/GEMINI.md, or move the file into .agents/rules/ if conditional triggers are needed.",
                    )
                )
            continue

        if df.role != "scoped_rule":
            continue

        if df.ecosystem in ("antigravity", "windsurf"):
            if fm is None:
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER",
                        file=df.rel_path,
                        line=1,
                        message=f"Scoped rule in {df.rel_path} is missing YAML frontmatter.",
                        suggestion="Add YAML frontmatter with `trigger: glob | model_decision | always_on`.",
                    )
                )
                continue
            trigger = fm.get("trigger")
            valid_triggers = {"always_on", "model_decision", "glob", "manual"}
            if trigger not in valid_triggers:
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="INVALID_FRONTMATTER_TRIGGER",
                        file=df.rel_path,
                        line=1,
                        message=f"Invalid or missing `trigger: {trigger!r}` (expected one of {sorted(valid_triggers)}).",
                        suggestion="Set `trigger: glob` (with `globs`), `trigger: model_decision` (with `description`), or `trigger: always_on`.",
                    )
                )
            elif trigger == "glob" and not fm.get("globs"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER_FIELD",
                        file=df.rel_path,
                        line=1,
                        message="Rule uses `trigger: glob` but is missing a non-empty `globs` field.",
                        suggestion='Add e.g. `globs: "src/ui/**/*.tsx"` to YAML frontmatter.',
                    )
                )
            elif trigger == "model_decision" and not fm.get("description"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER_FIELD",
                        file=df.rel_path,
                        line=1,
                        message="Rule uses `trigger: model_decision` but is missing a `description` field.",
                        suggestion="Add a clear `description` explaining when the agent should activate this rule.",
                    )
                )

        elif df.ecosystem == "cursor":
            if fm is None:
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER",
                        file=df.rel_path,
                        line=1,
                        message="Cursor rule file is missing YAML frontmatter (`description`, `globs`, `alwaysApply`).",
                        suggestion="Add `.mdc` YAML frontmatter with `alwaysApply: false` and `globs` or `description`.",
                    )
                )
                continue
            always_apply = fm.get("alwaysApply")
            if always_apply is not True and not fm.get("globs") and not fm.get("description"):
                findings.append(
                    Finding(
                        severity="WARN",
                        code="UNREACHABLE_CURSOR_RULE",
                        file=df.rel_path,
                        line=1,
                        message="Cursor rule has neither `alwaysApply: true`, `globs`, nor `description`; it may never attach automatically.",
                        suggestion="Provide `globs` for path auto-attachment or `description` for semantic agent attachment.",
                    )
                )

        elif df.ecosystem == "copilot":
            if fm is None or not fm.get("applyTo"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER_FIELD",
                        file=df.rel_path,
                        line=1,
                        message="GitHub Copilot `.instructions.md` file requires YAML frontmatter with `applyTo`.",
                        suggestion='Add `applyTo: "**/*.ts"` (or target path globs) in YAML frontmatter.',
                    )
                )

        elif df.ecosystem == "claude":
            if fm is not None and "paths" in fm and not fm.get("paths"):
                findings.append(
                    Finding(
                        severity="ERROR",
                        code="MISSING_FRONTMATTER_FIELD",
                        file=df.rel_path,
                        line=1,
                        message="Claude `.claude/rules/` file declares `paths:` in frontmatter, but the value is empty.",
                        suggestion='Provide one or more glob strings under `paths:` or omit frontmatter if unconditional.',
                    )
                )


def _clean_target_path(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"#L\d+(?:-L?\d+)?$", "", cleaned)
    cleaned = re.sub(r":\d+(?:-\d+)?$", "", cleaned)
    if "#" in cleaned:
        cleaned = cleaned.split("#", 1)[0]
    return cleaned.strip()


def _path_exists(repo_root: pathlib.Path, source_file: pathlib.Path, rel_cand: str) -> bool:
    if not rel_cand:
        return True
    p_local = (source_file.parent / rel_cand).resolve()
    p_root = (repo_root / rel_cand.lstrip("/")).resolve()
    return p_local.exists() or p_root.exists()


def _looks_like_concrete_repo_path(cand: str, existing_top_dirs: set[str]) -> bool:
    if not cand or " " in cand or "\t" in cand:
        return False
    if any(ch in cand for ch in ("*", "?", "{", "}", "<", ">", "$", "|", "=", ";", "(", ")", "[", "]")):
        return False
    if "://" in cand or "..." in cand or cand.startswith(("-", "@", "http", "git@", "~")):
        return False
    if cand.startswith(("/Users/", "/home/", "/etc/", "/tmp/", "/var/", "/dev/", "/proc/", "/opt/")):
        return False
    lowered = cand.lower()
    if any(
        tok in lowered
        for tok in ("path/to", "example/", "your-", "<pkg>", "<name>", "<file>", "foo/", "bar/")
    ):
        return False

    if cand.startswith(("./", "../")):
        return True

    if "/" not in cand:
        return False

    norm = cand.lstrip("./")
    first_seg = norm.split("/", 1)[0]
    return first_seg in existing_top_dirs or first_seg in STANDARD_REPO_ROOT_DIRS


def check_stale_paths_and_imports(
    repo_root: pathlib.Path, files: list[DiscoveredFile], findings: list[Finding]
) -> None:
    existing_top_dirs = {
        p.name for p in repo_root.iterdir() if p.is_dir() and p.name not in IGNORED_DIRS
    }

    md_link_re = re.compile(r"@?\[[^\]]*\]\(([^)]+)\)")
    backtick_re = re.compile(r"`([^`]+)`")
    at_import_re = re.compile(r"(?:^|(?<=\s))@([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)")

    for df in files:
        non_fenced, _ = iter_non_fenced_lines(df)
        reported_on_file: set[str] = set()

        for line_num, line in non_fenced:
            # 1. Markdown links and @[label](path)
            for m in md_link_re.finditer(line):
                raw_url = m.group(1).strip().split()[0]
                if raw_url.startswith(("http://", "https://", "mailto:", "#", "conversation://", "file://")):
                    continue
                target = _clean_target_path(raw_url)
                if not target or any(ch in target for ch in ("*", "<", ">", "{", "}")):
                    continue
                if target not in reported_on_file and not _path_exists(repo_root, df.path, target):
                    reported_on_file.add(target)
                    findings.append(
                        Finding(
                            severity="ERROR",
                            code="STALE_LINK_PATH",
                            file=df.rel_path,
                            line=line_num,
                            message=f"Linked path `{target}` does not exist on disk.",
                            suggestion="Update the link to the current file location or remove the stale reference.",
                        )
                    )

            # Strip inline code spans before scanning bare @path imports
            line_without_code = backtick_re.sub(" ", line)
            for m in at_import_re.finditer(line_without_code):
                imp = _clean_target_path(m.group(1))
                # Ignore npm scoped packages like @org/pkg.js unless it has known doc/config extensions or starts with ./
                if imp.endswith((".md", ".mdc", ".txt", ".json", ".yaml", ".yml")) or imp.startswith(("./", "../")):
                    if imp not in reported_on_file and not _path_exists(repo_root, df.path, imp):
                        reported_on_file.add(imp)
                        findings.append(
                            Finding(
                                severity="ERROR",
                                code="STALE_IMPORT_PATH",
                                file=df.rel_path,
                                line=line_num,
                                message=f"Imported `@path` target `@{imp}` does not exist on disk.",
                                suggestion="Fix the `@path` import target so Claude/agent file expansion does not fail silently.",
                            )
                        )

            # 3. Backtick repo path references
            for m in backtick_re.finditer(line):
                cand = _clean_target_path(m.group(1))
                if _looks_like_concrete_repo_path(cand, existing_top_dirs):
                    if cand not in reported_on_file and not _path_exists(repo_root, df.path, cand):
                        reported_on_file.add(cand)
                        findings.append(
                            Finding(
                                severity="ERROR",
                                code="STALE_REPO_PATH",
                                file=df.rel_path,
                                line=line_num,
                                message=f"Referenced repository path `{cand}` does not exist.",
                                suggestion="Update the path after recent directory/file renames or remove obsolete guidance.",
                            )
                        )


def check_commands_and_lockfiles(
    repo_root: pathlib.Path, files: list[DiscoveredFile], findings: list[Finding]
) -> None:
    npm_scripts, has_pkg_json, make_targets, has_makefile, js_managers = (
        collect_repo_scripts_and_locks(repo_root)
    )
    single_js_mgr = next(iter(js_managers)) if len(js_managers) == 1 else None

    explicit_run_re = re.compile(
        r"\b(npm|pnpm|yarn|bun)\s+(?:--filter\s+\S+\s+)?run\s+([A-Za-z0-9_:.-]+)"
    )
    shorthand_script_re = re.compile(
        r"\b(npm|pnpm|yarn|bun)\s+(?:--filter\s+\S+\s+)?(test|build|lint|typecheck|check|format|dev|start)\b"
    )
    mgr_usage_re = re.compile(
        r"\b(npm|pnpm|yarn|bun)\s+(install|ci|add|run|test|build|lint|typecheck|dev|exec|dlx)\b"
    )
    make_cmd_re = re.compile(r"\bmake\s+([A-Za-z0-9_.-]+)")
    backtick_re = re.compile(r"`([^`]+)`")

    for df in files:
        non_fenced, _ = iter_non_fenced_lines(df)
        seen_dead: set[str] = set()
        seen_mgr_mismatch: set[str] = set()

        for line_num, line in non_fenced:
            for m_bt in backtick_re.finditer(line):
                span = m_bt.group(1)
                prefix = line[max(0, m_bt.start() - 48) : m_bt.start()]
                suffix = line[m_bt.end() : min(len(line), m_bt.end() + 24)]
                is_negated_span = bool(
                    NEGATION_RE.search(prefix)
                    or re.match(
                        r"^[\s`'\".,;:은는을를이가도]*?(?:금지|사용하지\s*마|쓰지\s*마|말\s*것|비권장|forbidden|prohibited)",
                        suffix,
                        re.IGNORECASE,
                    )
                )

                if has_pkg_json:
                    for m in explicit_run_re.finditer(span):
                        script_name = m.group(2)
                        if not is_negated_span and script_name not in npm_scripts and script_name not in seen_dead:
                            seen_dead.add(script_name)
                            findings.append(
                                Finding(
                                    severity="ERROR",
                                    code="DEAD_PACKAGE_SCRIPT",
                                    file=df.rel_path,
                                    line=line_num,
                                    message=f"Command `{m.group(0)}` references `{script_name}`, which is not defined in any `package.json` scripts.",
                                    suggestion=f"Update the command to match `package.json` scripts ({', '.join(sorted(list(npm_scripts))[:8]) or 'none defined'}).",
                                )
                            )
                    for m in shorthand_script_re.finditer(span):
                        mgr, script_name = m.group(1), m.group(2)
                        # `bun test` can invoke Bun's built-in test runner even without a `test` script
                        if mgr == "bun" and script_name == "test":
                            continue
                        if not is_negated_span and script_name not in npm_scripts and script_name not in seen_dead:
                            seen_dead.add(script_name)
                            findings.append(
                                Finding(
                                    severity="ERROR",
                                    code="DEAD_PACKAGE_SCRIPT",
                                    file=df.rel_path,
                                    line=line_num,
                                    message=f"Command `{m.group(0)}` invokes `{script_name}`, which is missing from `package.json` scripts.",
                                    suggestion="Verify the script name in `package.json` and update the instruction.",
                                )
                            )

                if single_js_mgr and not is_negated_span:
                    for m in mgr_usage_re.finditer(span):
                        used_mgr = m.group(1)
                        if used_mgr != single_js_mgr and used_mgr not in seen_mgr_mismatch:
                            seen_mgr_mismatch.add(used_mgr)
                            findings.append(
                                Finding(
                                    severity="WARN",
                                    code="LOCKFILE_MANAGER_MISMATCH",
                                    file=df.rel_path,
                                    line=line_num,
                                    message=f"Instruction uses `{used_mgr}` (`{m.group(0)}`), but repository lockfile indicates `{single_js_mgr}`.",
                                    suggestion=f"Align command examples with `{single_js_mgr}` so agents do not generate conflicting lockfiles.",
                                )
                            )

                if has_makefile and not is_negated_span:
                    for m in make_cmd_re.finditer(span):
                        target = m.group(1)
                        if target.startswith("-"):
                            continue
                        key = f"make:{target}"
                        if target not in make_targets and key not in seen_dead:
                            seen_dead.add(key)
                            findings.append(
                                Finding(
                                    severity="ERROR",
                                    code="DEAD_MAKE_TARGET",
                                    file=df.rel_path,
                                    line=line_num,
                                    message=f"Command `make {target}` references a target not found in `Makefile`.",
                                    suggestion="Update `AGENTS.md` to reference an existing Makefile target.",
                                )
                            )


def check_antipatterns_and_hygiene(
    repo_root: pathlib.Path, files: list[DiscoveredFile], findings: list[Finding]
) -> None:
    hooks_configured = has_deterministic_hooks(repo_root)

    for df in files:
        non_fenced, _ = iter_non_fenced_lines(df)

        # Scan all lines (including fenced blocks) for secrets and hardcoded workstation paths
        for line_num, raw_line in enumerate(df.lines, start=1):
            for pat, label in SECRET_PATTERNS:
                if pat.search(raw_line):
                    findings.append(
                        Finding(
                            severity="ERROR",
                            code="POTENTIAL_SECRET_EXPOSURE",
                            file=df.rel_path,
                            line=line_num,
                            message=f"Potential secret detected ({label}).",
                            suggestion="Remove credentials immediately, rotate compromised keys, and reference `.env.example` variable names only.",
                        )
                    )
            if df.role != "local_override":
                m_home = LOCAL_HOME_PATH_RE.search(raw_line)
                if m_home:
                    findings.append(
                        Finding(
                            severity="ERROR",
                            code="HARDCODED_LOCAL_PATH",
                            file=df.rel_path,
                            line=line_num,
                            message=f"Hardcoded workstation home path `{m_home.group(0)}...` found in shared instruction file.",
                            suggestion="Use repository-relative paths, or move machine-specific settings to gitignored `CLAUDE.local.md` / the agent's user-level config.",
                        )
                    )

        # Scan prose lines for anti-pattern heuristics
        for line_num, line in non_fenced:
            for pat, reason in LINTER_HEURISTIC_PATTERNS:
                if pat.search(line):
                    findings.append(
                        Finding(
                            severity="WARN",
                            code="MISPLACED_LINTER_RULE",
                            file=df.rel_path,
                            line=line_num,
                            message=reason,
                            suggestion="Enforce formatting via Biome/ESLint/Prettier/Ruff + pre-commit/PostToolUse hooks and delete this line.",
                        )
                    )
                    break

            for pat in GENERIC_FILLER_PATTERNS:
                if pat.search(line):
                    findings.append(
                        Finding(
                            severity="WARN",
                            code="GENERIC_FILLER_RULE",
                            file=df.rel_path,
                            line=line_num,
                            message="Generic software engineering advice adds noise without repo-specific signal.",
                            suggestion="Delete generic advice or replace it with a concrete, verifiable repository constraint.",
                        )
                    )
                    break

            if not hooks_configured and SAFETY_PROSE_RE.search(line):
                findings.append(
                    Finding(
                        severity="WARN",
                        code="PROSE_ONLY_SAFETY_GUARD",
                        file=df.rel_path,
                        line=line_num,
                        message="Critical safety constraint relies solely on natural-language prose with no hooks/deny config detected.",
                        suggestion="Natural-language instructions are advisory. Enforce hard blocks via `.agents/hooks.json` (`PreToolUse`) or `.claude/settings.json` (`deny`/hooks).",
                    )
                )


def _is_gitignored(repo_root: pathlib.Path, target: pathlib.Path) -> bool:
    gitignore = repo_root / ".gitignore"
    rel_name = target.name
    rel_path = str(target.relative_to(repo_root)).replace("\\", "/")
    if gitignore.is_file():
        for raw in gitignore.read_text(encoding="utf-8", errors="replace").splitlines():
            rule = raw.strip()
            if not rule or rule.startswith("#"):
                continue
            if rule in (rel_name, f"/{rel_path}", rel_path, "*.local.md", "**/*.local.md"):
                return True
    if (repo_root / ".git").exists():
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo_root), "check-ignore", "-q", rel_path],
                check=False,
                capture_output=True,
                timeout=3,
            )
            if proc.returncode == 0:
                return True
        except (OSError, subprocess.SubprocessError):
            pass
    return False


def check_cross_tool_drift_and_legacy(
    repo_root: pathlib.Path, files: list[DiscoveredFile], findings: list[Finding]
) -> None:
    substantive_roots: list[DiscoveredFile] = []

    for df in files:
        if df.role == "legacy_root":
            replacement = (
                "`AGENTS.md` + `.cursor/rules/*.mdc`"
                if df.ecosystem == "cursor"
                else "`AGENTS.md` + `.windsurf/rules/*.md`"
            )
            findings.append(
                Finding(
                    severity="WARN",
                    code="LEGACY_RULE_FILE",
                    file=df.rel_path,
                    line=None,
                    message=f"Legacy root `{df.rel_path}` loads unconditionally without path scoping.",
                    suggestion=f"Migrate shared context to root `AGENTS.md` and file-specific rules to {replacement}.",
                )
            )

        if df.role == "local_override" and not _is_gitignored(repo_root, df.path):
            findings.append(
                Finding(
                    severity="ERROR",
                    code="UNIGNORED_LOCAL_OVERRIDE",
                    file=df.rel_path,
                    line=None,
                    message=f"Local personal override file `{df.rel_path}` is not covered by `.gitignore`.",
                    suggestion="Add `CLAUDE.local.md` and `*.local.md` to `.gitignore` to prevent leaking personal overrides into commits.",
                )
            )

        if df.role == "always_on_root":
            non_empty = [ln for ln in df.lines if ln.strip()]
            body_text = "\n".join(df.lines)
            bridges_to_agents = (
                df.path.name != "AGENTS.md"
                and ("@AGENTS.md" in body_text or "AGENTS.md" in body_text)
                and len(non_empty) <= 25
            )
            if len(non_empty) > 25 and not bridges_to_agents:
                substantive_roots.append(df)

    if len(substantive_roots) >= 2:
        names = ", ".join(df.rel_path for df in substantive_roots)
        findings.append(
            Finding(
                severity="WARN",
                code="UNBRIDGED_MULTI_TOOL_DUPLICATION",
                file="<workspace>",
                line=None,
                message=f"Multiple large standalone root instruction files detected ({names}).",
                suggestion="Consolidate shared context into root `AGENTS.md` as Single Source of Truth, and reduce `CLAUDE.md` to `@AGENTS.md` (plus tool-only notes if needed).",
            )
        )


def format_markdown_report(
    repo_root: pathlib.Path,
    files: list[DiscoveredFile],
    always_on_tokens: int,
    findings: list[Finding],
) -> str:
    out: list[str] = []
    out.append(f"# Project Instructions Audit Report (`{repo_root.name}`)")
    out.append("")
    if not files:
        out.append("No agent instruction files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.agents/rules`, `.cursor/rules`, `.github/copilot-instructions.md`) were found in this workspace.")
        return "\n".join(out)

    out.append("## 1. Discovered Files & Token Budget")
    out.append("")
    out.append("| File | Ecosystem | Role | Always Active | Lines | Bytes | Est. Tokens |")
    out.append("| :--- | :--- | :--- | :--- | ---: | ---: | ---: |")
    for df in files:
        active_str = "Yes" if df.is_always_active else "Scoped/Local"
        out.append(
            f"| `{df.rel_path}` | `{df.ecosystem}` | `{df.role}` | {active_str} | {len(df.lines)} | {df.byte_size:,} | ~{df.est_tokens:,} |"
        )
    out.append("")
    out.append(
        f"- **Aggregate Always-Active Token Estimate**: `~{always_on_tokens:,}` / `20,000` budget ({round(always_on_tokens / 200, 1)}%)"
    )
    out.append("")

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]
    infos = [f for f in findings if f.severity == "INFO"]

    out.append(
        f"## 2. Audit Findings (`{len(errors)}` Errors, `{len(warns)}` Warnings, `{len(infos)}` Info)"
    )
    out.append("")
    if not findings:
        out.append("All static checks passed with zero errors or warnings.")
        return "\n".join(out)

    for f in findings:
        loc = f"`{f.file}:{f.line}`" if f.line else f"`{f.file}`"
        out.append(f"- **[{f.severity}] `{f.code}`** at {loc}: {f.message}")
        out.append(f"  - *Fix*: {f.suggestion}")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static validator and bloat/drift auditor for multi-agent project instruction files."
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="Path to the target repository root (default: current directory).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output structured JSON for programmatic agent consumption.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero exit code on WARN findings as well as ERROR findings.",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.workspace).resolve()
    if not repo_root.is_dir():
        print(f"Error: workspace path does not exist or is not a directory: {repo_root}", file=sys.stderr)
        return 2

    files = discover_instruction_files(repo_root)
    findings: list[Finding] = []

    always_on_tokens = check_size_and_budget(files, findings)
    check_frontmatter_schemas(files, findings)
    check_stale_paths_and_imports(repo_root, files, findings)
    check_commands_and_lockfiles(repo_root, files, findings)
    check_antipatterns_and_hygiene(repo_root, files, findings)
    check_cross_tool_drift_and_legacy(repo_root, files, findings)

    severity_rank = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (severity_rank.get(f.severity, 9), f.file, f.line or 0))

    errors = sum(1 for f in findings if f.severity == "ERROR")
    warns = sum(1 for f in findings if f.severity == "WARN")

    if args.as_json:
        payload = {
            "workspace": str(repo_root),
            "summary": {
                "discovered_files": len(files),
                "always_on_estimated_tokens": always_on_tokens,
                "always_on_budget_tokens": AGGREGATE_TOKEN_ERROR,
                "errors": errors,
                "warnings": warns,
            },
            "files": [
                {
                    "path": df.rel_path,
                    "ecosystem": df.ecosystem,
                    "role": df.role,
                    "is_always_active": df.is_always_active,
                    "lines": len(df.lines),
                    "bytes": df.byte_size,
                    "estimated_tokens": df.est_tokens,
                    "frontmatter": df.frontmatter,
                }
                for df in files
            ],
            "findings": [dataclasses.asdict(f) for f in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_markdown_report(repo_root, files, always_on_tokens, findings))

    if errors > 0 or (args.strict and warns > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
