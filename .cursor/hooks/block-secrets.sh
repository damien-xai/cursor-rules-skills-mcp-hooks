#!/usr/bin/env bash
# Deny .env paths and credential-like strings in prompts, writes, and shell.
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HOOK_DIR/block-secrets.py"
fi

# Fail open if python3 is missing so the agent loop is not bricked.
echo '{"permission":"allow","continue":true}'
