---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Core Functional Verification

## Objective
Verify that the core interactive functions of the wiki—specifically the Redirect system and Search functionality—are operating correctly on the live site.

## Context
- `mkdocs.yml`: Contains a massive `redirect_maps` section.
- `site/`: The build output (on server).
- Goal: ensuring legacy URLs redirect to new locations and search returns results.

## Tasks

<task type="auto">
  <name>Verify Redirect Mapping</name>
  <files>scripts/verify_redirects.py</files>
  <action>
    Create a Python script that:
    1. Parses `mkdocs.yml` to extract the `plugins.redirects.redirect_maps` dictionary.
    2. For a sample (or all) of the redirects:
       - Construct the source URL (e.g., `https://eritora.wiki/OLD_PATH`).
       - Send a HTTP HEAD request.
       - Verify the status is 301 or 302.
       - Verify the `Location` header matches the expected target URL (normalized).
    3. Output a report of passed/failed redirects.
  </action>
  <verify>python scripts/verify_redirects.py --limit 50</verify>
  <done>Script confirms redirects are active and correct.</done>
</task>

<task type="auto">
  <name>Verify Search Index Availability</name>
  <files>scripts/verify_search.py</files>
  <action>
    Create a Python script that:
    1. Fetches `https://eritora.wiki/search/search_index.json`.
    2. Verifies the status is 200.
    3. Parses the JSON to ensure it contains a reasonable number of documents (> 100).
    4. Performs a sanity check: Ensure at least one known term (e.g., "Dragon") exists in the index.
  </action>
  <verify>python scripts/verify_search.py</verify>
  <done>Search index is confirmed present and populated.</done>
</task>

<task type="auto">
  <name>Verify Wikilink Rendering</name>
  <files>docs/functional_report.md</files>
  <action>
    The `ezlinks` plugin converts `[[link]]` to `<a>` tags.
    We need to verify this happens in the build.
    Create a simple check in `scripts/verify_search.py` (or separate) that:
    1. Fetches a page known to have wikilinks (e.g., specific monster page).
    2. Checks the HTML source to ensure no raw `[[` brackets remain and `href`s are formed.
    
    Synthesize all findings into `docs/functional_report.md`.
  </action>
  <verify>test -f docs/functional_report.md</verify>
  <done>Report confirms functional features.</done>
</task>

## Success Criteria
- [ ] Redirects are functioning (Legacy links don't dead-end).
- [ ] Search index is live and valid.
- [ ] Wikilinks are correctly processed into HTML anchors.
