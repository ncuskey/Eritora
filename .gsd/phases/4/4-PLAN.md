---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: Production Deployment

## Objective
Configure the system for production usage on `eritora.wiki`. This involves setting up Nginx as a reverse proxy/static file server, configuring SSL with Let's Encrypt, and updating the application configuration.

## Context
- .gsd/ROADMAP.md (Phase 4)
- scripts/ops/setup_vm.sh

## Tasks

<task type="auto">
  <name>Configure Nginx & SSL Scripts</name>
  <files>scripts/ops/setup_nginx.sh, scripts/ops/nginx.conf</files>
  <action>
    1. Create `scripts/ops/nginx.conf`: Standard Nginx server block for serving static files from `/var/www/wiki/site`.
    2. Create `scripts/ops/setup_nginx.sh`:
       - Installs Nginx and Certbot (`python3-certbot-nginx`).
       - Links the config file to `/etc/nginx/sites-enabled`.
       - Runs `certbot` to obtain SSL certificates.
  </action>
  <verify>test -f scripts/ops/nginx.conf && test -x scripts/ops/setup_nginx.sh</verify>
  <done>Scripts ready for production</done>
</task>

<task type="auto">
  <name>Update Application Config</name>
  <files>mkdocs.yml</files>
  <action>
    Update `site_url` in `mkdocs.yml` to `https://eritora.wiki`.
  </action>
  <verify>grep "eritora.wiki" mkdocs.yml</verify>
  <done>Config points to new domain</done>
</task>

<task type="auto">
  <name>Update Deployment Guide</name>
  <files>docs/guides/deployment.md</files>
  <action>
    Add a "Domain & SSL" section to the deployment guide explains:
    1. DNS A Record setup (Namecheap).
    2. Running the new `setup_nginx.sh` script.
    3. Verifying HTTPS.
  </action>
  <verify>grep "DNS" docs/guides/deployment.md</verify>
  <done>Guide covers production setup</done>
</task>

## Success Criteria
- [ ] User can follow guide to get green lock on `eritora.wiki`
