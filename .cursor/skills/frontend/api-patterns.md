# API patterns

1. Handlers live at `src/routes/api/<path>/+server.ts`.
2. Export `GET` / `POST` / `PATCH` / `DELETE` as `RequestHandler`.
3. Parse JSON defensively. Use `error(400, ...)` for bad input and
   `error(404, 'not found')` when a resource is missing.
4. Return `json(body, { status })` or `new Response(null, { status: 204 })`.
5. Put mutations in `$lib/server/`. Keep types in `$lib` so the client can
   import the shape without the store.
6. Extend the colocated `*.spec.ts` for store changes. Run `npm test` next to
   the nearest `package.json`. Do not start the dev server.
