#!/usr/bin/env bash
# afterMCPExecution entrypoint. Reads hook JSON on stdin; logs request + response.
# Tail with: tail -f .cursor/logs/mcp.log
set -euo pipefail

ROOT="$(pwd)"
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT/.cursor/logs"
mkdir -p "$LOG_DIR"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$HOOK_DIR/log-mcp.py"
fi

# Fallback when python3 is missing: append raw stdin so tailing still works.
{
  printf '======== %s  afterMCPExecution  python3 missing ========\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  cat
  printf '\n'
} >> "$LOG_DIR/mcp.log"
echo '{}'
