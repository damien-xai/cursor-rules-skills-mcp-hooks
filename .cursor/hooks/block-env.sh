#!/usr/bin/env bash
# Deny agent reads/writes of .env files (secrets). Allows .env.example and .env.test.
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HOOK_DIR/block-secrets.py"
fi

# Fail open if python3 is missing so the agent loop is not bricked.
echo '{"permission":"allow"}'
