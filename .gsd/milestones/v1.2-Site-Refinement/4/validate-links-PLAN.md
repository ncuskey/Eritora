---
phase: 4
plan: validate-links
---

# Validation Plan: Systematic Link Checking

## Problem
- User reports broken links (`adventuring-academy`).
- Potential case sensitivity or missing content.

## Solution
1.  **Crawler**: Script (`scripts/validate_site.py`) to crawl `sitemap.xml` and detect Soft 404s.
2.  **Redirects V2**: Update `generate_redirects.py` to support:
    - Lowercase variants (if relevant).
    - Slugified variants.

## Verification
- Scan site.
- Report valid vs invalid.
