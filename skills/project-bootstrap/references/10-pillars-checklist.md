# 10-Pillar Project Initialization Checklist & Presets

Use this checklist to decide which engineering guardrails to include based on project maturity:
- **MVP (`Lean MVP`)**: Fast validation, solo/small team, minimal ceremony.
- **Prod (`Standard Production`)**: Default for real services/products. Prevents early tech debt and security leaks.
- **Ent (`Strict Enterprise`)**: Multi-team, regulated, or long-lived high-scale systems.

Legend: `✅ Required` | `⚡ Recommended` | `➖ Optional / Skip`

---

## Pillar 1: Tech Stack & Package Management
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Language & runtime version pinned | ✅ | ✅ | ✅ | Current LTS/stable release, verified at setup time (e.g., Node LTS, Rust stable) |
| Modern package manager + committed lockfile | ✅ | ✅ | ✅ | `pnpm-lock.yaml`, `uv.lock`, `go.sum`, `Cargo.lock` |
| API contract / protocol choice | ⚡ | ✅ | ✅ | REST + OpenAPI, GraphQL, gRPC/Protobuf (`buf`), or tRPC |

## Pillar 2: Repository Strategy & Architecture Skeleton
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Repo topology (Single vs Monorepo workspace) | ✅ | ✅ | ✅ | Start single-repo or modular workspace (`pnpm`/`uv`/`Cargo`) |
| Explicit folder & module boundary layout | ⚡ | ✅ | ✅ | Domain/Feature-based, Clean/Hexagonal, or FSD (frontend) |
| Reusable template tracking (`Copier`) | ➖ | ➖ | ⚡ | `.copier-answers.yml` to sync org-wide boilerplate updates |

## Pillar 3: Dev Environment & Reproducibility
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Unified runtime/task manager (`mise.toml` / `Makefile` / `just`) | ⚡ | ✅ | ✅ | Standardized `dev`, `lint`, `test`, `build` commands |
| `.editorconfig` + IDE workspace recommendations | ✅ | ✅ | ✅ | Consistent indentation, LF line endings, UTF-8 |
| `.env.example` + **Fail-fast startup schema validation** | ✅ | ✅ | ✅ | Validate env vars on boot (`Zod`/`t3-env`, `Pydantic Settings`) |
| Local backing services (`compose.yaml`) | ⚡ | ✅ | ✅ | One-command local Postgres/Redis/MinIO startup |
| DevContainer (`.devcontainer/devcontainer.json`) | ➖ | ⚡ | ✅ | Instant reproducible container workspace |

## Pillar 4: Code Quality, Formatting & Static Analysis
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Auto-formatter | ✅ | ✅ | ✅ | Zero style debates (`Biome`/`Prettier`, `Ruff`, `gofumpt`, `rustfmt`) |
| Static linter | ✅ | ✅ | ✅ | Bug/anti-pattern rules (`ESLint`/`Biome`, `Ruff`, `golangci-lint`, `Clippy`) |
| Strict type checking | ✅ | ✅ | ✅ | `tsconfig` `"strict": true`, `pyright`/`mypy --strict`, compiler flags |
| **Architectural dependency linter** | ➖ | ⚡ | ✅ | Block illegal cross-layer imports (`dependency-cruiser`, `import-linter`, `ArchUnit`) |
| Spell / Markdown / Dockerfile lint | ➖ | ⚡ | ✅ | `cspell`, `markdownlint`, `hadolint` |

## Pillar 5: Testing Strategy & Quality Gates
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Fast unit test runner + initial smoke test | ✅ | ✅ | ✅ | Verify test runner works on Day 1 |
| Integration tests with real dependencies | ➖ | ✅ | ✅ | Use `Testcontainers` or ephemeral local DBs instead of heavy DB mocks |
| Critical-path E2E tests | ➖ | ⚡ | ✅ | `Playwright` (web/API) or `Maestro` (mobile) for auth/core flows |
| Contract / Property-based / Load tests | ➖ | ➖ | ⚡ | `Pact` (API contracts), `fast-check`/`Hypothesis`, `k6` |
| Deterministic test data factories | ➖ | ⚡ | ✅ | Avoid brittle shared SQL dumps; isolate per-test transactions |

## Pillar 6: Git Workflow & Collaboration Hooks
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Tailored `.gitignore` | ✅ | ✅ | ✅ | OS, IDE, build artifacts, `.env*` (except `.env.example`) |
| Pre-commit / Pre-push hooks | ⚡ | ✅ | ✅ | Staged-only format/lint + secret check in a few seconds; set up via the `git-hooks` skill when available |
| Conventional Commits enforcement | ➖ | ⚡ | ✅ | Required if automating changelogs with `Release-Please` |
| PR template, Issue templates & `CODEOWNERS` | ➖ | ⚡ | ✅ | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS` |

## Pillar 7: Shift-Left Security & Supply Chain
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Secret leak scanner (`Gitleaks` / `TruffleHog`) | ⚡ | ✅ | ✅ | Run in pre-commit hook and CI |
| Dependency vulnerability scan (SCA) | ➖ | ✅ | ✅ | `pnpm audit`, `pip-audit`/`uv`, `govulncheck`, `cargo-deny`, `Trivy` |
| Automated dependency PRs (`Renovate`) | ➖ | ✅ | ✅ | Group minor/patch updates to avoid PR noise |
| SAST & License compliance / SBOM | ➖ | ➖ | ✅ | `Semgrep`/`CodeQL`, `cargo-deny`/`license-checker`, Cosign/SBOM |

## Pillar 8: CI/CD Pipeline & Release Automation
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Fast PR CI pipeline (Lint + Typecheck + Test + Build) | ⚡ | ✅ | ✅ | Cached dependencies, < 5–10 min feedback, pinned Action versions |
| Automated SemVer & Changelog (`Release-Please` / `Changesets`) | ➖ | ⚡ | ✅ | Zero-touch release PRs & Git tags from Conventional Commits |
| Production containerization (`Dockerfile` + `.dockerignore`) | ➖ | ✅ | ✅ | Multi-stage build, non-root user, minimal base image |
| Infrastructure as Code (IaC) & Preview Environments | ➖ | ⚡ | ✅ | `Terraform`/`OpenTofu`/`Pulumi`, per-PR preview deploys |

## Pillar 9: Observability & Day-2 Operations
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Structured JSON logging with request/trace ID | ➖ | ✅ | ✅ | Never rely on unstructured `console.log`/`print` in production services |
| Health (`/healthz`) & Readiness (`/readyz`) + Graceful Shutdown | ➖ | ✅ | ✅ | Handle `SIGTERM` cleanly to drain active requests |
| Error tracking (`Sentry`) | ➖ | ⚡ | ✅ | Capture unhandled exceptions with source maps / release tags |
| Vendor-neutral telemetry (`OpenTelemetry`) | ➖ | ⚡ | ✅ | OTel SDK instrumentation for traces & metrics |

## Pillar 10: Documentation & AI-Native Governance
| Item | MVP | Prod | Ent | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Actionable `README.md` (5-minute quickstart) | ✅ | ✅ | ✅ | Prerequisites, setup, run, test, architecture summary |
| Root `AGENTS.md` (plus `CLAUDE.md` bridge if Claude Code is used) | ✅ | ✅ | ✅ | Verified commands and module boundaries for coding agents; use the `project-instructions` skill when available |
| Architecture Decision Records (`docs/adr/`) | ➖ | ✅ | ✅ | Record initial stack & key trade-offs (`0001-initial-stack.md`) |
| Auto-generated API docs (OpenAPI / Protobuf) | ➖ | ⚡ | ✅ | Keep API schema derived from code or code derived from schema |
