# Contributing and releasing

[Home](README.md)

Use Node.js 22.14 or later. The installer has no runtime dependencies.

```sh
npm ci
npm run verify
```

`verify` checks documentation links and language scope, tests the installer in temporary directories, and installs a real packed tarball into temporary homes. Tests never install into your actual agent directories. Local previews do not prove GitHub rendering; report the renderer and checks used.

## Editing

Each skill lives in `skills/<name>/` and must work on its own once installed: relative links may not leave the skill folder (the installer adds `LICENSE` at its root). Keep each `SKILL.md` concise and load supporting files selectively. Skill instructions and references are English; Korean appears only in `README.ko.md` files, `evals/`, and agent-code-review's Korean label examples. Keep each `README.ko.md` in sync with its `README.md`. Original materials are MIT; referenced projects retain their own terms. In readme-writer, preserve the distinction between fictional examples and working software.

To add a skill, create `skills/<name>/SKILL.md` whose frontmatter `name` matches the folder, add `agents/openai.yaml` and README files, list it in the home READMEs, and update the expected skill lists in `test/` and `scripts/check-pack.js`. Behavior changes to a skill that has `evals/` need a rerun of those cases with and without the skill; `evals/` is never packaged or installed.

Use focused commits such as `docs:`, `feat:`, `fix:`, `test:`, `ci:`, or `chore:`. No commit hook or automatic version inference is required. Research additions should include source, observation date, and what the README teaches.

## Versions

The CLI and all bundled skills share package.json's version. While at 0.x, compatible fixes use patch releases; features and breaking changes use minor releases. Explain breaking behavior and migration in CHANGELOG.md. Move to 1.0.0 when the compatibility contract is stable. After 1.0, use normal semantic versioning.

Prepare the changelog, run checks, and commit the change before incrementing from a clean worktree:

```sh
npm version patch -m "chore: release %s"
git push origin main --follow-tags
```

Choose `minor` or `major` deliberately instead of `patch` when appropriate. `npm version` updates package/lock files and creates a commit/tag; it does not publish npm or a GitHub Release. Create the GitHub Release for the resulting `vX.Y.Z` tag to trigger publication.

## First publication and OIDC

The initial 0.1.0 package is bootstrapped by an authenticated maintainer with `npm publish --access public` after `npm run verify` and inspection of the tarball. Browser login/2FA is interactive; do not commit credentials or store them in logs. The npm package name is `@tortle1228/agent-skills`; the repository and executable are `agent-skills`.

A successful publish command can precede public availability. Confirm the intended version and MIT license with `npm view @tortle1228/agent-skills version license --prefer-online` before announcing availability. If npm displays a temporary `0.0.0-stage` version, inspect Staged Packages; do not mistake the placeholder for the release or republish the same version while it is processing. Test the public installer from outside this source checkout, where npm cannot resolve the local package instead of downloading the published one.

Configure an npm Trusted Publisher for `tortle1228/agent-skills`, workflow `publish.yml`, with direct `npm publish` allowed. Enable the repository Actions variable `NPM_PUBLISH_ENABLED=true` only after bootstrap and the first GitHub Release have completed. Subsequent releases publish on GitHub-hosted runners with OIDC and provenance, without a stored npm token. A missing variable intentionally skips the bootstrap publish job. Verify that the connection appears in npm settings after authentication; the separate Update Package Settings action does not create a trusted publisher. If npm marks the connection Pending validation, complete a trusted publication before the deadline shown there and verify both the workflow result and public package metadata.

For a failed workflow, inspect its result before rerunning. If the version already exists on npm, do not overwrite its tag or silently increment it. Reconcile the published version first. A failed npm publish can leave a GitHub Release without a package; its existence is not proof of publication.

Sources: [npm version](https://docs.npmjs.com/cli/v11/commands/npm-version), [semantic versions](https://docs.npmjs.com/about-semantic-versioning), [trusted publishing](https://docs.npmjs.com/trusted-publishers), [workflow triggering](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow).

## Installation ownership

Use either this npm installer or the separate Skills CLI for each skill and host, not both. The npm installer records file hashes per skill and refuses to replace symlinks, other installations, or local edits. Preserve your edits and deliberately move/remove a conflicting installation before reinstalling. Removing a skill never removes this source repository.
