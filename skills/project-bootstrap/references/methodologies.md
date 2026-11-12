# Engineering Decision & Design Methodologies

Reference guide for choosing technologies, structuring architectures, and setting testing/collaboration standards.

---

## 1. Tech Stack Selection Methodologies

### 1.1 Choose Boring Technology (Innovation Token Budget)
Coined by Dan McKinley: every project starts with roughly **1 to 3 Innovation Tokens**.
- Spend tokens **only** where novel technology directly creates your product's core competitive advantage.
- Everywhere else (primary relational DB, background queues, container runtime, CI), default to battle-tested, well-documented "boring" standards (e.g., PostgreSQL, Redis, standard Linux containers) whose failure modes are widely understood.

### 1.2 Thoughtworks Technology Radar Ring Filter
Classify every candidate tool into one of four maturity rings before adopting:
- **Adopt**: Proven industry defaults with mature ecosystems and low operational risk. Safe for `Standard Production` and `Strict Enterprise`.
- **Trial**: Production-capable with clear advantages (e.g., `uv`, `Biome`, `Ruff`, `Mise`), suitable when the team understands the trade-offs.
- **Assess**: Promising early-stage tools. Restrict to side projects, non-critical internal tools, or isolated experiments.
- **Hold**: Legacy, unmaintained, security-compromised, or over-complicated tools. Avoid in greenfield projects.

### 1.3 Weighted Decision Matrix
When comparing 2–4 candidate frameworks or libraries, score each (1–5) across weighted dimensions:

| Criterion | Typical Weight | Key Questions |
| :--- | :---: | :--- |
| **Ecosystem & Maintenance Health** | 25% | Active releases in last 6 months? Multiple maintainers? High adoption on `deps.dev` / `ecosyste.ms`? |
| **Developer Velocity & Team Fit** | 25% | Team familiarity? Quality of official docs, TypeScript/type support, and AI agent training coverage? |
| **Operational Simplicity** | 20% | Easy to deploy, debug, monitor, and upgrade without dedicated infra specialists? |
| **Non-Functional Fit (Perf / Security)** | 20% | Meets p99 latency, throughput, bundle size, and compliance/supply-chain requirements? |
| **License & Lock-in Risk** | 10% | Permissive OSS license (MIT/Apache-2.0)? Clean exit path / standard protocols? |

> **Time-boxed Spike Rule**: If two candidates remain tied on a high-risk assumption, run a strictly time-boxed PoC (4–16 hours) testing the hardest integration point before committing.

### 1.4 Architecture Decision Records (ADRs)
Every major Day-1 choice (language, web framework, database, monorepo tool, auth provider) should produce a concise markdown file under `docs/adr/NNNN-title.md`:
- Prevents circular re-litigation 6 months later.
- Gives humans and AI agents explicit context on *why* constraints exist.

---

## 2. Application & Repository Architecture Methodologies

### 2.1 Modular Monolith First
- **Default for 90% of new backends**: Deploy as a single unit (one binary/container) while enforcing strict internal module boundaries (`modules/billing`, `modules/auth`, `modules/catalog`).
- Modules communicate only via exported public interfaces/facades—never by reaching into another module's internal DB tables or private repositories.
- Extract to microservices **only** when independent scaling, independent organizational ownership, or hard runtime isolation requires it.

### 2.2 Choosing an Internal Code Layout
Match folder architecture to domain complexity:

| Pattern | Best For | Structure Concept |
| :--- | :--- | :--- |
| **Flat / Idiomatic Standard** | CLIs, small APIs, microservices, libraries | Minimal packages (`cmd/`, `internal/` in Go; `src/<pkg>/` in Python/Rust) |
| **Vertical Slice Architecture** | Product CRUD/SaaS backends with high feature velocity | Group handler + validation + query + test together per feature (`features/create-order/`) |
| **Feature-Sliced Design (FSD)** | Medium-to-large frontend SPAs / web apps | Strict unidirectional layers: `app` → `pages` → `widgets` → `features` → `entities` → `shared` |
| **Hexagonal / Clean Architecture** | Complex domain rules, financial/core business engines, swappable adapters | Pure `domain` & `application` core with zero framework imports; `adapters`/`infra` depend inward |

### 2.3 Modern Twelve-Factor App Essentials
1. **Strict Config Separation**: Config lives in environment variables validated via typed schemas on startup—never committed secrets or per-env code branches.
2. **Stateless Processes**: Store session/upload state in attached backing services (DB, Redis, S3), never local container disk.
3. **Dev/Prod Parity**: Use `compose.yaml` / `Testcontainers` locally with the exact same DB engine and major version as production (avoid "SQLite in dev/test, Postgres in prod" subtle bugs).
4. **Disposability**: Fast startup + `SIGTERM` graceful shutdown + `/healthz` & `/readyz` endpoints.

---

## 3. Testing & Delivery Methodologies

### 3.1 Testing Trophy vs Testing Pyramid
- **Testing Trophy (Default for Web/API Services)**:
  1. **Static Analysis** (Types + Linter) catches typos and contract mismatches at zero runtime cost.
  2. **Integration Tests** (largest share) test real API routes/components against real containerized DBs (`Testcontainers`) or network-level mocks (`MSW`), maximizing confidence per line of test code.
  3. **Unit Tests** focus on pure domain logic, edge-case calculations, and state machines.
  4. **E2E Tests** (thin top layer) cover 3–5 revenue/auth critical user journeys.
- **Testing Pyramid (Default for Compilers, SDKs, Core Algorithms)**:
  - Heavy fast unit + property-based tests (`Hypothesis`, `fast-check`, `proptest`), moderate integration tests, minimal E2E.

### 3.2 Trunk-Based Development & Automated Releases
- Keep `main` always deployable; merge small, short-lived PRs (< 1–2 days) gated by automated CI.
- Enforce **Conventional Commits** (`feat:`, `fix:`, `perf:`, `chore:`, `feat!:`) when pairing with `Release-Please` or `Changesets` so version bumps and `CHANGELOG.md` require zero manual editing.
