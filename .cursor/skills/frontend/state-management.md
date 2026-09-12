# State management

1. Server state (the source of truth) lives in `$lib/server/`. Module-level
   memory is fine for the demo; it resets when the process restarts.
2. Export named functions with explicit return types. Return copies, not the
   live array.
3. First paint: `+page.server.ts` `load` reads the server store.
4. After client mutations: `fetch` the API, then replace a client cache.
   Use `$derived(clientState ?? data.fromLoad)` so SSR data is not captured
   into `$state` once.
5. Client modules must not import `$lib/server/*`.
