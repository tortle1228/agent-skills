# Document distributed tools and extensions

[Home](../README.md) · [Choose a type](../examples/README.md)

## Identify what executes

| Type | What the reader needs |
| --- | --- |
| Library | Integration, public API, supported platforms |
| CLI | Execution environment, inputs, outputs, exit status |
| Coding agent | Authentication, workspace, file/command authority, reviewing results |
| MCP server | Client connection, tools, data transfer, process lifetime |
| Skill | Host discovery/invocation, bundled scripts, outputs |
| pi extension/package | Host code loading and resources distributed together |

Instruction files do not imply an absence of execution or writes. Inspect scripts, external commands, and host permissions. A pi package can distribute extensions, skills, prompts, and themes together: an extension is a capability; a package is a distribution unit.

## Cover the lifecycle

1. **Prerequisites:** host/runtime/OS, accounts, external tools, paid services.
2. **Installation:** one recommended path first; explain user/project scope and version selection.
3. **Activation:** registration, reload/restart, or project trust if required.
4. **First success:** a concrete command or request and an observable result.
5. **Updates:** installation-specific upgrade path, compatibility changes, migrations.
6. **Removal:** distinguish the program from settings/history. Restore host settings if installation changed them.

Show default locations and required settings; link precedence rules and full options separately. If managed installation and a manual copy can duplicate resources, tell the user to choose one.

## State actual support and authority

Separate intended compatibility, configuration examples, and versions tested. Do not invent a tested matrix. Local hosting does not mean model context stays local. Document relevant file access, command execution, network use, credential storage, and automatic configuration changes.

Pi's official docs state that extensions run inside the host process with its OS permissions; do not describe that as an independent sandbox. Package declaration, resource discovery, and functioning behavior are different checkpoints.

## Evidence behind the guidance

- [Matt Pocock Skills](https://github.com/mattpocock/skills) distinguishes managed installation from editable copies and warns about duplicates.
- [pi-mcp-adapter configuration](https://github.com/nicobailon/pi-mcp-adapter/blob/main/docs/configuration.md) explains restoring built-in MCP after removing an adapter that changed its setting. This is not a property of every pi package.
- [pi-extensions](https://github.com/tmustier/pi-extensions) links a package catalog to component READMEs.

Official references: [pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md), [pi extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md). Checked 2026-11-10; recheck when the host changes.
