# Milestone: v1.0 Eritora Wiki

## Completed: 2026-01-25

## Goal
Build a self-hosted wiki system for the Eritora TTRPG that syncs between local Obsidian editing, Discord community input, and a public MkDocs website.

## Deliverables
- ✅ MkDocs-powered wiki with Material theme
- ✅ Discord Bot for sync and page creation
- ✅ Obsidian Git workflow documentation
- ✅ Production deployment on DigitalOcean with SSL

## Phases Completed
1. **Phase 1: Foundation & Infrastructure** — Git repo, MkDocs bootstrap, VM setup script
2. **Phase 2: The Bridge (Discord Bot)** — Bot scaffold, sync loop, `!wiki create` command
3. **Phase 3: Integration & Polish** — User guides, theme customization, deployment docs
4. **Phase 4: Production Deployment** — Nginx config, SSL via Certbot, DNS setup

## Verification
- ✅ https://eritora.wiki loads with valid SSL
- ✅ Discord bot running on DigitalOcean VM
- ✅ Sync loop active (pulls from GitHub every minute)

## Architecture
```
[Obsidian] --push--> [GitHub] <--pull-- [VM Bot] --build--> [MkDocs Site]
                           ^
                           |
                      [Discord Bot]
                      (!wiki create)
```

## Key Files
- `bot/run.py` — Bot entry point
- `bot/cogs/sync.py` — Sync loop logic
- `bot/cogs/wiki.py` — Discord commands
- `scripts/ops/setup_nginx.sh` — Production deployment
- `mkdocs.yml` — Site configuration
