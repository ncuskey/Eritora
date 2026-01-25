## Phase 4 Verification

### Must-Haves
- [x] **Nginx Config**: `scripts/ops/nginx.conf` created with correct domain (`eritora.wiki`).
- [x] **Setup Script**: `scripts/ops/setup_nginx.sh` handles Apt install, config linking, and Certbot.
- [x] **App Config**: `mkdocs.yml` updated to `https://eritora.wiki`.
- [x] **Documentation**: `docs/guides/deployment.md` updated with DNS instructions.

### Verdict: PASS

The system is ready for production deployment.
**Next Steps**:
1. User configures DNS at Namecheap.
2. User runs `git pull` and `sudo ./scripts/ops/setup_nginx.sh` on VM.
