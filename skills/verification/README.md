# Verification

[English](README.md) | [한국어](README.ko.md)

An agent skill that asks for evidence before the agent says work is done. Before it claims work is finished, fixed, or passing, the agent runs the check that would fail if the claim were wrong, reads the result, and reports with that evidence.

## What it does

It applies when the agent is about to say "done", "fixed", "works now", or "all green"; before a commit, PR, or handoff; and when it receives a subagent's success report.

- **Gate:** state the claim, choose a proof that could fail, run it fresh after the last edit, read the full output, then report.
- **Evidence table:** each kind of claim (tests pass, bug fixed, feature works, delegated work done) lists what counts and what does not, such as a lint pass standing in for a build.
- **Real surface:** CLI, service, UI, and library changes are proven by running them the way a user reaches them. Docs-only, types-only, and tests-only changes are `SKIP`.
- **Verdicts:** `PASS`, `FAIL`, `BLOCKED`, or `SKIP` per claim, plus a list of what was not checked. A check that could not run is never reported as a pass.

If the project has a `verify-*` skill or another recipe for launching its app, the agent uses it. When it has none, the agent may suggest `create-verification` once and works without it.

Invoke it as `$verification` in Codex or `/verification` in Claude Code, or just ask for a change and let it trigger before the agent reports back.

## What runs and what changes

- The skill only adds a check before the agent reports. The agent runs the project's own test, build, or launch commands to get evidence.
- It does not edit files or install anything by itself. Verification may start local servers or apps, and the agent is expected to stop what it started.

## Install

Requires Node.js 22.14 or later.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill verification
```

Or install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill verification -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/verification` (Codex) and `~/.claude/skills/verification` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill verification
```

## License

[MIT](LICENSE).
