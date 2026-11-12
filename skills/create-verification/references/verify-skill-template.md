# Template for verify-<app>/SKILL.md

Copy this skeleton, then replace every `<...>` with what this repo actually uses. Leave no placeholder behind.

The `description` is the only thing a future agent sees before deciding to open this skill, so write it to be found: name the app and its surface, the concrete files, commands, or features it covers, and the words a user would actually say (run it, start it, screenshot it, check it works, demo it).

````markdown
---
name: verify-<app>
description: >-
  Launch <app> and drive its <surface> the way a user does, to prove a change
  works. Use when verifying changes to <files, commands, or features it covers>,
  or when asked to run, start, screenshot, demo, or check <app>.
---

# Verify <app>

## Launch

- Command: `<exact start command>`
- Ready when: `<log line, prompt, or URL that answers with a usable page>`
- Starts from an empty data dir: `<migration and seed commands>`
- Teardown: `<how to stop what this run started>`

## Doctor

Read-only. Run first, and again after any failed drive.

- `<command>`: confirms `<process up, expected build, port owned by us, auth valid>`

## Drive

- Tool: `<Playwright script | tmux session | curl>`
- Handles: `<selectors, prompt strings, routes>`
- Example: `<one real command that exercises the main feature>`

## Evidence

- Save to: `<directory that survives cleanup>`
- Capture: `<screenshots | terminal transcript | response body | exit code | DB rows>`
- Check side effects: `<files written, rows inserted, messages sent>`

## Cleanup

Stop only what this run started (`<pid file or session name>`). Keep the evidence directory.

## Features

See [features/README.md](features/README.md).
````

## Feature file shape (`features/<feature>.md`)

````markdown
# <Feature>

<One sentence: what it is, from the user's side. State the observable end state that proves it works.>

## Sub-features

- <variant or option worth driving>

## How to get to it (user POV)

<Menu path, command, or route a user takes.>

## Driving it

<The exact steps with this repo's harness.>

## Gotchas

<Preconditions, seed data, timing, known failures with their reason.>
````
