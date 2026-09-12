# Testing

1. Add or extend `*.spec.ts` next to the module (not a separate `/tests` tree).
2. Import the module under test with a relative path. Use `beforeEach` to reset
   any module-level store.
3. Assert return values and edge cases (empty input, missing id, trim).
4. Next to the nearest `package.json`, run `npm test` (or
   `npx vitest run path/to/file.spec.ts`).
5. Do not start `npm run dev`. Do not remove failing tests to get a green run.
6. For a live UI pass, use `/browser-testing`. Do not put browser steps here.
7. After an agent edit, `.cursor/hooks/run-related-tests.sh` runs the sibling
   spec if one exists.
