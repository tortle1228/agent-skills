# Project Bootstrap

[English](README.md) | [한국어](README.ko.md)

An agent skill that starts new software projects and audits existing repositories against a 10-pillar engineering checklist, scaled to the project instead of maximal ceremony.

## What it does

The skill picks one of three modes from your request:

| Mode | Example request | Result |
| --- | --- | --- |
| New project | "Start a small Python CLI that counts words in Markdown files." | A scaffold from the ecosystem's official generator, with pinned runtime, lockfile, formatter, linter, type checks, one passing test, `.gitignore`, `AGENTS.md`, and the checks actually run |
| Existing repository | "What is this repo's engineering setup missing? Report only." | Gaps grouped as P0/P1/P2 with a phased rollout; nothing is changed unless you ask |
| Advice only | "FastAPI, Django REST Framework, or Litestar for our team?" | A weighted comparison, one recommendation, when not to choose it, and an optional ADR |

New projects use one of three presets: **Lean MVP** for prototypes and personal tools, **Standard Production** (the default) for real services, and **Strict Enterprise** for multi-team or regulated systems. The [checklist](references/10-pillars-checklist.md) shows what each preset includes.

Invoke it as `$project-bootstrap` in Codex or `/project-bootstrap` in Claude Code, or just describe the task; the skill description lets supported hosts pick it automatically.

## What runs and what changes

- [`scripts/audit-project.sh`](scripts/audit-project.sh) is read-only. It lists installed runtimes and which config files exist per pillar, including settings kept inside `pyproject.toml` or `package.json` and tools built into Rust and Go. It needs `bash`.
- In new-project mode the agent runs official generators (`uv init`, `pnpm create …`, `cargo init`, and so on), installs project-local dependencies, and runs the verification commands. If the requested runtime is missing, it tries a temporary toolchain in a git-ignored folder and removes it afterwards. It does not install anything system-wide or with `sudo` without your consent.
- Git hooks and agent instruction files are delegated to the sibling `git-hooks` and `project-instructions` skills when they are installed. Without them, the skill writes a minimal pre-commit hook and a short `AGENTS.md` itself.
- Tool recommendations age quickly. The skill checks current versions in official docs (Context7 or web search when the host provides them) rather than relying on the reference files alone.

## Install

Requires Node.js 22.14 or later. Install only this skill, for both hosts:

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill project-bootstrap
```

Add `--skill git-hooks --skill project-instructions` to install the delegated skills too. Alternatively, install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill project-bootstrap -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/project-bootstrap` (Codex) and `~/.claude/skills/project-bootstrap` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill project-bootstrap
```

## License

[MIT](LICENSE).
