# Release Notes Skills

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

Turn a reviewed change list into a draft release note for a maintainer to approve.

## Included skills

| Skill | Input and result |
| --- | --- |
| [Draft release notes](skills/draft-release-notes.md) | A change list and version produce a draft grouped by user-visible effects |

This fictional distribution contains instructions only: no hooks, executable scripts, or automatic publishing. It assumes a host that can load skill instructions; no host/version compatibility is certified here.

## Install one way

For an actual distribution, publish the host-specific installation command and the exact package identity. Alternatively, let users copy the skill directory to the host's documented discovery location. Do not install both a managed package and a copied version of the same skill.

This documentation example is not an installable skill. Its component file deliberately uses ordinary Markdown rather than an active `SKILL.md`.

## First use

Explicitly invoke the installed draft-release-notes skill using your host's invocation syntax:

> Draft release notes for version 1.2 from this reviewed change list. Mark uncertain behavior as a question. Do not publish anything.

Expected result: a draft for review, with unresolved questions separated from confirmed changes. The skill does not promise that the host will select it automatically.

## Data and behavior

The user supplies the change list. The host may send it to its model provider. The proposed skill returns text and does not change repository files. If a future release adds scripts or file writes, its requirements and this section must change together.

## Update and remove

Use the host's package manager for managed installations. For a copied skill, compare upstream changes before replacing your edited copy. Remove the installed package or copied directory and reload the host's resources. This design creates no separate state to delete.

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
