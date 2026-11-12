#!/usr/bin/env bash
# Integration check against the staging sync service.
set -eu
: "${SYNC_TOKEN:?SYNC_TOKEN is not set}"
python3 -c "import sync; print(sync.push(b'{}'))"
