---
name: readme-writer
description: Write, improve, or translate project READMEs using repository evidence and project-specific examples. Use for new READMEs, targeted edits, onboarding improvements, and language synchronization; not general code review or unrelated documents.
---

# README Writer

Help the reader understand the project, complete a first task, and find the right details. Preserve the user's scope, intended audience, existing conventions, and requested output language. These instructions are English; the output need not be.

## Choose the amount of work

- **New README:** inspect the manifest, entrypoints, public interface, configuration, tests, and existing docs. Identify the reader and shortest successful workflow. Use only relevant sections.
- **Targeted edit:** inspect the affected claim and its source. Preserve unrelated content, structure, language, and intentional choices. Do not turn a small edit into a full rewrite.
- **Broader improvement:** prioritize incorrect commands, missing prerequisites, misleading claims, and unclear first use before style. Separate user setup from contributor setup.
- **Translation:** preserve supported features, requirements, limitations, and link destinations. Update the requested language variants together; do not silently add languages.

## Read selectively

Resource paths below are relative to this skill directory, not the target project.

- For writing or substantial restructuring, read [writing principles](guides/writing.md).
- Choose the closest type in [examples](examples/README.md), then read that example and explanation only if useful. Templates in [templates](templates/README.md) are optional drafting aids, not mandatory outlines.
- For installers, agents, skills, MCP servers, or pi packages, consult [distribution](guides/distribution.md).
- For images, translations, or expandable content, consult [GitHub formatting](guides/github-formatting.md).
- For licensing questions, consult [licensing](guides/licensing.md). Never assign a license without authorization.
- For a full update or final review, consult [maintenance](guides/maintenance.md).

Research in `references/` is background evidence. Do not load the entire collection by default. Fictional examples demonstrate writing choices; their APIs, versions, commands, and capabilities are not facts about the target repository.

## Ground claims and finish

Verify setup and usage against actual configuration and current official documentation when API behavior matters. Use available documentation tools; this skill requires no specific connector. Test presence is not proof of a passing test run. Distinguish designed support, configuration examples, and environments actually tested.

Do not invent badges, benchmarks, guarantees, downloads, or missing link targets. Keep important limits visible. Local hosting does not imply that data never reaches a model provider. Link detailed reference material instead of maintaining multiple copies.

Validate changed relative links, examples, image paths, and affected language variants. Run relevant commands only within the authorized scope. Report what changed, what was checked, and what remains unverified. README work alone does not authorize modifying product code, committing, publishing, installing dependencies, or changing unrelated settings.
