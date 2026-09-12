# Hook logs

Project hooks append here so you can prove they ran. All `*.log` / `*.jsonl`
files are gitignored. This directory stays in git via `.gitkeep`.

| File | Source | What to do |
| --- | --- | --- |
| `hooks.log` | every hook (one line per run) | `tail -f .cursor/logs/hooks.log` |
| `hooks.jsonl` | same records as JSON | `tail -f .cursor/logs/hooks.jsonl` |
| `mcp.log` | `log-mcp.sh` full request/response | `tail -f .cursor/logs/mcp.log` |
| `mcp.jsonl` | MCP records as JSON | `tail -f .cursor/logs/mcp.jsonl` |

`block-secrets` logs `allow` / `deny` and a reason (`env_path` or
`credential_pattern`). It never writes the secret or the prompt.
