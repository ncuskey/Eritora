---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: Verification & Polish

## Objective
Final verification of the migrated site, fix any issues, and deploy to production.

## Context
Previous phases completed:
- ✅ Phase 1: Content crawled (960 markdown files, 25 images)
- ✅ Phase 2: Wikilinks working (ezlinks plugin)
- ✅ Phase 3: Theme matching (Draconis font, burgundy palette)

Now need to:
1. Verify content integrity
2. Check for broken links
3. Deploy updated site to production

## Tasks

<task type="auto">
  <name>Update Navigation</name>
  <files>mkdocs.yml</files>
  <action>
    Update nav structure to include crawled content:
    - Add main sections from Obsidian structure
    - Use folder-based navigation
    - Set Welcome to Eritora as home
  </action>
  <verify>grep "nav:" mkdocs.yml</verify>
  <done>Navigation updated</done>
</task>

<task type="auto">
  <name>Fix Missing Logo</name>
  <files>docs/assets/logo.png</files>
  <action>
    Check if logo exists, if not, use one from Images folder:
    ```bash
    ls docs/assets/logo.png || cp docs/Images/logo.png docs/assets/
    ```
  </action>
  <verify>ls docs/assets/logo.png</verify>
  <done>Logo in place</done>
</task>

<task type="auto">
  <name>Check for Broken Links</name>
  <files>site/</files>
  <action>
    Build and check for link errors:
    ```bash
    mkdocs build 2>&1 | grep -i "unrecognized\|error\|warning"
    ```
    Review and fix critical issues.
  </action>
  <verify>Build output review</verify>
  <done>Link issues catalogued</done>
</task>

<task type="auto">
  <name>Deploy to Production</name>
  <files>scripts/ops/</files>
  <action>
    Trigger production deployment:
    1. Push changes to GitHub
    2. SSH to server and pull latest
    3. Rebuild site on server
    4. Verify at https://eritora.wiki
  </action>
  <verify>curl -I https://eritora.wiki</verify>
  <done>Site deployed and accessible</done>
</task>

<task type="user">
  <name>Visual Verification</name>
  <files>N/A</files>
  <action>
    User to compare:
    1. Open eritora.info (original)
    2. Open eritora.wiki (new)
    3. Verify content, links, and styling
  </action>
  <verify>User approval</verify>
  <done>User confirms site matches</done>
</task>

## Verification Plan

### Automated Tests
```bash
# 1. Build succeeds
mkdocs build

# 2. Check link warnings (informational)
mkdocs build 2>&1 | grep -c "unrecognized"

# 3. Verify key files exist
ls docs/Welcome\ to\ Eritora.md
ls docs/assets/logo.png
ls docs/Images/*.png | head -5

# 4. Check production site
curl -I https://eritora.wiki
```

### Manual Verification (User)
1. Visit https://eritora.wiki
2. Click on "Welcome to Eritora" page
3. Verify Draconis font displays on headers
4. Verify burgundy color theme
5. Click several wikilinks to confirm navigation
6. Compare with https://eritora.info for visual parity

## Success Criteria
- [ ] `mkdocs build` succeeds
- [ ] Logo displays correctly
- [ ] Navigation includes main content sections
- [ ] Site deployed to production
- [ ] User confirms visual parity with source
