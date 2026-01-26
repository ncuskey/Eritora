---
phase: 4
plan: fix-build
---

# Fix Plan: MkDocs Build & 403 Errors

## Problem
- Local build crashes due to `follow_path` in `ezlinks` config.
- Server build likely failing or producing incomplete site (missing `index.html` for directories).
- 403 Forbidden persists because `try_files` sends request to root `index.html` (which returns 200 status but wrong content) or fails if Nginx tries to autoindex directory.

## Solution
1. **Fix Config**: Remove `follow_path` from `mkdocs.yml`.
2. **Verify Local**: Ensure `mkdocs build` runs and generates `site/2. Geography/index.html`.
3. **Deploy**: SCP `mkdocs.yml` to server.
4. **Build Remote**: Run `mkdocs build` on server.
5. **Verify**: Check functionality of directory links.

## Verification
- `mkdocs build` (local) -> Success.
- `ls site/2. Geography/index.html` (local) -> Exists.
- `curl -I https://eritora.wiki/2.%20Geography/` -> 200 OK.
