---
paths: "thoughts/**/*.md"
---

# Thoughts Format

Rules for notes in `thoughts/` folder and its subfolders.

## Folder Structure

```
thoughts/
├── ideas/       # Creative ideas, concepts
├── reflections/ # Personal reflections, lessons
├── projects/    # Project-related notes
└── learnings/   # Knowledge, discoveries
```

## File Naming

- Format: `slug.md` (БЕЗ даты в имени файла)
- Slug: lowercase, через дефис
- Первая буква slug — строчная (заглавная только в title внутри properties)
- Пробелы в slug заменяются на дефис
- Example: `удовольствие-от-результата.md`, `single-tasking-focus.md`

ЗАПРЕЩЕНО:
- Дата в имени файла (НЕ `2026-02-16-slug.md`)
- Тире вместо пробелов в title (тире ОК в slug, НО в title — только пробелы)

## Frontmatter (Required)

```yaml
---
Created: YYYY-MM-DD HH:MM
type: idea | reflection | project | learning
tags:
  - tag1
  - tag2
reference: "[[daily/YYYY-MM-DD]]"
links:
  - "[[Related Note]]"
---
```

### Field Rules

| Field | Required | Format | Notes |
|-------|----------|--------|-------|
| Created | YES | `YYYY-MM-DD HH:MM` | Заглавная C, обязательно время |
| type | YES | enum | idea/reflection/project/learning |
| tags | YES | YAML list | Релевантные теги |
| reference | YES | wiki-link | Источник: `"[[daily/YYYY-MM-DD]]"` |
| links | NO | YAML list | Связи с другими заметками |

ВАЖНО:
- `Created` с заглавной буквы (не `created`, не `date`)
- Обязательно указывать ВРЕМЯ (не только дату)
- `reference` — откуда взята мысль (обычно daily note)
- `tags` — НЕ `type`, поле называется `tags`
- `links` — НЕ `related`

## Content Structure

После frontmatter — сразу текст. БЕЗ заголовка.

```markdown
---
Created: 2026-02-16 15:00
type: reflection
tags:
  - mindset
  - growth
reference: "[[daily/2026-02-16]]"
links:
  - "[[Фундаментальный 2026 YEAR]]"
---

Текст заметки начинается сразу здесь. Без заголовка `# Title`.
Заголовок уже есть в имени файла и в properties.

Продолжение текста...
```

ЗАПРЕЩЕНО после frontmatter:
- `# Заголовок` — не нужен, название = имя файла
- Пустые секции (## Summary, ## Details, ## Action Items) — только если есть контент
- Шаблонные блоки без содержания

## Wiki-Links

When saving a thought:

1. **Search for related notes** in thoughts/ and goals/
2. **Link to relevant existing notes** — НЕ создавать новые заметки без разрешения
3. **Add backlinks** to source daily note via reference field

## Tags Convention

Простые теги без иерархии:
```
mindset, growth, productivity, focus, habits, health, work, video-editing
```

## Category Guidelines

### ideas/
- Novel concepts, inventions
- Business ideas
- Creative solutions
- "What if..." thoughts

### reflections/
- Personal insights
- Lessons learned
- Emotional processing
- Gratitude, wins

### projects/
- Project-specific notes
- Meeting notes
- Status updates
- Decisions made

### learnings/
- New knowledge
- Book/article insights
- Technical discoveries
- "TIL" moments
