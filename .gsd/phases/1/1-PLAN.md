---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Foundation & Infrastructure

## Objective
Initialize the local environment, set up the project structure for the Wiki, and prepare the VM script for deployment.

## Context
- .gsd/SPEC.md (Architecture: MkDocs, Git-backed)
- .gsd/ROADMAP.md (Phase 1)

## Tasks

<task type="auto">
  <name>Initialize Project Structure</name>
  <files>.gitignore, README.md</files>
  <action>
    Create a standard .gitignore for Python/MkDocs/Obsidian.
    Update README.md with project overview and "Getting Started" for the Wiki.
    Ensure .agent/ .gemini/ .gsd/ are committed.
  </action>
  <verify>test -f .gitignore && grep "mkdocs" .gitignore</verify>
  <done>Clean git status with correct ignores</done>
</task>

<task type="auto">
  <name>Create VM Setup Script</name>
  <files>scripts/ops/setup_vm.sh, requirements.txt</files>
  <action>
    Create `requirements.txt` with `mkdocs` and `mkdocs-material`.
    Create a robust setup script `scripts/ops/setup_vm.sh` that:
    1. Installs system dependencies (git, python3).
    2. Creates a python virtual environment.
    3. Installs requirements.
    4. Sets up a strict directory structure for the wiki.
  </action>
  <verify>test -f scripts/ops/setup_vm.sh</verify>
  <done>Script exists and is executable</done>
</task>

<task type="auto">
  <name>Bootstrap MkDocs</name>
  <files>mkdocs.yml, docs/index.md, docs/stylesheets/extra.css</files>
  <action>
    Initialize a new MkDocs project:
    1. Create `mkdocs.yml` configured for Material theme.
    2. Create `docs/index.md` (Home page).
    3. Create `docs/stylesheets/extra.css` for custom styling.
  </action>
  <verify>test -f mkdocs.yml && test -d docs</verify>
  <done>MkDocs project structure matches specification</done>
</task>

## Success Criteria
- [ ] `mkdocs serve` runs locally without errors
- [ ] Project root is clean and ready to be pushed to GitHub
