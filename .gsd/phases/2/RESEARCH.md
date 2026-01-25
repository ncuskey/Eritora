# Research: Phase 2 (The Bridge)

## Objective
Determine the most robust architecture for a Discord Bot that:
1.  Syncs the Wiki (Git Pull + MkDocs Build).
2.  Notifies Discord of changes.
3.  Allows creating pages from Discord.

## Options Analysis

### 1. Sync Mechanism (Obsidian -> Wiki)
| Option | Pros | Cons |
|--------|------|------|
| **Webhook Listener** | Instant updates | Requires public IP, open ports, configuring GitHub Webhooks |
| **Polling Loop** | Works behind firewalls, simple | Delay (e.g. 1 min), "wasted" checks |
| **Cron Job** | Decoupled from Bot | Harder to notify Bot of changes |

**Decision**: **Polling Loop (Background Task)** inside the Bot using `discord.ext.tasks`.
-   The Bot effectively becomes the "System Manager".
-   Every ~60s:
    -   `git remote update`
    -   Check if `LOCAL != REMOTE`
    -   If changed: `git pull`, `mkdocs build`, send msg to `#wiki-updates`.

### 2. Discord Interaction
-   **Library**: `discord.py` (Standard, mature, good asyncio support).
-   **Commands**: Usage of `discord.app_commands` (Slash Commands) is modern, but standard `!wiki` prefix commands are easier for quick text processing.
-   **Formatting**: Discord message content comes as string. Needs to be cleaned (remove emojis? smart quotes?) before saving as `.md`.

### 3. Git Operations
-   **Library**: `GitPython` vs `subprocess`.
-   **Decision**: `GitPython` is cleaner for object interaction vs parsing stdout.

## Architecture Specification
-   **Language**: Python 3.11+
-   **Dependencies**: `discord.py`, `GitPython`, `python-dotenv`.
-   **File Structure**:
    -   `bot/main.py`: Entry point & loop.
    -   `bot/cogs/wiki.py`: Commands (!wiki create).
    -   `bot/cogs/sync.py`: Background loop (Pull/Build/Notify).

## Risks
-   **Merge Conflicts**: If Bot commits while Obsidian User pushed, `git pull` might fail.
-   **Mitigation**: `git pull --rebase --autostash`. If conflict remains, Bot logs error and alerts Admin channel. (Keep it simple for v1).
