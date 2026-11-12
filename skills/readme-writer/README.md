# README Writer

[English](README.md) | [한국어](README.ko.md)

Write and improve project READMEs using repository evidence. README Writer includes an agent skill, seven worked examples, reusable templates, and guidance for people and agents.

Detailed guides and explanations are **English**. This entry page and the app example also have Korean versions. You can read the collection without installing anything.

## Install the skill

Requires Node.js 22.14 or later. This skill ships in the `@tortle1228/agent-skills` package; install only this skill into both local agents, or choose `codex` or `claude-code` instead of `all`:

```sh
npx @tortle1228/agent-skills@latest install --agent all --skill readme-writer
```

Then use `$readme-writer` in Codex or `/readme-writer` in Claude Code. Ask for a new README, a scoped edit, or a translation, and specify your output language. Skill discovery is automatic in supported hosts; reload or restart if it does not appear.

The installer copies the bundled resources to `~/.agents/skills/readme-writer` (Codex) and `~/.claude/skills/readme-writer` (Claude Code). It does not depend on the npm cache afterward and does not run at `npm install` time.

Run the same command from a newer version to update. To pin a release, replace `latest` with its version. Modified, unmanaged, or symlinked installations are left untouched and reported as conflicts. Back up your edits and deliberately remove or relocate the conflicting installation before retrying; there is no force option.

```sh
npx @tortle1228/agent-skills@latest uninstall --agent all --skill readme-writer
```

Removal only affects unmodified installations owned by this installer. It never deletes the source repository. Running with no arguments displays help without changing files.

Alternatively, install from GitHub using the separate Skills CLI:

```sh
npx skills add tortle1228/agent-skills --skill readme-writer -g -a codex -a claude-code
```

The npm installer supports Codex and Claude Code. For other agents that load Agent Skills (`SKILL.md`), such as Antigravity, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or OpenCode, use the Skills CLI with that agent's name, for example `-a cursor`.

Choose one installation method per host. The Skills CLI manages its own updates/removal; this package does not overwrite its installation.

## Read and adapt

1. Read the [writing principles](guides/writing.md).
2. Choose a type below and compare its example with the explanation.
3. Fill the template with your project's actual facts; omit irrelevant sections.
4. Use the [review checklist](guides/maintenance.md).

| Type | Example | Explanation | Template |
| --- | --- | --- | --- |
| Swift package | [Example](examples/swift-package/README.md) | [Why](examples/swift-package/EXPLAIN.md) | [Template](templates/swift-package.md) |
| CLI | [Example](examples/cli/README.md) | [Why](examples/cli/EXPLAIN.md) | [Template](templates/cli.md) |
| App | [Example](examples/app/README.md) | [Why](examples/app/EXPLAIN.md) | [Template](templates/app.md) |
| MCP server | [Example](examples/mcp-server/README.md) | [Why](examples/mcp-server/EXPLAIN.md) | [Template](templates/mcp-server.md) |
| Coding agent | [Example](examples/coding-agent/README.md) | [Why](examples/coding-agent/EXPLAIN.md) | [Template](templates/coding-agent.md) |
| Skill package | [Example](examples/skill-package/README.md) | [Why](examples/skill-package/EXPLAIN.md) | [Template](templates/skill-package.md) |
| pi extension/package | [Example](examples/pi-package/README.md) | [Why](examples/pi-package/EXPLAIN.md) | [Template](templates/pi-package.md) |

## Guides

- [Writing principles](guides/writing.md)
- [Images, languages, and linked docs](guides/github-formatting.md)
- [Distributed packages](guides/distribution.md)
- [Writing with AI](guides/ai-writing.md)
- [Maintenance](guides/maintenance.md)
- [License information](guides/licensing.md)

[Research notes](references/README.md) cover classic projects, a dated 20-repository Trending sample, agents/skills/pi packages, and Awesome README. Observations are not product audits or quality rankings.

## Development and license

Contribution and release instructions and the changelog live in the `@tortle1228/agent-skills` repository. Examples are fictional: they do not implement the illustrated products. README Writer is a writing skill, not a README generation service or hosted site.

Original code, documents, templates, and mockups are under the [MIT License](LICENSE). External references retain their own terms.
