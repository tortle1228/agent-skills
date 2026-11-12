---
name: project-bootstrap
description: >-
  Start new software projects and audit existing repositories against a 10-pillar
  engineering checklist: stack and package choice, architecture skeleton,
  reproducible environment, format/lint/types, tests, Git workflow, security,
  CI/CD, observability, and docs (ADRs, AGENTS.md). Use whenever the user wants to
  scaffold or start a project, pick a language, framework, or library, set up
  linting, testing, or CI for a repo, or find what an existing repo's engineering
  setup is missing, even if they never say "bootstrap".
---

# Project Bootstrap

Set projects up so the first real feature lands on solid ground, without building ceremony the project does not need yet. Scale every recommendation to the project: a weekend CLI and a regulated multi-team service deserve different setups.

## Resources

Read only what the current step needs:

- [references/10-pillars-checklist.md](references/10-pillars-checklist.md): what each preset includes, pillar by pillar.
- [references/methodologies.md](references/methodologies.md): stack selection (boring technology, tech radar, weighted matrix), code layout, testing shape.
- [references/language-ecosystems.md](references/language-ecosystems.md): per-language toolchains and package health sites. Read only the relevant section.
- [assets/adr-template.md](assets/adr-template.md): decision record template.
- [assets/common-configs.md](assets/common-configs.md): `.editorconfig`, `mise.toml`, `renovate.json`, CI skeleton.
- [scripts/audit-project.sh](scripts/audit-project.sh): read-only scan of installed tools and per-pillar config files. Run it as `bash <this skill's directory>/scripts/audit-project.sh <target>`.

## Pick the mode

- **A. New project**: empty or near-empty directory, or "start/scaffold X".
- **B. Existing repository**: "what is missing", "add lint/tests/CI", "modernize this repo".
- **C. Advice only**: "which framework/library/language should I use".

If a request spans modes (for example, advice and then scaffolding), do them in order and confirm between them.

## A. New project

1. **Inspect first.** Run the audit script on the target. Knowing which runtimes are installed avoids proposing a stack the machine cannot run.
   - **If the requested runtime is missing**, do not stop at "unverified". Without touching the system, try a temporary toolchain so you can still verify the scaffold: the official release archive unpacked into a temporary or git-ignored folder, or a per-project manager such as `mise` or `uvx`/`npx`. Use it for the verification gate, remove it afterwards (or leave it ignored and say so), and tell the user how to install the runtime properly. Only when that is impossible (no network, no archive for the platform) write the files and report plainly which checks did not run. Never install system-wide or with `sudo` without the user's consent.
2. **Fill gaps with short questions.** Ask only what you cannot infer: what is being built (web app, API, CLI, library, data pipeline, mobile), the preset, and stack constraints (preferred language, monorepo or not, deploy target). Offer the presets as choices:
   - **Standard Production** (default, recommend first): official scaffold, strict types, lint and format, unit and integration test runner, validated env config, Git hooks with secret scan, basic CI, first ADR, AGENTS.md.
   - **Lean MVP**: official scaffold, formatter and linter, strict types, one smoke test, `.env.example`, AGENTS.md. Pick this for prototypes and throwaway tools.
   - **Strict Enterprise**: Standard plus architecture boundary lint, devcontainer, Renovate, release automation, structured logging and tracing, SAST/SBOM gates.
3. **Propose a blueprint before writing files** when there are real trade-offs: stack, layout, and which pillars the preset includes. Prefer boring, well-documented tools except where novelty is the product's edge. Check current versions and setup steps in official docs (Context7 or web search when available) because tool advice ages quickly.
4. **Scaffold.**
   - Use the ecosystem's official generator non-interactively (`pnpm create …`, `uv init`, `cargo init`, `go mod init`, `dotnet new`). Generated scaffolds track upstream conventions better than hand-written boilerplate.
   - Set clear module boundaries for the chosen layout. Add a boundary linter only for Standard/Enterprise when the stack has a practical one.
   - Add runtime pinning, `.editorconfig`, a stack-specific `.gitignore` that excludes `.env*` except `.env.example`, and startup validation of env config.
   - Add formatter, linter, type checking, a test runner with one passing test, and CI that runs the same commands.
   - **Git hooks**: if the `git-hooks` skill is available, use it. Otherwise add one minimal pre-commit hook that runs the formatter/linter on staged files and a secret scan if `gitleaks` is installed.
   - **Agent instructions**: if the `project-instructions` skill is available, use it to write AGENTS.md. Otherwise write a short root AGENTS.md with only the verified commands (install, dev, lint, typecheck, test, single test) and the module boundary rules. Leave out generic advice an agent already follows.
   - Record the stack decision in `docs/adr/0001-initial-stack.md` from the ADR template (Lean MVP may skip this).
5. **Verify before reporting done.** Install dependencies (lockfile created), then run format check, lint, typecheck/build, and the sample test, and rerun the audit script. Report each command and its result. If something cannot run here (missing runtime, no network), say so plainly instead of claiming success.

## B. Existing repository

1. Run the audit script and read the manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, build files). Pillar 9 (observability) is not file-detectable: judge it from the code (logging style, health endpoints, shutdown handling) and say that you did. Treat the script's `NONE` as "no file found", not as "missing": settings can live inside manifests, and some toolchains (Rust, Go) ship their formatter, linter, and test runner without config files.
2. Compare against the checklist for the preset that fits the project, and group gaps by impact:
   - **P0, high risk or quick win**: missing lockfile, secrets not ignored or committed, unvalidated env vars, no type check or linter, no agent instructions.
   - **P1, team safety**: no hooks, no CI, missing integration tests, no dependency updates or audit.
   - **P2, scale and operations**: boundary lint, structured logging and tracing, release automation, ADRs.
3. Propose a phased plan. For legacy code, introduce strict lint and types gradually (baselines, per-directory strictness) so the existing build does not break all at once.
4. Apply only what the user approves, then run the existing and new checks to show nothing regressed.

## C. Advice only

1. Read the methodologies and the relevant language section.
2. Compare two or three candidates in a weighted matrix (ecosystem health, team fit, operational simplicity, performance and security, license and lock-in). Check health data such as release activity and advisories on the sites listed for that language when freshness matters.
3. Recommend one option, say when you would not choose it, and offer to record the decision as an ADR.
