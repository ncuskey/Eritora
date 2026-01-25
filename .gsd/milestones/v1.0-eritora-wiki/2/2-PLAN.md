---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: The Bridge (Discord Bot)

## Objective
Implement the "Sync Bot" that acts as the heartbeat of the system. It will poll for updates from GitHub (pushing them to the MkDocs site) and allow users to create new wiki stubs from Discord.

## Context
- .gsd/SPEC.md (Architecture: Bot as Bridge)
- .gsd/phases/2/RESEARCH.md (Polling Loop Architecture)

## Tasks

<task type="auto">
  <name>Bot Scaffold & Configuration</name>
  <files>bot/run.py, bot/config.py, .env.example, requirements.txt</files>
  <action>
    1. Update `requirements.txt` with `discord.py` and `GitPython`.
    2. Create `bot` directory.
    3. Create `bot/config.py` to load standard env vars (DISCORD_TOKEN, REPO_PATH, CHANNEL_ID).
    4. Create `bot/run.py` as the entry point with a basic `on_ready` event.
  </action>
  <verify>python3 bot/run.py --help (or check syntax)</verify>
  <done>Bot script exists and loads config without errors</done>
</task>

<task type="auto">
  <name>The Sync Loop (Pull & Build)</name>
  <files>bot/cogs/sync.py, bot/run.py</files>
  <action>
    Implement a cog `SyncCog` using `tasks.loop(minutes=1)`.
    Logic:
    1. `git remote update`
    2. Check if local hash != `origin/master`.
    3. If new:
       - `git pull --rebase`
       - `mkdocs build`
       - Send message to configured CHANNEL_ID: "🔄 **Wiki Updated!**\n[Commit Message]"
  </action>
  <verify>Manual verification (simulate git push)</verify>
  <done>Bot has a background task that checks git</done>
</task>

<task type="auto">
  <name>Inbound Commands (!wiki create)</name>
  <files>bot/cogs/wiki.py, bot/run.py</files>
  <action>
    Implement `WikiCog` with `!wiki create <filename> <content>` command.
    Logic:
    1. Clean filename (ensure .md extension, no weird chars).
    2. Write content to `docs/community/<filename>`.
    3. `git add`, `git commit`, `git push`.
    4. Reply: "✅ Created page: <url>"
  </action>
  <verify>None (Requires running bot)</verify>
  <done>Command exists in code</done>
</task>

## Success Criteria
- [ ] Bot connects to Discord
- [ ] Bot automatically pulls and rebuilds site when repo updates
- [ ] `!wiki create` commits file to GitHub
