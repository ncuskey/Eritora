# ROADMAP.md

> **Current Milestone**: v1.2 Site Refinement
> **Goal**: Clone the style and content from eritora.info (Obsidian Publish) to match functionality on eritora.wiki (MkDocs)

## Must-Haves
- [ ] All content from eritora.info migrated to eritora.wiki
- [ ] Visual style matches Obsidian Publish theme (dark/light)
- [ ] Wikilink syntax (`[[Page Name]]`) works correctly
- [ ] Navigation structure mirrors original site

## Nice-to-Haves
- [ ] Hover previews on links (like Obsidian Publish)
- [ ] Search functionality improved
- [ ] Mobile responsiveness enhancements

## Phases

### Phase 1: Content Crawl & Migration
**Status**: ✅ Complete
**Objective**: Crawl eritora.info to extract all markdown content and images.
**Deliverables**:
- Python script to crawl Obsidian Publish API
- All `.md` files extracted to `docs/`
- All images downloaded to `docs/assets/`

### Phase 2: Wikilink Support
**Status**: ⬜ Not Started
**Objective**: Configure MkDocs to handle `[[wikilinks]]` syntax.
**Deliverables**:
- Install/configure `mkdocs-roamlinks-plugin` or similar
- Convert wikilinks to standard markdown links if needed
- Verify all internal links work

### Phase 3: Theme Matching
**Status**: ⬜ Not Started
**Objective**: Make eritora.wiki visually identical to eritora.info.
**Deliverables**:
- Custom CSS in `docs/stylesheets/custom.css`
- Color palette matching (dark theme default)
- Typography and spacing adjustments
- Navigation structure matching

### Phase 4: Verification & Polish
**Status**: ⬜ Not Started
**Objective**: Ensure feature parity and deploy.
**Deliverables**:
- Side-by-side comparison verification
- Fix any broken links or missing content
- Deploy to production
