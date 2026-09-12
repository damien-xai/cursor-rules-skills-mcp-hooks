---
name: github
description: >
  Use the connected GitHub MCP for issues, pull requests, reviews, and
  repository data. Use when the user mentions GitHub, issues, PRs, reviews,
  branches, or runs /github.
---

# GitHub MCP

Call the connected GitHub MCP. Do not invent issue numbers, PR state, or SHAs.

## Procedure

1. If owner, login, or permission context is missing, call `get_me`.
2. Prefer `list_*` for “show all X”. Prefer `search_*` for keywords, authors, or
   natural language. Do not put `sort:` inside a search query string.
3. Page in batches of 5–10. Use `minimal_output: true` unless full bodies are needed.
4. Search issues with `search_issues` before `issue_write` (create) to avoid duplicates.
5. Pull request reviews: `pull_request_review_write` method `create`, then
   `add_comment_to_pending_review`, then `pull_request_review_write` method
   `submit_pending`.
6. Before `create_pull_request`, look for a PR template
   (`.github/PULL_REQUEST_TEMPLATE` or `pull_request_template.md`).
7. After each call, `.cursor/hooks/log-mcp.sh` records request and response.
   Do not commit `.cursor/logs/`.

If the GitHub MCP is unavailable, say so. Do not fall back to guessed API results.
