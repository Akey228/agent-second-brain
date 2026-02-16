# Entry Classification

<!--
╔══════════════════════════════════════════════════════════════════╗
║  КАК НАСТРОИТЬ ЭТОТ ФАЙЛ                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Замените [Your Client Names] на имена ваших клиентов        ║
║  2. Замените [Your Company] на название вашей компании          ║
║  3. Замените [@your_channel] на ваш Telegram-канал              ║
║  4. Добавьте свои домены работы, если они отличаются            ║
║  5. Удалите этот комментарий после настройки                    ║
╚══════════════════════════════════════════════════════════════════╝
-->

## Work Domains → Categories

Based on user's work context (see [ABOUT.md](ABOUT.md)):

### Client Work
Брифы, стратегии, креатив, кампании, KPI, предложения

<!-- Добавьте имена ваших клиентов через запятую -->
**Keywords:** [Your Client Names], клиент, бриф, презентация, дедлайн, KPI

**→ Category:** task → Todoist

### AI & Tech
Инструменты, модели, промпты, пайплайны, агенты

**Keywords:** GPT, Claude, модель, агент, API, пайплайн, автоматизация, интеграция

**→ Category:** learning или project → thoughts/

### Product
Идеи, гипотезы, MVP, юнит-экономика

**Keywords:** продукт, SaaS, MVP, гипотеза, монетизация, юнит-экономика, стартап

**→ Category:** idea или project → thoughts/

### Company Ops
Команда, процессы, автоматизация, найм, управление, финансы

<!-- Замените [Your Company] на название вашей компании/проекта -->
**Keywords:** команда, найм, процесс, HR, финансы, [Your Company]

**→ Category:** task или project (depends on urgency)

### Content
Посты, идеи, тезисы для Telegram и LinkedIn

<!-- Замените [@your_channel] на ваш Telegram-канал или удалите если не нужно -->
**Keywords:** пост, [@your_channel], LinkedIn, контент, тезис, статья

**→ Category:** idea → thoughts/ideas/ или task если с дедлайном

---

## Decision Tree

```
Entry text contains...
│
├─ Client brand or deadline? ────────────────────> TASK
│  ([Your Clients], клиент, дедлайн, презентация)
│
├─ Operational/urgent? ──────────────────────────> TASK
│  (нужно сделать, не забыть, позвонить, встреча)
│
├─ AI/tech learning? ────────────────────────────> LEARNING
│  (узнал, модель, агент, интеграция)
│
├─ Product/SaaS idea? ───────────────────────────> IDEA или PROJECT
│  (продукт, MVP, гипотеза, SaaS)
│
├─ Strategic thinking? ──────────────────────────> PROJECT
│  (стратегия, план, R&D, долгосрочно)
│
├─ Personal insight? ────────────────────────────> REFLECTION
│  (понял, осознал, философия)
│
└─ Content idea? ────────────────────────────────> IDEA
   (пост, тезис, контент)
```

## Photo Entries

For `[photo]` entries:

1. Analyze image content via vision
2. Determine domain:
   - Screenshot клиентского материала → Client Work
   - Схема/диаграмма → AI & Tech или Product
   - Текст/статья → Learning
3. Add description to daily file

---

## Output Locations

| Category | Destination |
|----------|-------------|
| task | Todoist |
| idea | thoughts/ideas/ |
| reflection | thoughts/reflections/ |
| project | thoughts/projects/ |
| learning | thoughts/learnings/ |

---

## File Naming

```
thoughts/{category}/slug.md
```

БЕЗ даты в имени файла. Slug — lowercase, дефисы вместо пробелов.

Examples:
```
thoughts/ideas/saas-pricing-model.md
thoughts/projects/ai-agents-pipeline.md
thoughts/learnings/claude-mcp-setup.md
thoughts/reflections/удовольствие-от-результата.md
```

---

## Thought Structure

Use preferred format:

```markdown
---
Created: YYYY-MM-DD HH:MM
type: {category}
tags:
  - tag1
  - tag2
reference: "[[daily/YYYY-MM-DD]]"
links:
  - "[[Related Note]]"
---

Текст заметки начинается сразу после frontmatter. БЕЗ заголовка # Title.
```

ВАЖНО:
- `Created` с заглавной C, обязательно с временем
- `reference` — источник (обычно daily note)
- `links` — связи с существующими заметками
- НЕ добавлять `# Заголовок` после frontmatter
- НЕ создавать новые заметки-ссылки без разрешения пользователя

---

## Anti-Patterns (ИЗБЕГАТЬ)

При создании мыслей НЕ делать:
- Абстрактные рассуждения без Next Action
- Академическая теория без применения к вашему проекту/продукту
- Повторы без синтеза (кластеризуй похожие!)
- Хаотичные списки без приоритетов
- Задачи типа "подумать о..." (конкретизируй!)

---

## MOC Updates

After creating thought file, add link to:
```
MOC/MOC-{category}s.md
```

Group by domain when relevant:
```markdown
## AI & Tech
- [[2024-12-16-claude-mcp-setup]] - MCP integration

## Product
- [[2024-12-16-saas-pricing-model]] - Pricing research
```
