---
name: add-cursor-rule
description: >
  Add a Cursor project rule as a .mdc file under .cursor/rules with the
  correct activation type. Use when the user wants a new rule, /create-rule,
  or runs /add-cursor-rule.
---

# Add a project rule

Create **one** `.mdc` file in `.cursor/rules/`. Do not put a plain `.md` there
(Cursor ignores it). Do not duplicate text that already lives in `AGENTS.md`
unless the new rule needs different activation.

## Pick the activation type

| User intent                             | Frontmatter                                              |
| --------------------------------------- | -------------------------------------------------------- |
| Every chat                              | `alwaysApply: true`                                      |
| Agent decides from a description        | `alwaysApply: false` and `description: ...` (no `globs`) |
| Only when matching files are in context | `alwaysApply: false` and `globs: pattern,pattern`        |
| Only when @mentioned                    | `alwaysApply: false`, omit `description` and `globs`     |

`globs` is a comma-separated string (see `.cursor/rules/sveltekit.mdc`).

## File shape

```markdown
---
description: one line, used for intelligent apply
globs: path/pattern/**/*.ext
alwaysApply: false
---

# Title

- Imperative bullets the agent can follow
- Point at a file in the repo instead of pasting a style guide
```

Name the file after the concern (`api-errors.mdc`), not the type.

## After writing

1. Show the user which of the four types they got and how to invoke it
   (`@filename` for manual).
2. If they also want a multi-step procedure, add a **skill** rather than
   stuffing a runbook into the rule. Offer `/` the new skill name; do not
   create it unless they ask.
