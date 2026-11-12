# Patchpilot

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

A terminal coding assistant that proposes a small patch and lets you inspect the result.

## Requirements

This fictional design targets macOS and Linux, with Git and an account for its configured model provider. Provider usage may incur charges. No binaries or provider integrations are shipped with this example.

## Start in a project

Install the appropriate binary from your project's release page, then open a disposable copy of a repository:

```sh
cd sample-project
patchpilot login
patchpilot
```

The proposed login flow stores a provider token in the OS credential store. It must explain the provider and account before requesting credentials. Do not put tokens in a tracked project file.

## First task

Ask: “Explain how this project runs its tests. Do not edit files.”

Expected behavior: the assistant identifies the relevant configuration and reports the test command with file references. For a subsequent edit request, inspect the proposed patch and command before approving it. Review the resulting Git diff and run the relevant tests yourself.

## Execution and data

The illustrative default asks before writing files or running commands. Approval is a workflow control, not an OS sandbox. The assistant can read files available to its process, and selected repository context is sent to the configured provider. Do not assume ignored files are a security boundary.

## Update and remove

Replace the binary with a compatible release. Read migration notes before reusing old configuration. Uninstalling the binary does not revoke provider credentials: sign out first, then remove the binary. Delete local conversation history separately if desired.

## Report a problem

Include the version, operating system, action, and sanitized error. Never attach credentials or private source without reviewing it. This example has no issue tracker or implemented behavior.

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
