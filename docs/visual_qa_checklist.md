# Visual QA Checklist

## Overview
Please perform a manual review of the [Eritora Wiki](https://eritora.wiki) (or local preview) to ensure visual parity with the expected design.

## 1. Typography & Fonts
- [ ] **Headers**: Inspect `h1` through `h6`. Are they rendering with the custom font (likely `Roboto` or `Cinzel` if fantasy-themed)?
- [ ] **Body Text**: Verify body text scaling is comfortable and matches the Slate theme defaults (or custom overrides).
- [ ] **Code Blocks**: Check that code snippets use a monospace font and have proper syntax highlighting colors (Slate scheme).

## 2. Color Palette (Slate Theme)
- [ ] **Background**: Should be dark grey/slate.
- [ ] **Primary Color**: Links and active elements should be the configured Primary color.
- [ ] **Accent Color**: Check accents on buttons or input fields.
- [ ] **Contrast**: Verify text is readable against the background.

## 3. UI Elements
- [ ] **Admonitions**: Check callout boxes (Note, Warning, Tip). Do they render with correct icons and colors?
- [ ] **Tables**: Verify tables have zebra striping (if enabled) and are readable.
- [ ] **Navigation**:
  - Desktop: Sidebar expands/collapses correctly.
  - Mobile: Hamburger menu works, drawer slides in smoothly.
- [ ] **Search Bar**: Typographic alignment in the search input and dropdown results.

## 4. Specific Issues to Watch
- [ ] **broken-images**: Ensure no "broken image" icons appear.
- [ ] **Overflow**: Check wide tables on mobile; they should scroll horizontally, not break layout.

## Sign-off
**Verified By**: __________________
**Date**: __________________
