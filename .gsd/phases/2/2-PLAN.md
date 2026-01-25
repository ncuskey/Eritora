---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Wikilink Support

## Objective
Configure MkDocs to handle Obsidian-style `[[wikilinks]]` and `![[embeds]]` so that internal links work correctly on the built site.

## Context
- Content uses `[[Page Name]]` syntax (1000+ wikilinks across 960 files)
- Also uses `![[image.png]]` for image embeds
- MkDocs Material doesn't support wikilinks natively

## Approach
Use `mkdocs-roamlinks-plugin` which:
- Converts `[[Page Name]]` → `[Page Name](Page%20Name.md)`
- Handles partial path matching
- Supports image embeds

## Tasks

<task type="auto">
  <name>Install Roamlinks Plugin</name>
  <files>requirements.txt</files>
  <action>
    Add `mkdocs-roamlinks-plugin` to requirements.txt and install:
    ```bash
    echo "mkdocs-roamlinks-plugin" >> requirements.txt
    pip install mkdocs-roamlinks-plugin
    ```
  </action>
  <verify>pip show mkdocs-roamlinks-plugin</verify>
  <done>Plugin installed</done>
</task>

<task type="auto">
  <name>Configure Plugin in mkdocs.yml</name>
  <files>mkdocs.yml</files>
  <action>
    Add roamlinks to the plugins section:
    ```yaml
    plugins:
      - search
      - roamlinks
    ```
  </action>
  <verify>grep "roamlinks" mkdocs.yml</verify>
  <done>Plugin configured</done>
</task>

<task type="auto">
  <name>Test Wikilink Conversion</name>
  <files>docs/</files>
  <action>
    Run `mkdocs build` and verify:
    1. No build errors
    2. Sample page with wikilinks renders correctly
    3. Links are clickable in browser
  </action>
  <verify>mkdocs build && grep -r "href=" site/Welcome\ to\ Eritora/index.html | head -5</verify>
  <done>Wikilinks converted and working</done>
</task>

<task type="auto">
  <name>Fix Image Embeds</name>
  <files>docs/, mkdocs.yml</files>
  <action>
    If `![[image.png]]` embeds don't work:
    1. Check if plugin handles embeds
    2. Consider post-processing script to convert `![[x]]` → `![x](Images/x)`
    3. Or configure additional plugin
  </action>
  <verify>Check site for rendered images</verify>
  <done>Images display correctly</done>
</task>

## Verification Plan

### Automated Tests
```bash
# 1. Build succeeds
mkdocs build

# 2. Check converted links exist
grep -r "href=" site/Welcome\ to\ Eritora/index.html

# 3. Run local server and spot check
mkdocs serve -a 0.0.0.0:8000
```

### Manual Verification
- Open http://localhost:8000
- Navigate to "Welcome to Eritora" page
- Click a wikilink (e.g., [[Eritora]]) and verify it navigates correctly
- Check that images display

## Success Criteria
- [ ] `mkdocs build` succeeds
- [ ] `[[wikilinks]]` convert to working `<a href="...">` tags
- [ ] `![[images]]` render as `<img>` tags
- [ ] No dead links on sample pages
