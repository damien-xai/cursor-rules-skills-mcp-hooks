---
name: browser-testing
description: >
  Verify UI in a real browser: exercise the flow, then fail oversized,
  misaligned, or non-fitting layouts on desktop and mobile. Use when the
  user asks to browser-test, e2e, smoke-test, design-review, check mobile,
  fix alignment or density, or when they run /browser-testing.
---

# Browser testing

Exercise the running app the way a person would. A screenshot of first paint
is not a test. After the flow works, **measure** density and fit, then fix
what fails. Follow `.cursor/rules/ui-design.mdc` and
`.cursor/skills/frontend/layout.md`.

## Before you start

1. Do **not** start or restart the dev server. Ask the user for the URL if
   it is not already open.
2. Prefer the Cursor browser tools (navigate, snapshot, click, type, fill,
   screenshot). Do not add Playwright, Cypress, or another runner unless
   the user asks.
3. If no browser tools are available, say so. Use the closest substitute
   (`curl` against the URL they gave, or unit tests) and stop.

## Procedure

1. List open tabs. Navigate to the URL the user is running.
2. Snapshot the page. Drive the **main flow** end to end: click, type, submit,
   navigate. Confirm behavior, not only layout.
3. Hit every route that shares the state, data, or components you changed.
4. Check edge states the change can break (empty, error, loading, auth).
5. Run **Fit and density** (below) at the **current browser panel size**.
   Do not set a desktop width (no 1280×800, no device metrics override).
   Then set **mobile ~390×844** only, and run the main flow plus Fit and
   density again. Do not guess mobile from the panel screenshot. When the
   mobile pass is done, **clear the device override** so the page follows
   the panel again.
6. Run the **design review**. Fix CSS, then re-measure and re-screenshot
   the panel size and mobile. Stop only when measurements pass and the
   review is clean.

## Fit and density

Use the browser CDP `Runtime.evaluate` (`returnByValue: true`) on a
representative heading, text input, select, button, and the main column
(or `[data-shell]` if present):

```js
({
	vw: innerWidth,
	vh: innerHeight,
	scrollOverflow:
		document.documentElement.scrollWidth >
		document.documentElement.clientWidth + 1,
	bodyFont: getComputedStyle(document.body).fontSize,
	letterSpacing: getComputedStyle(document.body).letterSpacing,
	wordSpacing: getComputedStyle(document.body).wordSpacing,
	titlePx: title ? parseFloat(getComputedStyle(title).fontSize) : null,
	inputH: input ? input.getBoundingClientRect().height : null,
	buttonH: button ? button.getBoundingClientRect().height : null,
	shell: shell
		? {
				left: shell.getBoundingClientRect().left,
				right: innerWidth - shell.getBoundingClientRect().right,
				top: shell.getBoundingClientRect().top,
				width: shell.getBoundingClientRect().width
			}
		: null
})
```

**Fail and fix** if any of these are true:

| Check              | Fail when                                      |
| ------------------ | ---------------------------------------------- |
| Horizontal fit     | `scrollOverflow`                               |
| Column fit         | shell width > 42rem at the panel size, or left/right gutters differ by > 32px |
| Hero spacing       | first heading `top` > 72px                     |
| Body type          | body `font-size` > 16px                        |
| Title type         | heading `font-size` > 22px                     |
| Control height     | input/select/button height > 36px (not textarea) |
| Tracking           | `letter-spacing` or `word-spacing` not `normal` / `0px` |
| Words              | labels look tracked-out, colliding, or split mid-word |
| Mobile stack       | a multi-field row still sits in one line at 390px and overflows |

Do not “pass” a 44–48px control to satisfy tap-target folklore. Compact
visual height is 32–36px; use row padding for hit area.

## Design review

Take a screenshot (not only a snapshot) of each important state at the
panel size and at mobile.

- Title, form, and list share one left edge. Labels sit on their controls.
  Actions in a row share height and vertical center.
- Spacing is even: 8–12px gaps, not 24–32px. No collisions or clipped text.
- Pills: same radius (999px), compact padding, type ~12px. They do not
  jump the row height.
- Icons are one set and one optical size. No emoji.
- At the panel size the layout is a compact column, not a stretched
  dashboard and not a vertically centered poster. Mobile (~390): no
  horizontal scroll, columns stacked, pills wrap.

If something is off, edit the component or CSS, then measure and
screenshot the same states again at the panel size and at mobile.

## Viewport

- **Desktop / default:** leave the page at the current browser panel size.
  Do not call `Emulation.setDeviceMetricsOverride` (or any other resize)
  for 1280, 1440, or a “standard desktop.”
- **Mobile only:** set ~390×844 (`Emulation.setDeviceMetricsOverride` with
  `mobile: true`).
- After the mobile pass, `Emulation.clearDeviceMetricsOverride` so the
  page matches the panel again.

## Checks

- Do not use raw CDP click/type when the dedicated browser tools exist.
- Unlock the browser tab when the session’s browser work is done.
- Keep unit tests in `*.spec.ts` (`/frontend` → testing). This skill is
  the live browser pass plus visual review.
