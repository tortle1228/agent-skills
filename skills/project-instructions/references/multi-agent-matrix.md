# Multi-Agent Ecosystem Specification & Synchronization Matrix

Use this reference during **Multi-Agent Sync (`sync`)**, **Bootstrap (`init`)**, and **Audit (`audit`)** workflows to accurately configure, validate, and bridge project instructions across AI coding tools without creating rule drift.

---

## 1. Cross-Tool File & Scoping Specification (2025–2026)

| Ecosystem | Always-On Root File(s) | Hierarchical Subdir Support? | Scoped / Modular Rules Path | Scoped Frontmatter Schema | Local / Gitignored Personal Override | Hooks & Hard Enforcement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Universal Standard** (Codex and others) | `AGENTS.md` | **Yes** (walks up from CWD to repo root) | Subdirectory `AGENTS.md` | *None* (plain Markdown only; do not add YAML frontmatter) | Tool-dependent | Tool-dependent |
| **Google Antigravity / Gemini** | `GEMINI.md`, `AGENTS.md` | **Yes** (`GEMINI.md` & `AGENTS.md` in any dir) | `.agents/rules/*.md` (also `_agents/rules/*.md`) | `trigger: always_on \| model_decision \| glob`<br>`globs: "*.tsx, src/ui/**"`<br>`description: "..."` | `~/.gemini/config/` (global machine-local) | `.agents/hooks.json` (`SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`) |
| **Claude Code** | `CLAUDE.md` or `.claude/CLAUDE.md` | **Yes** (subdir `CLAUDE.md` loaded on demand) | `.claude/rules/*.md` | `paths:` (YAML list or string of glob patterns, e.g. `["src/api/**/*.ts"]`) | `CLAUDE.local.md` (must be in `.gitignore`) | `.claude/settings.json` (`permissions.deny`, `hooks`: `PreToolUse`, `PostToolUse`, `Stop`) |
| **Cursor** | `AGENTS.md`, `.cursor/rules/*.mdc` (`alwaysApply: true`) *(Legacy: `.cursorrules`)* | **Yes** (`AGENTS.md` & nested `.cursor/rules/`) | `.cursor/rules/*.mdc` (or `*.md`) | `description: "..."`<br>`globs: ["**/*.tsx"]` (or comma string)<br>`alwaysApply: true \| false` | Cursor User Rules (IDE settings) | Cursor Permissions / Sandbox settings |
| **GitHub Copilot** | `.github/copilot-instructions.md`, `AGENTS.md` | `AGENTS.md` supported by Copilot coding agent | `.github/instructions/*.instructions.md` | `applyTo: "**/*.ts,**/*.tsx"`<br>`description: "..."` (optional) | Personal GitHub Copilot custom instructions | GitHub Actions / Branch protection / Environment gates |
| **Windsurf** | `AGENTS.md`, `.windsurf/rules/*.md` *(Legacy: `.windsurfrules`)* | **Yes** (`AGENTS.md` / workspace rules) | `.windsurf/rules/*.md` | `trigger: always_on \| model_decision \| glob`<br>`globs: ...`<br>`description: ...` | Global Windsurf rules (`global_rules.md`) | Cascade command allow/deny lists |

---

## 2. Platform-Specific Limits & Nuances

### Google Antigravity
- **Standalone `GEMINI.md` / `AGENTS.md`**: Must **not** contain YAML frontmatter. Always active for their directory subtree. If both exist in the same directory, verify they do not contradict; prefer `AGENTS.md` as the shared cross-tool file unless Gemini-only overrides are needed.
- **Per-File Byte Cap**: **24,000 bytes (24 KB)** after expanding `@`-mention file includes (`@[label]` followed by the target path in parentheses). Anything above 24 KB is truncated on line boundaries.
- **Aggregate Rules Token Budget**: **20,000 tokens** across all `always_on` and global rules. Over-budget rules are demoted to file path pointers.
- **Scoped Rules (`.agents/rules/*.md`)**:
  - `trigger: always_on` — injected every turn (counts against 20k budget).
  - `trigger: glob` — requires `globs` field; injected only when matching files are touched.
  - `trigger: model_decision` — requires clear `description` field; body loaded only when task semantically matches.

### Claude Code
- **`@path` Imports**: `CLAUDE.md` natively expands `@path/to/file` imports (e.g., `@AGENTS.md` or `@docs/testing.md`, up to 5 hops). Imports inside markdown code spans/blocks are ignored.
- **`CLAUDE.local.md` Governance Trap**: Ensure `CLAUDE.local.md` and `*.local.md` are listed in `.gitignore` so personal paths or experimental prompts never leak into PRs.
- **Path-Scoped Rules (`.claude/rules/*.md`)**: Files without `paths:` frontmatter load unconditionally; files with `paths: ["packages/api/**"]` load only when working with matching files.

### Cursor
- **Deprecate `.cursorrules`**: Root `.cursorrules` is legacy and lacks scoping. Migrate its contents: universal context into root `AGENTS.md`, and file-specific rules into `.cursor/rules/<topic>.mdc` with `alwaysApply: false` and explicit `globs`.
- **Agent-Requested vs Auto-Attached Rules in `.mdc`**:
  - **Always**: `alwaysApply: true` (use sparingly!)
  - **Auto-Attached (Glob)**: `alwaysApply: false` + `globs: ["src/ui/**/*.tsx"]`
  - **Agent-Requested (Semantic)**: `alwaysApply: false`, omit `globs`, provide a crisp `description` so Cursor attaches it when relevant.

### GitHub Copilot
- Keep `.github/copilot-instructions.md` concise or point/align it with `AGENTS.md`.
- Scoped files **must** end with `.instructions.md` inside `.github/instructions/` and specify `applyTo` in YAML frontmatter (e.g., `applyTo: "src/db/**/*.sql"`).

---

## 3. Synchronization Architectures (Preventing Multi-Tool Drift)

The #1 multi-agent anti-pattern is maintaining separate, copy-pasted 200-line instruction files in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and `.github/copilot-instructions.md`. Within weeks, commands and conventions diverge.

Choose **one** of these three drift-free architectures based on team tooling:

### Architecture A: `AGENTS.md` Hub + Thin Bridges (Recommended Default)
Best for repositories used with 2+ coding agents (Codex, Claude Code, Cursor, Copilot, Antigravity).

1. **`AGENTS.md` (Single Source of Truth, 60–150 lines)**: Holds all shared commands, architecture boundaries, stack anchors, and gotchas. (Codex, Cursor, Windsurf, Antigravity, and Copilot Agent read `AGENTS.md` natively; Claude Code reads it through the bridge below.)
2. **`CLAUDE.md` (Thin Bridge, 1–10 lines)**:
   ```markdown
   @AGENTS.md
   ```
   *(Add Claude-only notes below `@AGENTS.md` only if strictly necessary.)*
3. **`.github/copilot-instructions.md` (Optional Thin Bridge)**: Only create if team members use IDE Copilot Chat versions that do not yet ingest `AGENTS.md` in their workflow; keep it concise and structurally identical to `AGENTS.md` core commands/constraints, or generate/check parity with `audit_instructions.py`.
4. **Delete Redundant Monoliths**: Remove legacy `.cursorrules`, `.windsurfrules`, and duplicate `GEMINI.md` if `AGENTS.md` already covers everything.

### Architecture B: Shared Reference Docs + Tool-Native Scoped Triggers
Best for large codebases or monorepos with heavy domain-specific rules (e.g., strict Design System rules, SQL/ORM rules, Security rules) across multiple tools.

1. Keep canonical domain rule content in `docs/agent-rules/<domain>.md` (plain Markdown, zero tool lock-in) **or** inside subdirectory `packages/<pkg>/AGENTS.md`.
2. In tools requiring directory-specific frontmatter wrappers (`.agents/rules/`, `.claude/rules/`, `.cursor/rules/`, `.github/instructions/`), create tiny 5–10 line wrapper files containing **only** the tool's native YAML frontmatter (`trigger`/`globs`, `paths`, `applyTo`) and either a concise summary or `@docs/agent-rules/<domain>.md` / file pointer.

### Architecture C: Monorepo Hierarchical `AGENTS.md`
Best for `pnpm` / `turborepo` / `nx` / polyglot monorepos (`apps/web`, `services/api`, `crates/worker`).

1. **Root `AGENTS.md` (<100 lines)**: Workspace topology, workspace-filtered runner commands (`pnpm --filter <pkg> test`), cross-package import rules.
2. **Package `apps/<name>/AGENTS.md` (<80 lines each)**: Local framework stack, local test/migration commands, package-specific gotchas. Loaded only when an agent operates inside that package directory.

---

## 4. Conflict Resolution Checklist During `sync`

When merging or reconciling existing multi-tool files:
1. **Verify against Lockfiles & Manifests First**: If `CLAUDE.md` says `npm run test` and `.cursorrules` says `pnpm vitest`, inspect `pnpm-lock.yaml` + `package.json` on disk—trust the codebase, never the older prose.
2. **Compare Timestamps & Git Blame**: Newer rules added after recent migrations supersede older rules referencing deleted folders.
3. **Preserve Intentional Tool-Specific Capabilities**: Do not erase valid `.claude/settings.json` hooks or `.agents/hooks.json` configs while consolidating prose files—keep hooks in their native JSON configs.
4. **Backup Before Deleting Legacy Files**: Summarize every rule absorbed or dropped before deleting `.cursorrules` or duplicate `GEMINI.md`/`CLAUDE.md` prose, and confirm with the user.
