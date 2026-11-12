---
name: project-instructions
description: >-
  Create, audit, slim down, validate, and synchronize AI coding agent project
  instructions across multi-agent ecosystems (AGENTS.md, CLAUDE.md, .claude/rules,
  GEMINI.md, .agents/rules, .cursor/rules, .github/copilot-instructions.md,
  .windsurfrules). Use when the user asks to set up project guidelines, review or
  refactor bloated rules, check stale paths or commands, prevent context rot, or
  sync instructions across multiple AI tools.
---

# Project Instructions Architect & Auditor

Design, audit, slim down, and synchronize repository instructions across **Universal (`AGENTS.md`, read by Codex and most agents)**, **Claude Code (`CLAUDE.md`, `.claude/rules`)**, **Google Antigravity (`GEMINI.md`, `.agents/rules`)**, **Cursor (`.cursor/rules/*.mdc`)**, **GitHub Copilot (`.github/copilot-instructions.md`, `.github/instructions`)**, and **Windsurf (`.windsurf/rules`)**.

## Core Philosophy

1. **Less is more**: Auto-generated codebase summaries and directory trees lower agent task success and inflate token costs by 20–34%. Target **60–150 lines** for root always-on instructions.
2. **The deletion test**: Keep a line in an always-on file only if deleting it would plausibly cause a mistake the agent cannot avoid by reading the codebase.
3. **Never send an LLM to do a linter's job**: Formatting and style belong in deterministic linters/formatters, and non-negotiable safety blocks belong in **hooks** (`.claude/settings.json`, `.agents/hooks.json`). Prose is advisory; tools are enforced.
4. **Progressive disclosure**: Universal commands and boundaries go in root `AGENTS.md`, path-specific conventions in **scoped rules**, and multi-step procedures in **skills** (`SKILL.md`), so each costs tokens only when relevant.
5. **Single source of truth**: Copy-pasted multi-tool monoliths drift apart. Anchor on `AGENTS.md` plus thin tool bridges (for example, `@AGENTS.md` in `CLAUDE.md`).

## Stay Within the Request

Change only the instruction files the request is about. Hooks, scoped rules, files for other AI tools, and settings changes are often good ideas, but they add moving parts the team did not ask for and may not want to maintain. When one would clearly help (for example, a hook to protect migrations), recommend it in the report with the exact change instead of creating it, unless the user asked for that kind of enforcement.

## The Auditor

Run the bundled static auditor (Python 3 standard library only) from this skill's directory:

```bash
python3 <this skill's directory>/scripts/audit_instructions.py <repo> [--json] [--strict]
```

`--json` emits machine-readable findings; `--strict` also fails on warnings. Exit code 1 means errors (or warnings under `--strict`).

---

## Step 1: Select the Operating Mode

Classify the request into one of four workflows and load only the files it needs:

| Mode | When to Use | Required Reference(s) & Tools |
| :--- | :--- | :--- |
| **1. Bootstrap (`init`)** | Repo has no agent instructions (or the user wants a clean-slate setup) | Read [content-rubric.md](references/content-rubric.md) and [templates.md](assets/templates.md). Read [multi-agent-matrix.md](references/multi-agent-matrix.md) if configuring 2+ tools. |
| **2. Audit & Diet (`audit`)** | User wants to check, critique, lint, or slim down existing instruction files | Run [audit_instructions.py](scripts/audit_instructions.py) first, then read [content-rubric.md](references/content-rubric.md). |
| **3. Multi-Agent Sync (`sync`)** | Repo has fragmented or conflicting files across Claude, Cursor, Copilot, Gemini, or `AGENTS.md` | Run [audit_instructions.py](scripts/audit_instructions.py), then read [multi-agent-matrix.md](references/multi-agent-matrix.md) and [templates.md](assets/templates.md). |
| **4. Evolve (`evolve`)** | User wants to add or update a rule after an agent mistake or codebase change | Read [content-rubric.md](references/content-rubric.md) (Section 1 and the Section 4 layer routing matrix). |

---

## Step 2: Execute the Selected Workflow

### Mode 1: Bootstrap (`init`)
1. **Inspect concrete repo signals instead of guessing**:
   - Lockfiles (`pnpm-lock.yaml`, `yarn.lock`, `bun.lock*`, `package-lock.json`, `uv.lock`, `Cargo.lock`, `go.mod`) and manifests (`package.json`, `pyproject.toml`, `Makefile`, `turbo.json`).
   - Existing linters/formatters (`biome.json`, `eslint.config.*`, `ruff.toml`, `.prettierrc*`), so formatting rules are never repeated in prose.
   - Non-obvious architectural boundaries (monorepo package roles, custom API/logger wrappers, generated or immutable folders).
2. **Pick target tools and prose language**: If unclear, ask which AI tools the team uses. Write the instruction files in the language the repository already uses for its docs and code comments (English when there is no signal), not automatically in the language of the chat: the files are read by every teammate and every agent, while the chat is only with this user. Use another language only when the user asks for it. Keep replying to the user in their conversation language.
3. **Draft a minimal architecture**:
   - Draft root `AGENTS.md` (**40–120 lines**) from [templates.md](assets/templates.md): exact install/build/lint/**single-test** commands, stack anchors, module boundaries, 3–5 project gotchas, and doc pointers. If library versions or current conventions matter, search the web or Context7 when available rather than relying on memory.
   - Leave out `tree` output, generic SOLID/clean-code clichés, and pasted boilerplate; they cost tokens every turn and rot.
   - Add thin bridges (`CLAUDE.md` containing `@AGENTS.md`, a `.gitignore` entry for `*.local.md`, optional scoped rules) per [multi-agent-matrix.md](references/multi-agent-matrix.md).
4. **Verify**: Run the auditor on the workspace and fix any warnings or errors before finishing.

### Mode 2: Audit & Diet (`audit`)
1. **Run the static audit**: `python3 <this skill's directory>/scripts/audit_instructions.py <repo> --json`.
2. **Classify semantically** against [content-rubric.md](references/content-rubric.md). Put every section or rule into:
   - **Keep**: high-signal, non-inferable commands, boundaries, gotchas.
   - **Fix**: stale file paths, dead `npm`/`make` scripts, lockfile mismatches, broken frontmatter.
   - **Delete**: generic filler, standard framework tutorials, full directory trees.
   - **Migrate**: formatting → linter; >20-line procedures → `SKILL.md`; file-type rules → scoped rules; critical safety blocks → hooks (`.claude/settings.json`, `.agents/hooks.json`); personal paths → `*.local.md` or user-level config.
3. **Present a scorecard and plan before destructive edits**: Show current vs. projected line/token counts, concrete findings, and the Keep / Fix / Delete / Migrate breakdown. Get the user's confirmation before deleting legacy files or cutting major sections, because removed rules may encode knowledge only the team has. Then apply the changes and re-run the auditor to confirm a clean pass.

### Mode 3: Multi-Agent Sync (`sync`)
1. **Run the static audit** (`--json`) to inventory all discovered rule files, token budgets, frontmatter errors, and unbridged duplicates.
2. **Resolve conflicts against ground truth**: When two files disagree (for example, `CLAUDE.md` says `npm test` while `.cursorrules` says `pnpm vitest`), check the actual lockfiles, `package.json`, and directory structure on disk.
3. **Consolidate using [multi-agent-matrix.md](references/multi-agent-matrix.md)**:
   - Unify universal rules in root `AGENTS.md` (no YAML frontmatter).
   - Replace duplicated `CLAUDE.md` monoliths with `@AGENTS.md`, keeping only genuinely Claude-specific notes.
   - Migrate legacy `.cursorrules` / `.windsurfrules` into `AGENTS.md` plus properly scoped `.cursor/rules/*.mdc` / `.windsurf/rules/*.md`.
   - When mirroring path-scoped rules across ecosystems, use each tool's exact frontmatter: `paths` for `.claude/rules/*.md`, `trigger`/`globs` for `.agents/rules/*.md`, `globs`/`alwaysApply` for `.cursor/rules/*.mdc`, `applyTo` for `.github/instructions/*.instructions.md`.
   - List `CLAUDE.local.md` and `*.local.md` in `.gitignore`.
4. **Verify**: Re-run the auditor with `--strict` to confirm zero schema, path, or duplication issues.

### Mode 4: Evolve (`evolve`)
1. **Apply the two-strike and deletion tests**: Is the failure a recurring pattern, and could the agent not have inferred the fix from code?
2. **Route to the cheapest reliable layer** ([content-rubric.md](references/content-rubric.md) Section 4):
   - Can ESLint/Biome/Ruff/TypeScript catch it deterministically? → Add a lint rule (0 tokens).
   - Is it a zero-exception safety block or mandatory pre-stop check? → Configure a hook (`PreToolUse` / `Stop`, 0 tokens).
   - Does it apply only to specific files or packages? → Add it to a subdirectory `AGENTS.md` or a glob-scoped rule.
   - Is it a multi-step workflow? → Extract it to a skill (`.agents/skills/<name>/SKILL.md` or `.claude/skills/<name>/SKILL.md`).
   - Otherwise, add **1–3 crisp, falsifiable bullet lines** to root `AGENTS.md`, prune any rule it supersedes, and run the auditor.
