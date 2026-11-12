# Nameplan

> Fictional documentation example. This project is not distributed; commands, APIs, versions, and results below describe an illustrative design, not a tested product. URLs under `example.invalid` are intentionally non-installable.

Preview a batch filename change before applying it.

## Before you start

This illustrative CLI targets macOS and Linux. Work on a directory you own and keep a backup before applying renames. It changes filenames, not file contents.

## Install

Download the binary matching your OS and architecture from your project's release page, verify it using the published checksum, and put it on your PATH. This fictional project has no release download.

## Preview, then apply

Run from the folder containing the files:

```sh
nameplan preview --replace ' ' '-' ./photos
```

Illustrative output:

```text
family trip.jpg -> family-trip.jpg
No files changed. 1 rename planned.
```

Inspect the plan before applying the same operation:

```sh
nameplan apply --replace ' ' '-' ./photos
```

The proposed behavior refuses conflicting destination names. It only visits direct children of the chosen folder; it does not follow directory symlinks or recurse.

## Results and limits

A successful preview or apply exits with status 0. Invalid input or a collision exits with status 1 and prints a diagnostic to stderr. A filesystem failure during apply can leave a partially applied operation; use your backup to recover. This example does not promise transactional rollback.

## Update and remove

Replace the installed binary with a compatible release to update. Remove that binary to uninstall. The proposed CLI keeps no configuration or background process. Include the command and diagnostic, with private paths removed, when reporting a problem.

## License

This fictional product has no separate release license. The documentation example itself is covered by the repository’s [MIT License](../../LICENSE).
