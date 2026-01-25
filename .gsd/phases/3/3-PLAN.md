---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Theme Matching

## Objective
Customize MkDocs Material theme to match the Obsidian Publish site's visual style.

## Source Analysis

### publish.css Key Elements

**Custom Font: Draconis**
- Fantasy-style font embedded as base64 woff2/woff
- Has normal, bold, and italic variants
- Gives site its distinctive TTRPG aesthetic

**Color Palette:**
```css
--accent: #863737          /* Deep red primary */
--dark-accent: #652121     /* Darker red */
--lite-accent: #e06c6c     /* Light red */
--h1: (header color)
--h2: sandybrown           /* #F4A460 */
--note: #1a1e24            /* Background */
--side-bar: #14181b        /* Sidebar */
--outer-bar: #0b0f13       /* Darkest */
```

## Tasks

<task type="auto">
  <name>Extract Draconis Font</name>
  <files>docs/assets/fonts/</files>
  <action>
    Create a script to extract the base64 font data from publish.css
    and save as .woff2 and .woff files.
  </action>
  <verify>ls -la docs/assets/fonts/</verify>
  <done>Font files extracted</done>
</task>

<task type="auto">
  <name>Create Custom CSS Theme</name>
  <files>docs/stylesheets/extra.css</files>
  <action>
    Override MkDocs Material CSS variables to match eritora.info theme:
    1. Custom font-face declarations for Draconis
    2. Color palette matching the burgundy/dark red scheme
    3. Header styling with sandybrown/red colors
    4. Dark background colors for slate theme
  </action>
  <verify>View extra.css and build</verify>
  <done>Custom CSS created</done>
</task>

<task type="auto">
  <name>Configure Material Theme</name>
  <files>mkdocs.yml</files>
  <action>
    Update theme configuration:
    1. Set slate color scheme for dark mode
    2. Configure primary/accent colors
    3. Disable palette toggle (single dark theme)
  </action>
  <verify>grep "palette" mkdocs.yml</verify>
  <done>Theme configured</done>
</task>

<task type="auto">
  <name>Verify Visual Match</name>
  <files>site/</files>
  <action>
    Run `mkdocs serve` and visually compare:
    1. Header styling
    2. Link colors
    3. Background colors
    4. Overall aesthetic
  </action>
  <verify>Screenshot comparison</verify>
  <done>Visual verification complete</done>
</task>

## Verification Plan

### Automated Tests
```bash
# 1. Build succeeds
mkdocs build

# 2. Custom CSS loaded
grep -l "Draconis" docs/stylesheets/extra.css

# 3. Font files exist
ls docs/assets/fonts/*.woff*
```

### Manual Verification
- Run `mkdocs serve -a 0.0.0.0:8000`
- Open http://localhost:8000
- Compare header colors to eritora.info
- Compare background colors
- Verify Draconis font loads

## Success Criteria
- [ ] Draconis font loads and displays
- [ ] Dark red accent color matches source
- [ ] Dark slate background matches source
- [ ] Headers styled with sandybrown
- [ ] Overall aesthetic feels consistent
