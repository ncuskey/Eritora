---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: Visual Asset Audit & QA

## Objective
Ensure all custom styling assets are present, valid, and correctly configured to strictly match the original site's visual design.

## Context
- `mkdocs.yml` defines `extra_css`.
- Custom CSS files: `docs/publish.css`, `docs/stylesheets/extra.css`.
- "Pixel-perfect" requirement means we need to catch missing assets (fonts, images referenced in CSS) and ensure no broken styles.

## Tasks

<task type="auto">
  <name>Audit Custom CSS & Assets</name>
  <files>scripts/audit_assets.py</files>
  <action>
    Create a Python script that:
    1. Parses `mkdocs.yml` to find `extra_css` and `extra_javascript`.
    2. Verifies these files exist on disk.
    3. Scans these CSS files for `url(...)` references (images, fonts).
    4. Verifies that all local referenced assets exist.
    5. Checks for external links in CSS (e.g. Google Fonts) and verifies they are reachable.
  </action>
  <verify>python scripts/audit_assets.py</verify>
  <done>Asset integrity confirmed.</done>
</task>

<task type="auto">
  <name>Generate Visual QA Checklist</name>
  <files>docs/visual_qa_checklist.md</files>
  <action>
    Create a rigorous manual checklist for the user to perform the final visual sign-off.
    Sections:
    - Font Rendering (Headers vs Body)
    - Color Palette (Primary/Accent correctness)
    - Mobile Responsiveness (Menu behavior, Table scrolling)
    - Admonition/Callout Styling
    - Table Styling
  </action>
  <verify>test -f docs/visual_qa_checklist.md</verify>
  <done>Checklist created for user sign-off.</done>
</task>

## Success Criteria
- [ ] All custom CSS/JS files defined in config exist.
- [ ] All assets referenced within CSS (images, fonts) exist.
- [ ] A comprehensive Manual QA checklist is generated for the user.
