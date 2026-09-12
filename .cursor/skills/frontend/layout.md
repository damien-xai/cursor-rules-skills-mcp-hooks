# Layout, density, and alignment

Follow `.cursor/rules/ui-design.mdc`. This file is the CSS recipe. Do not
build a marketing/hero page for an app chrome.

## Page shell

Pin the app to the **top** of the viewport. Do not vertically center the
page. Do not use `min-height: 100vh` + `justify-content: center` for the
main column.

```css
:global(html),
:global(body) {
	margin: 0;
	min-height: 100dvh;
	box-sizing: border-box;
}

:global(*),
:global(*::before),
:global(*::after) {
	box-sizing: border-box;
}

.shell {
	width: min(100%, 40rem);
	margin-inline: auto;
	padding: 1rem 1rem 2rem;
}
```

- Equal left/right gutters. Never `width: 100vw` (horizontal scroll).
- One shared left edge for title, forms, and lists.
- A list/detail app stays in a ~40rem column. Do not stretch inputs across
  a 1280px window.

## Compact density (default)

| Token        | Value                                      |
| ------------ | ------------------------------------------ |
| Body type    | 14–15px, `letter-spacing: normal`          |
| Page title   | 1.25rem (20px), font-weight 650            |
| Meta / hint  | 12–13px                                    |
| Control h    | 2rem (32px). Hard cap 2.25rem (36px)       |
| Control pad  | 0 0.625rem                                 |
| Card pad     | 0.75rem                                    |
| Stack gap    | 0.5–0.75rem                                |
| List row pad | 0.5rem 0                                   |
| Radius       | 6px controls, 999px pills only             |

Do not use 48px inputs, 2rem card padding, or a 2rem+ page title unless the
user asks for a marketing layout.

```css
input,
select,
button,
textarea {
	height: 2rem;
	padding: 0 0.625rem;
	font: inherit;
	font-size: 0.875rem;
	line-height: 1.2;
	border-radius: 6px;
}

textarea {
	height: auto;
	min-height: 4rem;
	padding: 0.5rem 0.625rem;
}
```

On mobile, keep the **visual** control at 32–36px. Grow the row, not the
widget, if you need a larger hit area.

## Alignment

- Forms: CSS grid. Each label sits in the same column as its control.
  Controls in one row share `height` and `align-items: center`.
- Toolbar rows (filters + count): `display: flex; align-items: center;
  gap: 0.5rem; flex-wrap: wrap`.
- List rows: checkbox/icon, title, and meta on one baseline. Secondary
  fields wrap under the title, still indented to the title column.
- No leftover unused selectors. If a class is unused, delete it.

## Responsive

Use a single breakpoint (~40rem). Do not invent a breakpoint per component.

```css
.form {
	display: grid;
	grid-template-columns: 1fr 8.5rem 7rem;
	gap: 0.5rem 0.75rem;
	align-items: end;
}

@media (max-width: 40rem) {
	.form {
		grid-template-columns: 1fr;
	}
}
```

- Below 40rem: one column. Filter chips wrap. Item meta stacks under the
  title. No horizontal scroll.
- `minmax(0, 1fr)` on flexible columns so long text cannot blow the grid.

## Typography (do not break words)

- `letter-spacing: normal` and `word-spacing: normal` on all UI text.
- Do not track-out headings. Do not use `word-break: break-all`.
- `overflow-wrap: anywhere` only on user-provided strings that can be one
  long token (URLs, titles). Labels and chrome stay `normal`.

## Anti-patterns (this is a fail)

- Vertically centering the whole app in the window
- Full-bleed form fields on a wide desktop
- `padding: 2rem` / `gap: 1.5rem` on cards and toolbars
- Control height ≥ 40px
- Emoji, or a second icon set
