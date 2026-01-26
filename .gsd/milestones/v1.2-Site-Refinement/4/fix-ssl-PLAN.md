---
phase: 4
plan: fix-ssl
---

# Fix Plan: SSL Certificate

## Problem
`net::ERR_CERT_COMMON_NAME_INVALID` indicates invalid SSL certificate.

## Steps
1.  **Generate Certificate**: Run `certbot --nginx`.
    - Domains: `eritora.wiki`, `www.eritora.wiki`
    - Email: `nickcuskey@gmail.com` (assumed based on context, or use `--register-unsafely-without-email`)
2.  **Reload Nginx**: Ensure changes take effect.
3.  **Verify**: `curl -I https://eritora.wiki` should return 200 without SSL error.
