# Pi Session Label

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

Add a visible label to your current pi session and include a short handoff prompt.

## Requirements and contents

This fictional package targets a pi version whose extension API has been checked by its publisher. No numeric compatibility floor is claimed without that check. pi extensions execute inside the host process with its OS permissions.

| Resource | Purpose |
| --- | --- |
| [Session label extension](docs/session-label.md) | Register `/session-label` and display its value |
| [Handoff prompt](docs/handoff.md) | Ask the agent to summarize progress and remaining work |

A distribution can declare the resources in its package manifest:

```json
{
  "name": "example-pi-session-label",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions/session-label.ts"],
    "prompts": ["./prompts/handoff.md"]
  }
}
```

Those resource paths describe the fictional package; they are not implemented in this example directory.

## Install and activate

The URL below is intentionally non-installable. A publisher must replace it with a real source and version.

```sh
pi install --local git:https://example.invalid/pi-session-label.git@v1.0.0
```

This demonstrates a project-scoped declaration. Without `--local`, pi uses personal settings. Follow the host's project trust flow and reload resources with `/reload` when the agent is idle, or restart pi. Confirm that the extension command appears.

## First use

```text
/session-label release-review
```

The proposed extension shows `release-review` in the session UI. It changes no model, approval rule, or built-in extension. Its label is in memory and resets on reload; the bundled prompt sends its text through the normal agent conversation.

## Update and remove

This illustration pins a Git tag. To move to another tag, replace the configured source with the new version using the host's documented package management flow. Recheck compatibility and reload. Do not promise that an update command advances an explicitly pinned tag.

Remove the same project-scoped source:

```sh
pi remove --local git:https://example.invalid/pi-session-label.git@v1.0.0
```

Reload or restart to unload it. This design has no files to clean up beyond the host-managed installation and declaration. A package that changes other host settings must document how to restore them.

Official references: [package lifecycle](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md), [extension permissions and reload](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md).

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
