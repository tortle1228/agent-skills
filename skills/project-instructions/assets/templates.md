# Ready-to-Use Project Instruction Templates

Adapt these minimal templates during **Bootstrap (`init`)** and **Multi-Agent Sync (`sync`)**. Strip any section that does not contain non-inferable, repo-specific signal.

---

## 1. Root `AGENTS.md` — Standard Repository (Target: 40–100 lines)

```markdown
# Project Instructions

## Commands
- Install: `<exact install command, e.g., pnpm install>`
- Build / Typecheck: `<e.g., pnpm build && pnpm typecheck>`
- Lint / Format Check: `<e.g., pnpm biome check .>`
- Single Test (Preferred): `<e.g., pnpm vitest run path/to/file.test.ts>`
- Full Test Suite: `<e.g., pnpm test>`

## Stack & Architectural Boundaries
- Runtime & Framework: `<e.g., Node 22, Next.js 15 App Router, TypeScript strict>`
- `<Boundary rule 1: where domain logic lives vs UI/transport layers>`
- `<Boundary rule 2: forbidden cross-layer imports or deprecated patterns>`

## Project-Specific Conventions & Gotchas
- `<Wrapper rule: e.g., Use src/lib/http.ts instead of raw fetch>`
- `<State/DB rule: e.g., Never edit generated files in src/gen/ or migrations/>`
- `<Env/Config rule: e.g., Access env vars exclusively via src/config/env.ts>`

## Reference Pointers
- Architecture decisions: `docs/adr/`
- `<Domain workflow pointer: e.g., See docs/auth-flow.md before modifying session middleware>`
```

---

## 2. Monorepo Root & Subpackage `AGENTS.md`

### Root `AGENTS.md` (Workspace Topology Only)
```markdown
# Monorepo Instructions

## Workspace Commands
- Package Manager: `pnpm` workspaces + Turborepo (never run `npm` or `yarn`).
- Scoped Test: `pnpm --filter <pkg-name> test -- <file>`
- Scoped Typecheck & Lint: `pnpm --filter <pkg-name> typecheck && pnpm lint`

## Package Boundaries
- `apps/web`: Customer-facing web app (see `apps/web/AGENTS.md`)
- `services/api`: Core backend API (see `services/api/AGENTS.md`)
- `packages/shared`: Pure types & validation schemas — zero runtime DB/HTTP dependencies allowed.

## Cross-Cutting Rules
- Shared contract changes in `packages/shared` require running `pnpm --filter shared build` before downstream typechecks.
```

### Subpackage `services/api/AGENTS.md`
```markdown
# API Service Instructions (`services/api`)

## Local Commands
- Single Unit Test: `pnpm vitest run src/<module>/<file>.test.ts`
- Integration Test (requires local Postgres): `pnpm test:int <file>`

## Service Constraints
- Controllers (`src/routes/`) handle HTTP parsing only; business rules belong in `src/services/`.
- All external queries must pass a `alsContext` transaction handle (`src/db/tx.ts`).
```

---

## 3. Multi-Agent Thin Bridges

### `CLAUDE.md` (Bridge to `AGENTS.md`)
```markdown
@AGENTS.md
```

### `.gitignore` Hygiene Snippet (Local Overrides)
```gitignore
# Local AI agent overrides (personal preferences, never commit)
CLAUDE.local.md
*.local.md
```

---

## 4. Path-Scoped Rule Headers Across Ecosystems

Use scoped rules so specialized instructions consume **0 tokens** on unrelated tasks.

### Claude Code — `.claude/rules/frontend-ui.md`
```markdown
---
paths:
  - "src/ui/**/*.tsx"
  - "src/components/**/*.tsx"
---

# UI Component Rules
- Use semantic design tokens from `src/ui/tokens.css`; never hardcode hex colors.
- Interactive elements require accessible labels and keyboard focus states.
```

### Google Antigravity — `.agents/rules/frontend-ui.md`
```markdown
---
trigger: glob
globs: "src/ui/**/*.tsx, src/components/**/*.tsx"
description: "Design system token and accessibility constraints for React UI components"
---

# UI Component Rules
- Use semantic design tokens from `src/ui/tokens.css`; never hardcode hex colors.
- Interactive elements require accessible labels and keyboard focus states.
```

### Google Antigravity (Semantic On-Demand) — `.agents/rules/payments.md`
```markdown
---
trigger: model_decision
description: "Apply whenever modifying Stripe billing, subscriptions, webhooks, or invoice logic."
---

# Billing & Webhook Rules
- Every webhook handler in `src/billing/webhooks/` must enforce idempotency using `event.id` in `webhook_events`.
- Monetary amounts must be stored and calculated in integer minor units (cents/KRW), never floats.
```

### Cursor — `.cursor/rules/frontend-ui.mdc`
```markdown
---
description: "Design system token and accessibility constraints for React UI components"
globs: ["src/ui/**/*.tsx", "src/components/**/*.tsx"]
alwaysApply: false
---

# UI Component Rules
- Use semantic design tokens from `src/ui/tokens.css`; never hardcode hex colors.
- Interactive elements require accessible labels and keyboard focus states.
```

### GitHub Copilot — `.github/instructions/frontend-ui.instructions.md`
```markdown
---
applyTo: "src/ui/**/*.tsx,src/components/**/*.tsx"
description: "Design system token and accessibility constraints for React UI components"
---

# UI Component Rules
- Use semantic design tokens from `src/ui/tokens.css`; never hardcode hex colors.
- Interactive elements require accessible labels and keyboard focus states.
```
