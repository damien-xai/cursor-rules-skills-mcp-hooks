# Agent instructions

This repository is a **Cursor template** for rules, skills, MCP, and hooks.
Use **SvelteKit** when building the UI and API. Put new application code where
the user says.

## What lives where

| Need | Put it here | Loaded when |
| --- | --- | --- |
| Always-on, cross-tool instructions | `AGENTS.md` (this file, and nested copies) | Every agent session in this tree |
| Scoped / typed project rules | `.cursor/rules/*.mdc` | Always, by glob, by relevance, or by `@mention` |
| On-demand workflows | `.cursor/skills/<name>/SKILL.md` | Agent decides, or user types `/skill-name` |
| External tools | Connected MCP (GitHub plugin) + `.cursor/mcp.json` | Workspace load |
| Deterministic intercepts | `.cursor/hooks.json` + `.cursor/hooks/` | Before/after agent-loop events |

**User** settings live in Cursor Settings. **Team-level shared settings** are
managed in the dashboard, not in git.

A plain `.md` file in `.cursor/rules/` is **ignored**. Project rules must be
`.mdc` with YAML frontmatter. A nested `AGENTS.md` applies when the agent
works in that directory.

## Working in this repo

- Treat `.cursor/` as the product. Follow the user's path for new SvelteKit
  code. Do not invent a second project at the repo root unless they ask.
- There is no existing application source tree. List the directory before
  claiming files exist. Do not assume a previous demo.
- Prefer editing rules, skills, MCP config, and hooks over drive-by refactors.
- For GitHub issues, PRs, reviews, or repo metadata, call the connected
  **GitHub** MCP. Start with `get_me` if owner or permission context is missing.
- After MCP tool calls, a project hook appends request and response to
  `.cursor/logs/mcp.log`. Every hook also appends one line to
  `.cursor/logs/hooks.log`. Do not commit those transcripts.
- After file edits, hooks run Prettier write + check and the sibling Vitest
  spec if one exists (`.cursor/hooks/format-after-edit.sh`,
  `.cursor/hooks/run-related-tests.sh`).
- A secrets hook blocks `.env` paths and credential-like strings
  (`.cursor/hooks/block-secrets.sh`).
- Keep new rules under ~500 lines and split by concern. Keep skill bodies
  procedural.

## Pointers

- Rules: `.cursor/rules/`
- Skills: `.cursor/skills/`
- MCP: GitHub plugin; `.cursor/mcp.json` has no extra project servers
- Hooks: `.cursor/hooks.json`
