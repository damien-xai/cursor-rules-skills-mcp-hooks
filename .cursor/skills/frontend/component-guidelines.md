# Component guidelines

1. Put presentational pieces in `$lib/components/*.svelte`.
2. Use `<script lang="ts">`, `$props()`, and typed `on*` callbacks for events.
3. Colocate scoped `<style>` in the same file. Do not add a CSS framework unless asked.
4. Keep one idea per component. Pages in `src/routes/` compose components; they
   do not inline large markup.
5. Call the API with `fetch`. Do not import `$lib/server/*` from a component.
6. Compact, aligned, viewport-fitting layout is required. Follow
   [layout.md](layout.md) and `.cursor/rules/ui-design.mdc` before writing
   styles. Default control height is 32px, not 48px.
