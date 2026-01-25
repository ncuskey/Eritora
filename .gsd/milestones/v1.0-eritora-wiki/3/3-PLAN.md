---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Integration & Polish

## Objective
Finalize the user experience by providing clear documentation for the Obsidian workflow, polishing the Wiki's visual appearance, and documenting the VM deployment process.

## Context
- .gsd/SPEC.md (Obsidian Git workflow)
- mkdocs.yml (Theme configuration)

## Tasks

<task type="auto">
  <name>Create User Guides</name>
  <files>docs/guides/obsidian-setup.md, docs/guides/deployment.md</files>
  <action>
    1. Create `docs/guides/obsidian-setup.md`: Step-by-step guide for installing "Obsidian Git", configuring it for mobile/desktop, and conflict resolution basics.
    2. Create `docs/guides/deployment.md`: Detailed "Runbook" for the VM (pull, setup, restart bot).
    3. Link these in `mkdocs.yml` navigation.
  </action>
  <verify>test -f docs/guides/obsidian-setup.md</verify>
  <done>Guides exist and are linked in nav</done>
</task>

<task type="auto">
  <name>Polish Wiki Theme</name>
  <files>mkdocs.yml, docs/assets/logo.png</files>
  <action>
    1. Update `mkdocs.yml` to enable:
       - Social cards
       - Edit button (link to GitHub)
       - Footer
    2. Create `docs/assets` directory.
    3. Generate/Copy a placeholder logo.
  </action>
  <verify>mkdocs build</verify>
  <done>Wiki builds with new theme settings</done>
</task>

## Success Criteria
- [ ] Documentation explains how to contribute from Obsidian
- [ ] Wiki looks professional (not default theme settings)
