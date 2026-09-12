#!/usr/bin/env bash
# afterFileEdit: run the sibling Vitest spec if it exists (fail open).
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HOOK_DIR/run-related-tests.py"
fi

echo '{}'
