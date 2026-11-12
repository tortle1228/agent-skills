# Agent Code Review

[English](README.md) | [한국어](README.ko.md)

An agent skill that reviews a code change like the senior developer who gets paged when it breaks, then reports in plain language with a clear ship-or-fix verdict.

## What it does

| Mode | Example request | Result |
| --- | --- | --- |
| Report only | "Review my uncommitted changes." / "Review the last commit." | Findings grouped as must fix, should fix, and nice to have, each with a concrete failure case and the smallest fix. No code is changed |
| Fix loop | "Review this and fix what's needed." / before the agent calls its own multi-file work done | An isolated reviewer, verified findings, fixes, and re-checks for at most three rounds, then the same report plus what was fixed or rejected |

When unsure, it uses report-only mode, because changing code you did not ask to change is harder to undo than an extra question.

How it keeps reviews useful:

- It runs the project's own build, type check, lint, and tests first, so review attention goes to what machines cannot catch.
- The review runs in a fresh context (a subagent when the host has one) given your original request, not the writer's summary. Without subagents, the report says so.
- A finding needs a concrete case: "this input leads to this wrong result". Vague worries and style taste are dropped, and wrong findings are rejected with a reason.
- The loop is capped at three rounds. Ambiguous requirements and architecture trade-offs go back to you.
- The report is written entirely in your language, labels included, in short sentences for a reader who has not seen the code. See the [report format](references/report-format.md).

Invoke it as `$agent-code-review` in Codex or `/agent-code-review` in Claude Code, or ask for a review in your own words.

## What runs and what changes

The skill has no bundled scripts. The agent runs your project's existing commands (from package scripts, Makefile, CI config, or README). In report-only mode it changes no files. In fix-loop mode it edits the files needed for accepted fixes and reruns the tests after each round; it does not commit unless you ask.

## Install

Requires Node.js 22.14 or later.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill agent-code-review
```

Or install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill agent-code-review -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/agent-code-review` (Codex) and `~/.claude/skills/agent-code-review` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill agent-code-review
```

## License

[MIT](LICENSE). The review order, finding checks, and report format are adapted from the ponytail-review skill of Ponytail under the MIT License; see [NOTICE](NOTICE).
