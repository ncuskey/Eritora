# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
A seamless, bidirectional knowledge bridge that keeps a community Discord server and a public Wiki in perfect sync. By treating a Git repository as the single source of truth, users can contribute via Discord messages or their local Obsidian app, with all changes automatically propagated to a beautiful, self-hosted MkDocs website.

## Goals
1.  **Self-Hosted Wiki**: Deploy a robust, high-performance Markdown wiki (MkDocs Material) on the user's VM, auto-building from a private GitHub repository.
2.  **Discord -> Wiki Sync**: Create a Discord bot that listens for specific commands or messages and transforms them into committed Markdown files in the repository.
3.  **Wiki -> Discord Sync**: Implement webhooks/actions that notify a Discord channel whenever the Wiki is updated (new pages or edits).
4.  **Obsidian Integration**: Establish a standard workflow using the "Obsidian Git" plugin to allow local, offline editing that seamlessly merges with the system.

## Non-Goals (Out of Scope)
-   Real-time collaborative editing (like Google Docs). Conflict resolution relies on Git's standard merge strategies.
-   Hosting the Wiki on Obsidian Publish (explicitly moving away from this).
-   Complex user authentication for the Wiki (it will be public read-only).

## Users
-   **Admins**: Manage the architecture and write long-form content via Obsidian.
-   **Discord Community**: Read the wiki and contribute "stubs" or suggestions directly from Discord channels.

## System Architecture ("The Invisible Git")
1.  **Storage**: Private GitHub Repository (Markdown files).
2.  **Frontend**: MkDocs (Material Theme) running on the VM, pulling from the repo.
3.  **Bridge**: Python/Node.js Bot running on the VM.
    -   *Inbound*: Accepts Discord content -> Commits to Git.
    -   *Outbound*: Watches Git hooks/polling -> Posts to Discord.
4.  **Editor**: Local Obsidian app + Obsidian Git plugin.

## Constraints
-   **Infrastructure**: Must run on the provided VM (Linux).
-   **Access**: SSH Keys provided for VM access.
-   **Format**: Discord Markdown and Obsidian Markdown have slight differences (e.g., links); the Bot must handle basic conversion.

## Success Criteria
-   [ ] **Wiki Deployment**: `eritora.info` (or new IP) serves the MkDocs site.
-   [ ] **Pipeline**: A change in the GitHub repo automatically rebuilds the site within <2 minutes.
-   [ ] **Bot Action**: `!wiki "Title" Content...` in Discord creates a file in the repo.
-   [ ] **Notification**: A push to the repo triggers a "New Wiki Update" message in Discord.
