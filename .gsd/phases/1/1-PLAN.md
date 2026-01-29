---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Automated Audit & Verification Setup

## Objective
Establish the tooling and baseline data for the "Audit & Gap Analysis" phase. This involves creating a comprehensive spider/crawler to identify technical issues (broken links, missing assets) and defining the manual verification criteria for visual/functional parity.

## Context
- .gsd/SPEC.md (Vision: Robust MkDocs deployment)
- scripts/validate_site.py (Existing simple validator)
- Target: https://eritora.wiki

## Tasks

<task type="auto">
  <name>Develop Comprehensive Audit Script</name>
  <files>scripts/audit_site.py</files>
  <action>
    Create a Python script using `requests` and `BeautifulSoup` (or similar) to:
    1. Start at a base URL (e.g., https://eritora.wiki or localhost).
    2. recursively crawl all internal links (spider).
    3. Validate HTTP status for every link (internal and external).
    4. Check for broken anchors (e.g., page.html#section).
    5. Validate existence of all referenced assets (images, css, js).
    6. Output a structured report (JSON or Markdown) of all failures.
    
    Refine/Replace `scripts/validate_site.py` with this more robust tool.
  </action>
  <verify>python scripts/audit_site.py --help</verify>
  <done>Script exists and handles crawling logic.</done>
</task>

<task type="auto">
  <name>Execute Audit & Generate Report</name>
  <files>docs/audit_report.md</files>
  <action>
    Run `scripts/audit_site.py` against `https://eritora.wiki` (and/or localhost).
    Capture the output and save it to `docs/audit_report.md`.
    Summarize the findings:
    - Total pages scanned
    - Number of broken links
    - specific high-priority errors
  </action>
  <verify>test -f docs/audit_report.md</verify>
  <done>Report file exists and contains audit data.</done>
</task>

<task type="auto">
  <name>Create Verification Matrix</name>
  <files>docs/verification_matrix.md</files>
  <action>
    Create a structured Markdown checklist for the "Functional Parity" and "Visual & UI Polish" phases.
    List all features to be verified, such as:
    - Search functionality
    - Mobile navigation responsiveness
    - Dark/Light mode toggle (if applicable)
    - Image rendering and lightboxes
    - Markdown rendering quirks (tables, callouts)
    - Discord integration points (if testable)
  </action>
  <verify>test -f docs/verification_matrix.md</verify>
  <done>Matrix exists with categories for Functional, Visual, and Content parity.</done>
</task>

## Success Criteria
- [ ] `scripts/audit_site.py` successfully finds broken links/assets.
- [ ] `docs/audit_report.md` provides a clear "To-Do" list for Phase 2 (Content Restoration).
- [ ] `docs/verification_matrix.md` establishes the standard for Phase 3 and 4.
