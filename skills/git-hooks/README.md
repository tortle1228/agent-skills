# Git Hooks

[English](README.md) | [한국어](README.ko.md)

An agent skill that sets up, audits, and troubleshoots Git hooks fast enough that nobody has a reason to skip them, and verifies them with real commits and pushes.

## What it does

Ask for the guard you want, for example:

> Run lint and a secret scan before every commit, and make it work for teammates after they clone.

The skill inspects the repository, picks a hook manager that fits it, places each check in the right hook, and proves the result with real Git commands. Its final report names the tool it chose and why, the scenarios it ran, how to bypass in an emergency, and what still needs server-side enforcement.

| Situation | Usual choice |
| --- | --- |
| No extra dependencies wanted | Git's built-in `core.hooksPath` with a committed `.githooks/` folder |
| Polyglot or monorepo | Lefthook |
| Python-centric | `pre-commit` or `prek` |
| Single Node.js package | Husky with `lint-staged` and `commitlint` |

Checks it knows how to place:

- **pre-commit:** staged-only secret scan (gitleaks when installed, built-in patterns otherwise), `.env` and key files, conflict markers, large files, case collisions, and lint on changed files. When the skill adds an auto-fixing formatter, it keeps unstaged edits out of the commit and proves it with a partially staged file.
- **commit-msg:** Conventional Commits with subject length counted in characters, so Korean and other non-ASCII subjects are not rejected early.
- **prepare-commit-msg:** issue keys from the branch name added as a trailer.
- **pre-push:** protected branches with an explicit override, `WIP`/`fixup!` commits, and the first push of a new branch.
- **post-checkout / post-merge:** reminders when lockfiles or migrations changed.

Invoke it as `$git-hooks` in Codex or `/git-hooks` in Claude Code, or just describe the task. The [hook catalog](references/hook-catalog.md) covers each hook's arguments and common pitfalls.

## What runs and what changes

- The agent writes hook files and hook-manager config into your repository and sets `core.hooksPath` in the repository's local Git config. It does not change your global Git config.
- [`scripts/install-hooks.sh`](scripts/install-hooks.sh) copies the six POSIX hooks from [`examples/githooks/`](examples/githooks/) into `<repo>/.githooks/` and sets `core.hooksPath`. Existing files with the same names are overwritten.
- Hooks need `git` and a POSIX shell. gitleaks, Lefthook, and `pre-commit` are optional and used only when present or chosen.
- To verify, the agent makes test commits, and for `pre-push` a local bare remote, then removes what it created.

## Install

Requires Node.js 22.14 or later.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill git-hooks
```

Or install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill git-hooks -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/git-hooks` (Codex) and `~/.claude/skills/git-hooks` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched. Removing the skill does not remove hooks already installed in your repositories.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill git-hooks
```

## License

[MIT](LICENSE).
