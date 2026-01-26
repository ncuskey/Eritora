# Debug Session: 403 Forbidden

## Context
- User reports 403 errors on directory URLs.
- Initial Fix (`try_files`) failed initially.
- SSL Enabled.

## Root Cause
- **Build Failure**: `mkdocs build` crashed locally and likely on server due to unsupported `follow_path: true` option in `ezlinks` plugin.
- **Missing Files**: `site/2. Geography/index.html` was missing.
- **Nginx**: `try_files` couldn't find index file, fell back to autoindex (forbidden).

## Resolution
1. **Config**: Removed `follow_path` from `mkdocs.yml`.
2. **Rebuild**: Triggered successful build on server. `index.html` files generated.
3. **Nginx**: `try_files` logic now finds the files.
4. **Permissions**: `chown` confirmed.

## Verification
- `curl -I https://eritora.wiki/2.%20Geography/` -> 200 OK.
- `curl -I https://eritora.wiki/1.%20Adventurer's%20Hub/` -> 200 OK.
