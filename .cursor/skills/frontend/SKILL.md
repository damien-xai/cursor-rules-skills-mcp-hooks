---
name: frontend
description: >
  SvelteKit frontend workflows: compact layout, components, API routes,
  state, and Vitest. Use when adding a page, component, CSS, +server.ts
  endpoint, client/server state, or unit tests, or when the user runs
  /frontend.
---

# Frontend

SvelteKit + TypeScript + Svelte 5. Read only the file that matches the task:

| Task                              | Read                                               |
| --------------------------------- | -------------------------------------------------- |
| Component or page UI              | [component-guidelines.md](component-guidelines.md) |
| Layout, density, responsive, CSS  | [layout.md](layout.md)                             |
| REST / `+server.ts`               | [api-patterns.md](api-patterns.md)                 |
| Store, load, or client cache      | [state-management.md](state-management.md)         |
| Unit tests                        | [testing.md](testing.md)                           |

Any new page or visible UI change must also follow [layout.md](layout.md).
Do not start or restart the dev server. The user runs it.
