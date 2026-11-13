#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
cd repo && git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "initial"
