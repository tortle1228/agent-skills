# Project Instructions

[English](README.md) | [한국어](README.ko.md)

An agent skill that creates, audits, slims down, and synchronizes the instruction files coding agents read: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and rule folders for Claude Code, Antigravity, Cursor, Copilot, and Windsurf.

## What it does

| Mode | Example request | Result |
| --- | --- | --- |
| Bootstrap | "Write an AGENTS.md for this repo and make Claude Code read it too." | A short `AGENTS.md` built from verified commands and project-specific rules, plus a `CLAUDE.md` that imports it with `@AGENTS.md` |
| Audit and diet | "Our agent instructions are long and contradict each other. Clean them up." | Stale commands and paths fixed, filler and formatting rules removed, real rules kept, with a before/after summary |
| Sync | "Make CLAUDE.md, .cursorrules, and Copilot instructions agree." | `AGENTS.md` as the single source with thin bridges for each tool |
| Evolve | "The agent keeps making this mistake; add a rule." | The cheapest reliable fix: a lint rule, a hook, a scoped rule, or one or two lines in `AGENTS.md` |

The skill follows a few principles from the [content rubric](references/content-rubric.md): keep a line only if deleting it would cause a mistake the agent cannot avoid by reading the code, leave formatting to linters, and keep one source of truth.

It writes instruction files in the language the repository already uses (English when there is no signal), not automatically in your chat language. It changes only the files your request is about, and suggests hooks or files for other tools in its report instead of creating them, unless you ask.

Invoke it as `$project-instructions` in Codex or `/project-instructions` in Claude Code, or just describe the task.

## What runs and what changes

- [`scripts/audit_instructions.py`](scripts/audit_instructions.py) is a read-only static auditor (Python 3 standard library only). It finds dead package scripts and Make targets, broken paths and imports, lockfile mismatches, missing frontmatter, unbridged duplicates, oversized files, hardcoded local paths, and likely secrets. Run it directly with `python3 scripts/audit_instructions.py <repo> [--json] [--strict]`.
- The agent edits instruction files in your repository. Before deleting legacy files or cutting major sections, it shows the plan and asks, because removed rules may hold knowledge only the team has.

## Install

Requires Node.js 22.14 or later for the installer and Python 3 for the auditor.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill project-instructions
```

Or install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill project-instructions -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/project-instructions` (Codex) and `~/.claude/skills/project-instructions` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill project-instructions
```

## License

[MIT](LICENSE).
