# Work Tracking

[English](README.md) | [한국어](README.ko.md)

An agent skill that decides once where a repository's planned work and decisions live, records the rule in a few lines, and stops agents from creating and syncing roadmap, ADR, and research documents on their own.

## What it does

It inspects the repository, then asks one question at a time and recommends an answer:

| Choice | Planned work lives in | Section written |
| --- | --- | --- |
| GitHub Issues | Issues via `gh`, with `roadmap`, `backlog`, and `when-needed` labels | [issues](assets/section-issues.md) |
| Single file | One `ROADMAP.md`, one line per item | [roadmap](assets/section-roadmap.md) |
| No tracker documents | Code comments and commit bodies, with a `Decision:` trailer | [commits](assets/section-commits.md) |

It also asks where to record the choice: a short "Work tracking" section in `AGENTS.md` (recommended) or a separate `docs/agents/work-tracking.md`. It shows the draft and writes only after you confirm.

Every section carries the same scale rules: record a finding once, keep the instructions file to commands and pitfalls, and create ADR or research documents only on request.

Invoke it as `$work-tracking` in Codex or `/work-tracking` in Claude Code, or describe the task.

## What runs and what changes

- Inspection is read-only: `git remote -v`, `gh repo view`, `gh issue list`, and a look for `ROADMAP.md`, `docs/`, and an existing "Work tracking" section. An existing section is never overwritten.
- Labels are created with `gh label create` only after you confirm. The skill never creates issues.
- The only file it writes is the section (or the one file you chose).

## Install

Requires Node.js 22.14 or later.

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill work-tracking
```

Alternatively, install from GitHub with the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill work-tracking -g -a codex -a claude-code
```

Remove it with `npx @tortle1228/agent-skills@latest uninstall --agent all --skill work-tracking`.

## License

[MIT](LICENSE).
