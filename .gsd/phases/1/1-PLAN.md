---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Content Crawl & Migration

## Objective
Crawl all content from eritora.info (Obsidian Publish) and migrate to the local MkDocs site.

## Context
- Source: Obsidian Publish site at `publish-01.obsidian.md`
- UID: `70dcd6fa444bebdb92e475a6b545b707`
- Files: ~250+ markdown files, ~30 images
- API:
  - Cache manifest: `https://publish-01.obsidian.md/cache/{uid}`
  - File content: `https://publish-01.obsidian.md/access/{uid}/{path}`

## Tasks

<task type="auto">
  <name>Create Crawler Script</name>
  <files>scripts/tools/crawl_obsidian.py</files>
  <action>
    Create Python script that:
    1. Fetches cache manifest JSON
    2. Parses file list (markdown files + images)
    3. Downloads each file to `docs/` preserving folder structure
    4. Handles URL encoding for special characters
    5. Reports progress and any errors
  </action>
  <verify>python3 scripts/tools/crawl_obsidian.py --help</verify>
  <done>Script created and executable</done>
</task>

<task type="auto">
  <name>Run Crawler</name>
  <files>docs/</files>
  <action>
    Execute crawler to download all content:
    ```bash
    python3 scripts/tools/crawl_obsidian.py \
      --uid 70dcd6fa444bebdb92e475a6b545b707 \
      --output docs/
    ```
  </action>
  <verify>find docs -name "*.md" | wc -l</verify>
  <done>All content downloaded</done>
</task>

<task type="auto">
  <name>Verify Content</name>
  <files>docs/</files>
  <action>
    1. Count files and compare to source
    2. Spot check key files (Welcome to Eritora, Turnbuckle Town)
    3. Verify images downloaded
    4. Run `mkdocs build` to check for major errors
  </action>
  <verify>mkdocs build && ls -la site/</verify>
  <done>Content verified, site builds</done>
</task>

## Success Criteria
- [ ] All markdown files from eritora.info exist in `docs/`
- [ ] All images exist in `docs/assets/` or `docs/Images/`
- [ ] `mkdocs build` succeeds (warnings OK, no errors)
