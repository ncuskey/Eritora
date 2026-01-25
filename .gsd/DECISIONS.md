# DECISIONS.md

## ADR-001: Git-Backed Architecture
*Date: 2026-01-25*

**Context**: User wants bidirectional sync between Obsidian (Local), Discord (Community), and a Web Wiki. Obsidian Publish is read-only for bots.
**Decision**: Use a centralized Git repository as the database.
- **Frontend**: MkDocs (Static Site Generator) running on VM.
- **Backend / Sync**: Discord Bot commits to/reads from Git.
- **Editor**: Obsidian uses "Obsidian Git" plugin.
**Consequences**:
- Complex merge conflicts possible (mitigated by git).
- Requires VM configuration (cost/maintenance).
- Highly portable and strictly version controlled.
