# Domain Configuration

Domains define the organizational structure of the vault. Each domain has specific linking rules and priorities.

## Core Domains

### 0. System/
**Purpose:** Files (attachments), Templates, Home Dashboard

### 1. Inbox/
**Purpose:** Incoming notes, fleeting/literature/permanent, MOCs
**Linking:**
- Outgoing to other domains when organized
- Should reference MOCs for categorization

### 5. Projects/
**Purpose:** Active project documentation
**Linking:**
- Cross-links with Areas and Resources
- Outgoing to goals (alignment)

### 6. Areas/
**Purpose:** Life areas (goals, health, etc.)
**Linking:**
- Incoming from projects (related work)
- Cross-links with other areas

### 7. Resources/
**Purpose:** Reference material (editing, finance, etc.)
**Linking:**
- Incoming from all domains
- Knowledge base for projects and areas

### 8. Archives/
**Purpose:** Archived content, no longer active

## Link Priority Rules

When suggesting links, prioritize:

1. **Orphan → MOC** — Every note should belong to a Map of Content
2. **Note → Goal** — Ideas should align with goals
3. **Cross-domain** — Bridge related concepts across domains

## Custom Domains

Add custom domains by creating subdirectories and documenting them here:

```markdown
### your-domain/
**Purpose:** Description
**Linking:** Rules for incoming/outgoing links
```

## Entity Patterns

Common patterns to detect for auto-linking:

- `[[Note Name]]` — Existing wiki-links
- `@mention` — People/contacts (if contacts domain exists)
- `#tag` — Tags that may map to notes
- Project names — Match against projects/ directory
- Dates — Temporal context
