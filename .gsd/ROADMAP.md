# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0 - The Living Wiki

## Must-Haves (from SPEC)
- [ ] Validated MkDocs deployment on VM
- [ ] Working Discord Bot that can commit files
- [ ] Working Discord Bot that notifies on changes
- [ ] Documented Obsidian Git setup for user

## Phases

### Phase 1: Foundation & Infrastructure
**Status**: ✅ Complete
**Objective**: Establish the "Source of Truth" repo and get the minimal Wiki running on the VM.
**Deliverables**:
- Private GitHub Repository created
- VM configured with SSH and dependencies (Python, Git)
- MkDocs installed and serving a default "Hello World" site from the repo
- Domain `eritora.info` (or temp IP) pointing to the VM

### Phase 2: The Bridge (Discord Bot)
**Status**: ✅ Complete
**Objective**: Build the Discord integration that reads/writes to the repo.
**Deliverables**:
- Python/Node Bot running on VM
- Command `!wiki create <title> <body>` commits to repo
- Git Hook/Poller that detects new commits and posts to `#wiki-updates`
- Basic Markdown cleaning (Discord -> Obsidian format)

### Phase 3: The Editor & Polish
**Status**: ✅ Complete
**Objective**: Connect the local Obsidian experience and refine the Wiki look.
**Deliverables**:
- "Obsidian Git" setup guide validated
- MkDocs "Material" theme configuration (colors, logo, layout)
- Automatic site rebuild on git push (Webhook or Cron)
- Final end-to-end sync verification
