#!/usr/bin/env bash
set -eu
# Recreate the fixture repo: commit the base, then leave the change uncommitted.
cp -R "$(dirname "$0")/files/repo/." .
git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.com commit -qm base
git apply "$(dirname "$0")/files/change.patch"
