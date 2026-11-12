# Agent Skills

[English](README.md) | [한국어](README.ko.md)

Agent skills that cover the everyday engineering around your code: starting projects, agent instructions, Git hooks, code review, verification, and READMEs. Install all of them or only the ones you want.

## Skills

| Skill | Use it to |
| --- | --- |
| [project-bootstrap](skills/project-bootstrap/README.md) | Start a project or audit a repo's setup against a 10-pillar checklist, scaled to the project; compare stacks and record the decision |
| [project-instructions](skills/project-instructions/README.md) | Create, slim down, and sync `AGENTS.md`, `CLAUDE.md`, and other agent rule files, with a static auditor for stale commands and paths |
| [git-hooks](skills/git-hooks/README.md) | Set up fast pre-commit, commit-msg, and pre-push hooks that teammates share, verified with real commits |
| [agent-code-review](skills/agent-code-review/README.md) | Review a change with an isolated reviewer and get a plain-language ship-or-fix report, optionally with a capped fix loop |
| [readme-writer](skills/readme-writer/README.md) | Write, improve, or translate READMEs from repository evidence, with worked examples and templates |
| [verification](skills/verification/README.md) | Require fresh evidence before the agent claims work is done, fixed, or passing, with a PASS/FAIL/BLOCKED/SKIP verdict |
| [create-verification](skills/create-verification/README.md) | Generate a project-local `verify-<app>` skill that launches and drives the app, and prove it by running it once |

Each skill works on its own. project-bootstrap hands Git hooks and agent instructions to git-hooks and project-instructions when they are installed, and does a minimal version itself when they are not. verification uses a `verify-*` skill made by create-verification when the project has one, and works without it.

## Supported agents

The skills use the Agent Skills format (`SKILL.md`) and name host features only as examples, so any agent that loads Agent Skills can use them.

- **npm installer (this package):** Codex and Claude Code.
- **[Skills CLI](https://github.com/vercel-labs/skills):** Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, OpenCode, and the other agents it lists, as well as Codex and Claude Code.

The eval runs behind each skill were done in Claude Code; other agents are supported by format but not tested here.

## Install

Requires Node.js 22.14 or later. Install every skill for both hosts:

```sh
npx @tortle1228/agent-skills@latest install --agent all
```

Choose skills with `--skill` (repeat it for several) and a host with `--agent codex` or `--agent claude-code`:

```sh
npx @tortle1228/agent-skills@latest install --agent claude-code --skill project-bootstrap --skill git-hooks
npx @tortle1228/agent-skills@latest list
```

The installer copies each skill to `~/.agents/skills/<skill>` (Codex) or `~/.claude/skills/<skill>` (Claude Code) and records file hashes. It does not depend on the npm cache afterward and does not run at `npm install` time. Running it with no arguments only prints help.

For other agents, or to install from GitHub, use the Skills CLI. It can also pick single skills; replace the `-a` values with your agents:

```sh
npx skills add tortle1228/agent-skills --skill project-bootstrap -g -a codex -a claude-code
```

Use one installation method per skill and host; each manages its own updates and removal.

Then invoke a skill by name (`$project-bootstrap` in Codex, `/project-bootstrap` in Claude Code) or describe the task and let the host pick it. Reload or restart the host if a new skill does not appear.

## Update and remove

Run the install command from a newer version to update. Locally modified, unmanaged, or symlinked installations are reported as conflicts and left untouched; there is no force option. Back up your edits and move the conflicting copy before retrying.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill git-hooks
```

Without `--skill`, uninstall removes every skill this installer manages. It never deletes other files or this repository.

## Development and license

See [contributing and release instructions](CONTRIBUTING.md) and the [changelog](CHANGELOG.md). Skill behavior is checked with with-skill and without-skill eval runs kept in `evals/<skill>/`, which is not packaged.

Original code and documents are under the [MIT License](LICENSE). agent-code-review adapts material from Ponytail under the MIT License; see its [NOTICE](skills/agent-code-review/NOTICE).
