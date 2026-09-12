# Cursor template: rules, skills, MCP, and hooks

Project config for tailoring Cursor to a SvelteKit codebase, plus a connected
**GitHub** MCP for issues and pull requests.

| Mechanism                                | Role                                          |
| ---------------------------------------- | --------------------------------------------- |
| [Rules](https://cursor.com/docs/rules)   | Persistent standards injected into context    |
| [Skills](https://cursor.com/docs/skills) | On-demand workflows the agent invokes         |
| [MCP](https://cursor.com/docs/mcp)       | Tools, data, and APIs outside the repo        |
| [Hooks](https://cursor.com/docs/hooks)   | Scripts that run at agent-loop trigger points |

## Team-level shared settings

This repo is **project** config. Team-shared settings live in the dashboard:

| Shared setting | Dashboard                                                                       |
| -------------- | ------------------------------------------------------------------------------- |
| Rules          | [Team content → Rules](https://cursor.com/dashboard/team-content?section=rules) |
| Skills         | [Plugins](https://cursor.com/dashboard/plugins)                                 |
| MCP            | [Integrations](https://cursor.com/dashboard/integrations)                       |
| Hooks          | [Team content → Hooks](https://cursor.com/dashboard/team-content?section=hooks) |

## Layout

```text
AGENTS.md                          # always-on agent instructions
.cursor/
  rules/
    always-project.mdc             # Always Apply
    github.mdc                     # Apply Intelligently (GitHub MCP)
    sveltekit.mdc                  # Apply to Specific Files (SvelteKit)
    testing.mdc                    # Apply to Specific Files (*.spec.ts)
    ui-security.mdc                # Apply to Specific Files (*.svelte)
    ui-design.mdc                  # Apply to Specific Files (*.svelte, *.css)
    api-security.mdc               # Apply to Specific Files (API + server)
    manual-pr-checklist.mdc        # Apply Manually (@mention)
  skills/
    add-cursor-rule/SKILL.md
    frontend/                      # UI / compact layout / API / state / tests
    browser-testing/SKILL.md       # live browser verify + density checks
    github/SKILL.md                # GitHub MCP workflows
  mcp.json                         # no extra project servers (GitHub is a plugin)
  hooks.json                       # event → command (paths from repo root)
  hooks/                           # scripts stdin JSON, stdout JSON
    log-mcp.sh                     # afterMCPExecution
    log-mcp.py
    block-secrets.sh               # .env paths + credential-like strings
    block-secrets.py
    format-after-edit.sh           # afterFileEdit / afterTabFileEdit
    format-after-edit.py
    run-related-tests.sh           # afterFileEdit: sibling Vitest spec
    run-related-tests.py
  logs/                            # gitignored MCP transcripts
```

## Quick start

1. Open this folder in Cursor.
2. Confirm **Customize → MCP** shows the GitHub server enabled.
3. Tail MCP traffic:

   ```bash
   tail -f .cursor/logs/mcp.log
   ```

4. Ask something GitHub can answer, for example:
   _“Who am I on GitHub, and list this repo’s open issues.”_
5. Watch `.cursor/logs/mcp.log` append the GitHub tool request and response.

`python3` is required for the hooks.

## Rules

Cursor merges applicable sources. When they conflict,
**Team Rules → Project Rules → User Rules**.

| File                      | Frontmatter             | When it loads                                |
| ------------------------- | ----------------------- | -------------------------------------------- |
| `AGENTS.md`               | none                    | Every session in this directory              |
| Nested `AGENTS.md`        | none                    | When the agent works in that directory       |
| `always-project.mdc`      | `alwaysApply: true`     | Every session                                |
| `github.mdc`              | `description`, no globs | Agent pulls it in for GitHub work            |
| `sveltekit.mdc`           | `globs`                 | `.svelte` / SvelteKit route and server files |
| `testing.mdc`             | `globs`                 | `*.spec.ts` / `*.test.ts`                    |
| `ui-security.mdc`         | `globs`                 | `**/*.svelte` in context                     |
| `ui-design.mdc`           | `globs`                 | `**/*.svelte` / `*.css` in context           |
| `api-security.mdc`        | `globs`                 | API / `$lib/server` / `*.server.ts`          |
| `manual-pr-checklist.mdc` | neither                 | Only `@manual-pr-checklist`                  |

## MCP

GitHub is connected as a **Cursor plugin** (not an entry in
`.cursor/mcp.json`). Typical tools: `get_me`, `list_issues`, `search_issues`,
`issue_write`, `list_pull_requests`, `create_pull_request`,
`pull_request_review_write`.

Project `.cursor/mcp.json` is an empty `mcpServers` object so we do not pull
in extra remotes. Enable GitHub under Customize → MCP if tools are missing.

After each MCP call, `afterMCPExecution` logs request and response. Every
project hook also appends one line to `hooks.log`. Tail with:

```bash
tail -f .cursor/logs/hooks.log
tail -f .cursor/logs/mcp.log
```

## Hooks

| Event                                                                           | Script                 | Job                                            |
| ------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------- |
| `afterMCPExecution`                                                             | `log-mcp.sh`           | Audit GitHub (and any other) MCP calls         |
| `beforeShellExecution` / `beforeReadFile` / `beforeSubmitPrompt` / `preToolUse` | `block-secrets.sh`     | Block `.env` paths and credential-like strings |
| `afterFileEdit` / `afterTabFileEdit`                                            | `format-after-edit.sh` | Prettier `--write` then `--check`              |
| `afterFileEdit`                                                                 | `run-related-tests.sh` | Vitest on the sibling `*.spec.ts` if it exists |

## Skills

| Skill             | Invoke                                                  |
| ----------------- | ------------------------------------------------------- |
| `github`          | Automatic on GitHub / issue / PR work, or `/github`     |
| `frontend`        | Automatic on SvelteKit UI / API / state, or `/frontend` |
| `browser-testing` | Automatic on e2e / UI verify / design review, or `/browser-testing` |
| `add-cursor-rule` | `/add-cursor-rule` when adding a `.mdc` file            |

## Docs

- Cursor: [Rules](https://cursor.com/docs/rules) · [Skills](https://cursor.com/docs/skills) · [MCP](https://cursor.com/docs/mcp) · [Hooks](https://cursor.com/docs/hooks)
- Dashboard: [Rules](https://cursor.com/dashboard/team-content?section=rules) · [Plugins](https://cursor.com/dashboard/plugins) · [Integrations](https://cursor.com/dashboard/integrations) · [Hooks](https://cursor.com/dashboard/team-content?section=hooks)
