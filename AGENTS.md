# Working on Agent Skills

- This repository packages several independent skills under `skills/<name>/`, plus one npm installer (`bin/`, `lib/`). Each skill must stay self-contained and host-neutral: name host features (subagents, tools, slash commands) only as examples, and never link outside its own folder.
- Skill instructions and references are English. Korean appears only in `README.ko.md` files, `evals/`, and agent-code-review's Korean label examples (`SKILL.md`, `references/report-format.md`). Keep every `README.ko.md` in sync with its `README.md`.
- Keep each `SKILL.md` brief and read supporting resources selectively. Skills may delegate to sibling skills by name (for example project-bootstrap → `git-hooks`, `project-instructions`) but must still work when the sibling is not installed.
- Behavior changes to a skill's `SKILL.md` or references need a rerun of that skill's `evals/` cases with and without the skill. `evals/` is not shipped.
- readme-writer examples describe fictional products. Never present their commands, APIs, compatibility, or results as verified implementations.
- `npm run verify` checks documentation, tests the installer in temporary homes, and installs a real packed archive. No test may modify the developer's real skill directories.
- The CLI and all skills share package.json's version. Keep package-lock.json, CHANGELOG.md, and vX.Y.Z release tags consistent.
- Publish only on an explicit release request. Inspect the packed allowlist before publication; never package credentials, temporary files, evals, or tests.
- Use focused commits: docs, feat, fix, test, ci, or chore. No automatic version bumps on ordinary commits.
