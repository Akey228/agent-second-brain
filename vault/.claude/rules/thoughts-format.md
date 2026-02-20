---
paths: "vault/*.md"
---

# Note Format

Rules for all notes in vault/ root.

## Location

ALL notes go to `vault/` root. NO subfolders like thoughts/, ideas/, etc.

```
vault/Название заметки на русском.md
```

## File Naming

- Filename: RUSSIAN title with SPACES (NOT hyphens, NOT English, NOT slug)
- NO date in filename
- NO slug format, NO lowercase-hyphens

Examples:
```
vault/Модель ценообразования SaaS.md
vault/Акустический поролон для записи звука.md
vault/Здоровый образ жизни решает большинство проблем.md
```

FORBIDDEN:
- `thoughts/ideas/slug.md` — old format, DO NOT use
- `2026-02-16-slug.md` — no dates in filenames
- `single-tasking-focus.md` — no English slugs

## Frontmatter (MANDATORY)

```yaml
---
Created: "YYYY-MM-DDTHH:MM"
References:
Tags:
Links:
---
```

### Field Rules

| Field | Required | Format | Notes |
|-------|----------|--------|-------|
| Created | YES | `"YYYY-MM-DDTHH:MM"` | In quotes, T-separator |
| References | NO | text | Source reference |
| Tags | NO | text | Relevant tags |
| Links | NO | text | Related notes |

## Content Structure

After frontmatter — text immediately. NO heading.

```markdown
---
Created: "2026-02-20T15:00"
References:
Tags:
Links:
---
Текст заметки начинается сразу здесь. Без заголовка.

#### Linked References to "Название заметки"
```dataview
list from [[Название заметки]]
```
```

CRITICAL:
- Text goes BETWEEN frontmatter and Linked References block
- `#### Linked References to "Title"` is ALWAYS at the END
- `list from [[...]]` MUST be inside ```dataview code block
- NO `# Title` after frontmatter

## Note Content Rules

- Text from voice messages goes into notes almost AS-IS with MINIMAL editing
- Allowed edits: remove word repetitions, replace some words with better fits
- FORBIDDEN: adding headers, bullet points, lists, conclusions, structure, summaries, analysis

## Wiki-Links

When saving a note:

1. **Search for related notes** in vault/
2. **Link to relevant existing notes** — do NOT create new notes without permission
3. **Add backlinks** via Links field if applicable
