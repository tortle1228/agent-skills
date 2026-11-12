# Write for the reader

[Home](../README.md) · [Choose an example](../examples/README.md) · [AI workflow](ai-writing.md)

A README helps a newcomer understand a project and choose a next action. There is no universal length or section count. A large project may need a map to established documentation; a small library may need a complete usage example.

## Establish the facts

Identify the primary reader, the task the project solves, prerequisites for a first success, and the observable result. Separate implemented behavior from plans. Read the manifest, entrypoints, public interfaces, configuration, tests, and existing docs. File names alone do not establish capabilities. A test's presence does not mean it passed.

## Choose a useful order

Start with purpose, a result or example, prerequisites, the shortest working path, and links to more detail. Complex software may need a short explanation before installation. These are candidates, not mandatory headings.

- **Purpose:** who the project helps and what task it performs.
- **Result:** a short API example, CLI input/output, or app screenshot and workflow.
- **Start:** working directory, dependencies, commands, and expected result together. Do not hide required extras after an example that needs them.
- **Decision information:** supported environments, accounts, costs, data handling, and important limits.
- **Next steps:** advanced configuration, API reference, help, contribution instructions, and the license.

Separate end-user installation from source development. Split details that obscure the first task or duplicate another maintained source; do not fragment every short document.

## Replace claims with observable behavior

| Weak claim | Better direction |
| --- | --- |
| Powerful, blazing-fast, production-ready | Describe the task; support performance claims with measurement conditions and results |
| Supports every agent | Distinguish tested hosts/versions from configuration examples |
| Completely local | Explain local processing/storage separately from data sent to model providers |
| Works immediately after installation | Include authentication, activation, reload, and external dependencies |
| Support coming soon | State current support and link plans separately |

“Preview filename changes before applying them” is more useful than “Seamlessly manage all your files,” but only when preview actually exists.

## Remove work for the reader and maintainer

Merge repeated introduction and feature lists. Link files a reader needs instead of reproducing a whole directory tree. Use badges for real status, versions, or licensing. GitHub already provides an outline, so a short page does not need a manual contents list. Comparisons need evidence and conditions; stars do not prove documentation quality.

A long README can work when its first task is easy to find. A short README with missing prerequisites cannot.

Sources: [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), [timeless documentation](https://developers.google.com/style/timeless-documentation), [observed examples](../references/README.md).
