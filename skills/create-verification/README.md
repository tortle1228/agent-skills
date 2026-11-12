# Create Verification

[English](README.md) | [한국어](README.ko.md)

An agent skill that reads a repository and writes a project-local `verify-<app>` skill: a recipe for launching the real app, driving it the way a user does, and capturing evidence. The generated skill is run once before it is handed over.

## What it does

Ask for it when a repo has no scripted way to prove UI, CLI, or service behavior, for example:

> Make a verification skill for this repo so an agent can actually run it and show me it works.

The skill answers its questions from the code (what the user touches, how the app starts, how to drive and observe it, whether two instances can run side by side) and asks you only for what it cannot see. It then writes:

- `verify-<app>/SKILL.md` with **Launch**, **Doctor**, **Drive**, **Evidence**, **Cleanup**, and any helper scripts, using this repo's real commands and selectors.
- `verify-<app>/features/` with an index and one file for each of the top three to five user-facing features. The [template](references/verify-skill-template.md) shows the shape.

Then it follows its own recipe once: launch, doctor, drive one feature, capture evidence, clean up, and confirm the evidence survived. It also shows the check can fail by breaking one behavior in a scratch copy of the repo. If the app does not build or start, it reports exactly why instead of writing a placeholder recipe. A recipe proved in a stand-in environment lists the steps the real target will still need.

Invoke it as `$create-verification` in Codex or `/create-verification` in Claude Code. It pairs with the `verification` skill, which uses the generated recipe, but each works alone.

## What runs and what changes

- The agent writes files only under the new `verify-<app>/` folder in the project's local skills directory. It does not edit product code in your working tree.
- To show the check can fail, it breaks one behavior in a scratch copy of the repo and discards the copy afterwards.
- To prove the recipe, it builds and starts the app locally, drives one feature, and stops what it started. It may create a clearly marked scratch asset when an unrelated missing file blocks startup, and removes it afterwards.
- Evidence files are kept after cleanup, in the location the generated skill names.

## Install

Requires Node.js 22.14 or later.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill create-verification
```

Or install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill create-verification -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. Installed copies live in `~/.agents/skills/create-verification` (Codex) and `~/.claude/skills/create-verification` (Claude Code).

## Update and remove

Run the install command from a newer package version to update. Locally modified installations are reported as conflicts and left untouched. Removing the skill does not remove `verify-<app>` skills already generated in your repositories.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill create-verification
```

## License

[MIT](LICENSE).
