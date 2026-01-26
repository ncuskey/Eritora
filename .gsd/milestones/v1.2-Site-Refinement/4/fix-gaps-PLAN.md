---
phase: 4
plan: fix-gaps
wave: 1
gap_closure: true
---

# Fix Plan: 403s, Images, and Wikilinks

## Problem
1.  **403 Forbidden**: Navigation items point to directories without `index.md`, causing Nginx to block access.
2.  **Broken Image**: Acolyte page still shows broken image ref.
3.  **Wikilinks**: `[[links]]` not converting.

## Tasks

<task type="auto">
  <name>Fix 403 Forbidden (Directory Indices)</name>
  <files>docs/</files>
  <action>
    Create `index.md` for each main section directory (Geography, Organizations, etc.) that lists its children or provides a landing page.
    Script to recursively add `index.md` if missing.
  </action>
  <verify>Check `docs/2. Geography/index.md` exists</verify>
  <done>Index files created</done>
</task>

<task type="auto">
  <name>Fix Wikilinks Config</name>
  <files>mkdocs.yml</files>
  <action>
    Update `mkdocs.yml` to properly configure `ezlinks`:
    - Ensure `wikilinks` is enabled with correct extension settings.
    - Check if `follow_path: true` is needed.
  </action>
  <verify>Grep "ezlinks" mkdocs.yml</verify>
  <done>Configuration updated</done>
</task>

<task type="auto">
  <name>Double Check Acolyte Image</name>
  <files>docs/8. D&D 5e Rules and more!/Monsters/Acolyte (NPC) copy.md</files>
  <action>
    It seems there might be a duplicate file or the edit didn't take effectively. 
    Find the exact file causing the issue and remove the image link.
    Check for `Acolyte (NPC).md` vs `Acolyte (NPC) copy.md` (finding distinct file).
  </action>
  <verify>Grep "Pasted image" in Acolyte files</verify>
  <done>Image link removed</done>
</task>

<task type="auto">
  <name>Deploy Fixes</name>
  <files>scripts/ops/</files>
  <action>
    Push changes and rebuild on server.
  </action>
  <verify>curl -I https://eritora.wiki</verify>
  <done>Deployed</done>
</task>
