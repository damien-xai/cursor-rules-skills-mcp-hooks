#!/usr/bin/env bash
# afterFileEdit / afterTabFileEdit: format then prettier --check the edited file.
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HOOK_DIR/format-after-edit.py"
fi

echo '{}'
