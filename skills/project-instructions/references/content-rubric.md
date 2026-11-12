# Project Instructions Content Rubric & Layer Routing Guide

Use this rubric during **Bootstrap (`init`)**, **Audit & Diet (`audit`)**, and **Evolve (`evolve`)** workflows to decide what belongs in an always-on instruction file, what should be deleted, and what must move to another layer.

---

## 1. Core Principles (Empirical Consensus)

1. **Less is More (Context Pollution Prevention)**:
   Empirical evaluations (e.g., ETH Zurich & LogicStar.ai, *Evaluating AGENTS.md*, 2026) demonstrate that auto-generated, encyclopedic instruction files **reduce task success rates (~3%)** and **increase token/inference cost by 20–34%** because agents over-explore and dilute attention on redundant summaries.
2. **The Deletion Test**:
   For every single line in an always-on file (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.github/copilot-instructions.md`), ask:
   > *"If I delete this line, will the agent plausibly make a mistake that it could not avoid by inspecting the repository?"*
   If **No**, delete it immediately.
3. **Goldilocks Budget**:
   - **Target**: **60–150 lines** (max ~200 lines / ~800 words) for root always-on files.
   - **Hard Platform Caps**: Antigravity caps individual rule files at **24,000 bytes (24 KB)** and enforces a **20,000-token** aggregate always-on rules budget (demoting excess rules to file pointers).
4. **The Two-Strike Rule**:
   Never add speculative rules *"just in case."* Add a rule only after an agent makes the **same category of mistake twice** in real work, and prune rules when dependencies, folder layouts, or model capabilities make them obsolete.
5. **Pointers over Copies**:
   Never paste multi-line code templates, schema dumps, or full style guides into root instructions. Inline snippets rot silently when source code changes. Reference authoritative living files instead (e.g., *"Follow the error wrapper pattern in `src/lib/http/errors.ts`"*).

---

## 2. What to INCLUDE (High-Signal, Non-Inferable Context)

| Category | What to Write | Concrete Example |
| :--- | :--- | :--- |
| **1. Exact Commands** | Package manager, build, typecheck, lint, and **single-file test** commands with exact flags | ``Run a single test with `pnpm vitest run <file>` (never run full `pnpm test` during iteration).`` |
| **2. Architectural Boundaries** | Layering invariants, domain ownership, forbidden cross-imports | ``Domain logic lives in `src/domains/<name>/`. UI components in `src/ui/` must never import `src/infra/` directly.`` |
| **3. Stack Anchors & Legacy Bans** | Pin versions/paradigms where models often regress to training-corpus defaults | ``Next.js 15 App Router only (never Pages Router). Tailwind v4 CSS-first config (no `tailwind.config.js`).`` |
| **4. Non-Obvious Gotchas** | Internal wrappers, custom env loaders, DB/test quirks | ``Never call `fetch` or `console.log` directly; use `src/shared/apiClient.ts` and `src/shared/logger.ts`.`` |
| **5. Contextual Pointers** | 1-line links to deep docs or canonical reference implementations | ``When adding billing webhooks, read `docs/billing-idempotency.md` first.`` |

---

## 3. What NOT to Include (7 Anti-Patterns & Remediations)

| Anti-Pattern | Detection Signal | Required Action |
| :--- | :--- | :--- |
| **1. Generic Best-Practice Filler** | *"Write clean, maintainable code"*, *"Use meaningful variable names"*, *"Follow SOLID/DRY"*, *"Handle edge cases carefully"* | **Delete**. Frontier models already follow these; generic prose dilutes hard constraints. |
| **2. Language / Framework Tutorials** | Explaining standard React hooks, Python type hints, Go error idioms, REST basics | **Delete**. Keep only rules where your repo **deviates** from standard idioms. |
| **3. Linter / Formatter Rules** | *"Use 2 spaces"*, *"Single quotes"*, *"Always add semicolons"*, *"Sort imports alphabetically"* | **Migrate to Linter/Formatter** (Biome, ESLint, Prettier, Ruff, gofmt) + pre-commit or PostToolUse hook. *Never send an LLM to do a linter's job.* |
| **4. Auto-Generated Directory Trees** | Full `tree` outputs or file-by-file prose descriptions of standard folders (`components/`, `utils/`) | **Delete** (or shrink to 3–5 lines covering only non-obvious top-level boundaries). Agents traverse directories dynamically. |
| **5. Copy-Pasted Code Templates** | >15–20 lines of boilerplate code blocks demonstrating how to write a controller or test | **Replace with File Pointer** (`See src/modules/orders/order.controller.ts for canonical controller structure`). |
| **6. Prose-Only Critical Safety Guards** | *"NEVER edit `migrations/`"*, *"NEVER run destructive SQL or `git push --force`"* with zero programmatic enforcement | **Keep brief warning + Enforce via Hooks/Permissions** (`.claude/settings.json` `deny` / hooks, `.agents/hooks.json` `PreToolUse`). Natural language is advisory, not a security boundary. |
| **7. Secrets, Internal Secrets & Personal Preferences** | Tokens, private URLs, `/Users/<name>/...` paths, or personal communication style preferences in shared VCS files | **Strip immediately**. Move personal preferences to the agent's user-level config (e.g., `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.gemini/config/`) or a gitignored `CLAUDE.local.md`. |

---

## 4. The 5-Layer Progressive Disclosure Routing Matrix

When auditing or adding an instruction, route each requirement to the lowest-token, highest-reliability layer:

| Layer | Mechanism | Token Cost | Deterministic? | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1: Tooling** | Linter, Formatter, Typechecker, CI (`eslint`, `biome`, `ruff`, `tsc`) | **0 tokens** | **Yes (100%)** | Formatting, import sorting, banned AST symbols (e.g., `no-console`, `no-explicit-any`), architectural import boundaries (`eslint-plugin-boundaries`). |
| **Layer 2: Lifecycle Hooks** | `.claude/settings.json`, `.agents/hooks.json` (`PreToolUse`, `PostToolUse`, `Stop`) | **0 tokens** | **Yes (100%)** | Blocking writes to protected paths (`migrations/`, `.env`), blocking dangerous shell commands, auto-running formatters after file edits, verifying tests pass on `Stop`. |
| **Layer 3: Always-On Root** | `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` | **Paid every turn** | Advisory | Repo-wide build/test/lint commands, core stack anchors, top-level module boundaries, 3–5 universal gotchas. |
| **Layer 4: Scoped Rules** | Subdir `AGENTS.md`, `.agents/rules/*.md` (`glob`/`model_decision`), `.claude/rules/*.md` (`paths`), `.cursor/rules/*.mdc` (`globs`), `.github/instructions/*.instructions.md` (`applyTo`) | **Paid only when matched** | Advisory | Frontend-only design token rules, backend-only ORM/SQL rules, test-file mocking conventions, package-specific commands in monorepos. |
| **Layer 5: On-Demand Skills** | `.agents/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md` | **Metadata only (~30 tokens) until invoked** | Procedural | Multi-step runbooks: creating a DB migration, cutting a release, scaffolding a microservice, running end-to-end QA workflows. |

---

## 5. Concrete Refactoring Example (Before vs. After)

### Before (Bloated Monolith — Anti-Pattern)
```markdown
# Project Guidelines
You are an expert senior TypeScript engineer. Always write clean, modular, SOLID code with meaningful variable names and thorough error handling.

## Code Style
- Use 2 spaces for indentation, single quotes, and no trailing semicolons.
- Sort imports: external packages first, then internal `@/` aliases.

## Project Directory Tree
├── src/
│   ├── components/   # React components
│   ├── hooks/        # Custom React hooks
│   ├── utils/        # Utility functions
... (80 lines of tree output)

## Database Migration Procedure
Step 1: Edit schema.prisma...
Step 2: Run npx prisma migrate dev --name ...
... (60 lines of step-by-step runbook + pasted SQL template)

## Safety
NEVER modify existing files inside `prisma/migrations/`!
```

### After (Progressive Disclosure — High Signal)
1. **Deleted**: Persona fluff, SOLID/clean code clichés, standard `src/components` tree dump.
2. **Moved to Biome/ESLint**: 2-space indent, single quotes, semicolons, import sorting.
3. **Moved to Skill (`.agents/skills/db-migration/SKILL.md`)**: 60-line Prisma migration step-by-step runbook.
4. **Moved to Hook (`PreToolUse` in `.claude/settings.json` or `.agents/hooks.json`)**: Hard deny on file edits/writes targeting `prisma/migrations/**`.
5. **Kept in Root `AGENTS.md` (18 lines)**:
   ```markdown
   # Repository Instructions

   ## Commands
   - Install / Build: `pnpm install` / `pnpm build`
   - Typecheck & Lint: `pnpm typecheck && pnpm biome check .`
   - Single test: `pnpm vitest run <path/to/file.test.ts>`

   ## Architecture & Constraints
   - Next.js 15 App Router + Prisma (`pnpm` only; never `npm` or `npx`).
   - Server mutations belong in `src/features/*/actions.ts` and must validate inputs with Zod via `safeActionClient` (`src/lib/safe-action.ts`).
   - Existing files in `prisma/migrations/` are immutable; use `/db-migration` skill for schema changes.
   ```
