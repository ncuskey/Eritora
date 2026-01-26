---
phase: 4
plan: implement-redirects
---

# Fix Plan: Address Missing Segments (Redirects)

## Problem
- Users (and legacy links) expect "flat" URLs (e.g., `/St. Timothy's Cathedral/`) matching the old Obsidian Publish structure.
- Content is nested (e.g., `/3. Organizations/St. Timothy's Cathedral/`).
- Result: 403 Forbidden (Soft 404) on root URLs.

## Solution
Implement `mkdocs-redirects` to map filenames to their nested paths.

## Steps
1.  **Script**: Create `scripts/generate_redirect_map.py`.
    - Scans `docs/` for all `.md` files.
    - Generates a mapping: `Filename/`: `Path/To/Filename/`.
    - Handles duplicates (warns/skips).
2.  **Config**: Update `mkdocs.yml`:
    - Add `mkdocs-redirects` to plugins.
    - Include the generated map.
3.  **Install**: `pip install mkdocs-redirects`.
4.  **Deploy**: SCP updated config and install plugin on server.

## Verification
- `curl -I https://eritora.wiki/St.%20Timothy's%20Cathedral/` -> 301 Redirect -> 200 OK.
