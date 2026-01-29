---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Content Reconciliation & Integrity

## Objective
Ensure that every source Markdown file in the repository is correctly built and served by the site (no "orphaned" content), and valid static analysis of all source links/assets to catch issues in unlinked pages.

## Context
- `docs/` contains the source of truth Markdown files.
- `site/sitemap.xml` (or `https://eritora.wiki/sitemap.xml`) contains the built pages.
- Goal: `Source Files` ⊆ `Built Pages`.

## Tasks

<task type="auto">
  <name>Develop Reconciliation Script</name>
  <files>scripts/reconcile_content.py</files>
  <action>
    Create a Python script to:
    1. Scan `docs/` recursively for all `.md` files (ignoring files starting with `.` or `_` if needed).
    2. Convert file paths to expected URLs (slugification logic matching MkDocs).
    3. Fetch `https://eritora.wiki/sitemap.xml` and parse all `<loc>` URLs.
    4. Compare sets: Identify Source files NOT present in Sitemap (Orphans).
    5. Output `docs/orphaned_content.md` listing any missing pages.
  </action>
  <verify>python scripts/reconcile_content.py --help</verify>
  <done>Script exists and runs.</done>
</task>

<task type="auto">
  <name>Develop Static Source Validator</name>
  <files>scripts/validate_source.py</files>
  <action>
    Create a Python script to:
    1. Parse every `.md` file in `docs/`.
    2. Extract all `[link](path)` and `![image](path)` references.
    3. Resolve relative paths against the file system.
    4. Verify the target file exists.
    5. Report "Dead Links" where the source Markdown points to a non-existent file/image (even if not deployed).
    6. Output `docs/source_integrity_report.md`.
  </action>
  <verify>python scripts/validate_source.py --help</verify>
  <done>Script exists and identifies filesystem-level broken links.</done>
</task>

<task type="auto">
  <name>Execute Reconciliation & Integrity Checks</name>
  <files>docs/content_gap_report.md</files>
  <action>
    Run both scripts:
    1. `scripts/reconcile_content.py > docs/orphaned_content.md`
    2. `scripts/validate_source.py > docs/source_integrity_report.md`
    
    Synthesize findings into `docs/content_gap_report.md`:
    - Count of defined source pages vs built pages.
    - List of orphans to be restored (or deleted if obsolete).
    - List of source-level broken links to be fixed.
  </action>
  <verify>test -f docs/content_gap_report.md</verify>
  <done>Gap report generated.</done>
</task>

## Success Criteria
- [ ] All source files are accounted for (either in sitemap or legitimately excluded).
- [ ] No internal broken file references in the source Markdown.
- [ ] Clear list of action items for restoring missing content.
