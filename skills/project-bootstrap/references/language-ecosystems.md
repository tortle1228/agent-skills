# Language Ecosystems: Modern Toolchains & Reference Directories

Consult the relevant language section below when scaffolding a project or evaluating packages. Tool names are starting points, not mandates: confirm current versions and setup steps in official docs before using them, because this file ages.

---

## Cross-Language Discovery & Health Verification Sites
Use these vendor-neutral references to check maturity, security, and dependency health across any language:
- **Package Security & Transitive Dependency Health**: `https://deps.dev/` (Google Open Source Insights — OpenSSF Scorecard, licenses, advisories)
- **Cross-Registry Maintainer & Download Metrics**: `https://ecosyste.ms/`
- **Technology Maturity Rings**: `https://www.thoughtworks.com/radar`
- **Role & Stack Ecosystem Maps**: `https://roadmap.sh/`
- **Curated Awesome Lists Index**: `https://github.com/sindresorhus/awesome`
- **Boilerplate Utilities**: `https://www.toptal.com/developers/gitignore` (gitignore.io), `https://choosealicense.com/`, `https://adr.github.io/`

---

## 1. TypeScript / JavaScript (Node.js, Bun, Frontend, Full-Stack)

### Recommended Modern Toolchain
- **Package Manager & Monorepo**: `pnpm` (preferred for disk efficiency & strict node_modules isolation) or `bun`; `Turborepo` or `Nx` for monorepos.
- **Official Scaffolds**: `pnpm create vite`, `pnpm create next-app`, `pnpm create t3-app`, `pnpm create astro`, `pnpm create hono`.
- **Formatter & Linter**:
  - *Fast All-in-One*: `Biome` (`biome.json` — formatting + linting in milliseconds).
  - *Ecosystem Plugin Richness*: `ESLint v9+ (eslint.config.mjs Flat Config)` + `Prettier` (optionally paired with `Oxlint` for speed).
- **Type Safety & Env**: `tsconfig.json` with `"strict": true`, `"noUncheckedIndexedAccess": true`; runtime validation via `Zod` + `@t3-oss/env-core`.
- **Architectural Boundary Lint**: `dependency-cruiser` (`.dependency-cruiser.cjs`) or `eslint-plugin-boundaries`.
- **Testing**: `Vitest` (unit/integration) + `@testing-library/*` + `MSW` (API mocking) + `Playwright` (E2E) + `testcontainers` (backend DB tests).
- **Release**: `Changesets` (monorepos/npm packages) or `Release-Please`.

### Authoritative Reference Sites
- **Curated Package Comparison**: `https://bestofjs.org/` (stars velocity, category leaders, maintenance health)
- **Supply-Chain Security Audit**: `https://socket.dev/` (detects install scripts, typosquatting, maintainer risk)
- **Bundle Cost & Download Trends**: `https://bundlephobia.com/`, `https://pkg-size.dev/`, `https://npmtrends.com/`
- **Ecosystem Surveys**: `https://stateofjs.com/`, `https://stateofreact.com/`
- **Style & Architecture Guides**:
  - Google TS Style Guide: `https://google.github.io/styleguide/tsguide.html`
  - Feature-Sliced Design (Frontend): `https://feature-sliced.design/`
  - Node.js Best Practices: `https://github.com/goldbergyoni/nodebestpractices`

---

## 2. Python (Backend APIs, AI/ML, Data, CLI)

### Recommended Modern Toolchain
- **Unified Package, Env & Python Manager**: `uv` (`uv init --package`, `uv add`, `uv lock`, `uv run` — replaces `pip`, `poetry`, `virtualenv`, `pyenv`).
- **Standard Layout**: `pyproject.toml` (PEP 621) + `src/<package_name>/` layout (prevents accidental implicit local imports during tests).
- **Formatter & Linter**: `Ruff` (`ruff check` + `ruff format` in `pyproject.toml`, enabling rule sets like `E`, `F`, `I`, `B`, `UP`, `SIM`, `S` for security).
- **Type Checker**: `Pyright` (`strict` mode) or `mypy` (`strict = true`).
- **Config Validation**: `pydantic-settings` (`BaseSettings` loading `.env` on startup).
- **Architectural Boundary Lint**: `import-linter` (`[tool.importlinter]` contracts in `pyproject.toml`).
- **Testing**: `pytest` + `pytest-cov` + `pytest-asyncio` + `Hypothesis` (property-based) + `testcontainers-python`.
- **Security**: `pip-audit` or `Bandit` / `Semgrep`.

### Authoritative Reference Sites
- **Modern Tooling Docs**: `https://docs.astral.sh/` (`uv` & `Ruff` official guides)
- **Curated Package Catalog**: `https://github.com/vinta/awesome-python`
- **Registry & Download Trends**: `https://pypi.org/`, `https://pypistats.org/`
- **Packaging Standards**: `https://packaging.python.org/`
- **Style & Architecture Guides**:
  - PEP 8: `https://peps.python.org/pep-0008/`
  - Google Python Style Guide: `https://google.github.io/styleguide/pyguide.html`
  - FastAPI Production Structure: `https://github.com/zhanymkanov/fastapi-best-practices`

---

## 3. Go (Cloud-Native Services, CLIs, Infrastructure)

### Recommended Modern Toolchain
- **Module & Layout**: `go mod init` following official layout:
  - Simple lib/CLI: root `*.go`
  - Multi-binary / service: `cmd/<app>/main.go` + `internal/<domain>/` (compiler-enforced private packages!) + `api/` (OpenAPI/proto).
- **Formatter & Linter**: `gofumpt` + `golangci-lint` (`.golangci.yml` enabling `errcheck`, `govet`, `staticcheck`, `revive`, `gocritic`, `gosec`).
- **Architectural Boundary Lint**: Go's built-in `internal/` visibility + `go-arch-lint` or `depguard` rule inside `golangci-lint`.
- **Testing**: `go test -race -shuffle=on ./...` + `testify/require` + `testcontainers-go`.
- **Security & Release**: `govulncheck ./...` (official Go vulnerability scanner) + `GoReleaser` (`.goreleaser.yaml`).
- **Structured Logging**: Standard library `log/slog` (Go 1.21+) or `uber-go/zap`.

### Authoritative Reference Sites
- **Official Package Discovery & "Imported By" Trust Metric**: `https://pkg.go.dev/`
- **Curated Catalog**: `https://github.com/avelino/awesome-go`
- **Official Module Layout Guide**: `https://go.dev/doc/modules/layout`
- **Style & Idiom Guides**:
  - Effective Go: `https://go.dev/doc/effective_go`
  - Go Code Review Comments: `https://go.dev/wiki/CodeReviewComments`
  - Uber Go Style Guide: `https://github.com/uber-go/guide/blob/master/style.md`
  - Google Go Style Guide: `https://google.github.io/styleguide/go/`

---

## 4. Rust (Systems, High-Performance Backends, CLI, WebAssembly)

### Recommended Modern Toolchain
- **Workspace & Toolchain Pinning**: `cargo init` / Cargo Workspaces (`[workspace.lints]` shared across crates) + `rust-toolchain.toml`.
- **Formatter & Linter**: `cargo fmt --check` + `cargo clippy --all-targets --all-features -- -D warnings` (configure `clippy::pedantic` selectively).
- **Supply Chain, License & Advisory Gate**: `cargo-deny` (`deny.toml` — checks advisories, duplicate crates, and OSS licenses in one step) + `cargo-audit`.
- **Testing & Benchmarking**: `cargo-nextest` (fast parallel test runner) + `proptest` + `insta` (snapshot tests) + `criterion` (benchmarks).
- **Observability & Error Idioms**: `tracing` (structured spans/events), `thiserror` (library typed errors), `anyhow` / `eyre` (application errors).

### Authoritative Reference Sites
- **De-Facto Standard Crate Recommendations**: `https://blessed.rs/` (essential Day-1 stack picker for async, HTTP, DB, CLI, serialization)
- **Fast Categorized Crate Explorer**: `https://lib.rs/` (cleaner categorization, dependency weight, and maintenance signals than raw `crates.io`)
- **Official Registry & Docs**: `https://crates.io/`, `https://docs.rs/`
- **Style & Design Guides**:
  - Rust API Guidelines: `https://rust-lang.github.io/api-guidelines/`
  - Effective Rust: `https://www.lurklurk.org/effective-rust/`
  - The Rust Performance Book: `https://nnethercote.github.io/perf-book/`

---

## 5. Java & Kotlin (Enterprise Backend, Android, KMP)

### Recommended Modern Toolchain
- **Build & Version Catalog**: `Gradle (Kotlin DSL: build.gradle.kts)` + `gradle/libs.versions.toml` (centralized dependency versions) + Gradle Wrapper (`./gradlew`).
- **Official Scaffolds**: `https://start.spring.io/` (Spring Boot), `https://start.ktor.io/` (Ktor), `https://kmp.jetbrains.com/` (Kotlin Multiplatform).
- **Formatting & Static Analysis**:
  - *Java*: `Spotless` (`google-java-format` or `palantir-java-format`) + `ErrorProne` + `NullAway` (compile-time null safety) + `SonarLint`.
  - *Kotlin*: `ktlint` (or `Spotless`) + `Detekt` (`detekt.yml`).
- **Architectural Boundary Lint**: `ArchUnit` (enforce package/hexagonal/DDD dependency rules directly inside JUnit tests) or `Konsist` (Kotlin-native structural linter).
- **Testing**: `JUnit 5` + `AssertJ` / `Kotest` + `MockK` (Kotlin) / `Mockito` (Java) + `Testcontainers`.

### Authoritative Reference Sites
- **Registries**: `https://central.sonatype.com/`, `https://plugins.gradle.org/`
- **Curated Catalogs**: `https://github.com/akullpp/awesome-java`, `https://github.com/KotlinBy/awesome-kotlin`
- **Style & Guides**:
  - Google Java Style Guide: `https://google.github.io/styleguide/javaguide.html`
  - Official Kotlin Coding Conventions: `https://kotlinlang.org/docs/coding-conventions.html`
  - Practical JVM Tutorials: `https://www.baeldung.com/`

---

## 6. C# (.NET), Swift & Dart (Flutter) Quick Reference

| Ecosystem | Modern Toolchain Defaults | Key Discovery & Style Reference Sites |
| :--- | :--- | :--- |
| **C# / .NET** | `dotnet new` + `Directory.Build.props` (`TreatWarningsAsErrors`, `Nullable=enable`) + `Directory.Packages.props` (Central Package Mgmt) + `dotnet format` + Roslyn Analyzers + `xUnit` + `Testcontainers` | `https://www.nuget.org/`, `https://dotnet.microsoft.com/en-us/learn/dotnet/architecture-guides`, `https://github.com/quozd/awesome-dotnet` |
| **Swift** | `swift package init` (`Package.swift`) + `swift-format` + `SwiftLint` + `Swift Testing` (`@Test`) | `https://swiftpackageindex.com/` (platform & Swift version matrix), `https://www.swift.org/documentation/api-design-guidelines/` |
| **Dart / Flutter** | `flutter create` + `very_good_analysis` (`analysis_options.yaml`) + `flutter test` + `patrol` / `integration_test` | `https://pub.dev/` (check Pub Points & Verified Publisher), `https://docs.flutter.dev/app-architecture` |
