# Agent Second Brain

Voice-first personal assistant for capturing thoughts and managing tasks via Telegram.

## EVERY SESSION BOOTSTRAP

**Before doing anything else, read these files in order:**

1. `vault/MEMORY.md` — curated long-term memory (preferences, decisions, context)
2. Today's session log from `vault/.sessions/` — current entries

**Don't ask permission, just do it.** This ensures context continuity across sessions.

---

## SESSION END PROTOCOL

**Update `vault/MEMORY.md` if:**
- New key decision was made
- User preference discovered
- Important fact learned
- Active context changed significantly

---

## Mission

Help user stay aligned with goals, capture valuable insights, and maintain clarity.

## Directory Structure

| Folder | Purpose |
|--------|---------|
| `0. System/` | Files (attachments), Templates, Home Dashboard |
| `1. Inbox/` | Incoming notes, fleeting/literature/permanent, MOCs |
| `5. Projects/` | Active projects |
| `6. Areas/` | Life areas (goals, health, etc.) |
| `7. Resources/` | Reference material (editing, finance, etc.) |
| `8. Archives/` | Archived content |

## Current Focus

See [[goals/3-weekly]] for this week's ONE Big Thing.
See [[goals/2-monthly]] for monthly priorities.

## Goals Hierarchy

```
goals/0-vision-3y.md    → 3-year vision by life areas
goals/1-yearly-2025.md  → Annual goals + quarterly breakdown
goals/2-monthly.md      → Current month's top 3 priorities
goals/3-weekly.md       → This week's focus + ONE Big Thing
```

## Processing Workflow

Messages are processed in real-time via Claude brain. Session logs are stored in `.sessions/`.

## Daily Journal (Дневник)

Trigger: user says "добавь дневные заметки", "добавь в дневник", "запиши в дневник" or similar.

### Rules:
1. **One file per day:** `vault/YYYY-MM-DD.md` (e.g. `vault/2026-02-21.md`)
2. **Accumulates:** entries are ADDED, never overwritten
3. **Entry format:** `## HH:MM` header + cleaned text below
4. **Text cleanup:** minimal — remove word repetitions, tautology. Do NOT restructure, add lists, headers, conclusions
5. **What goes in:** only substantive voice/text entries from session log. NOT commands, questions, greetings
6. **Frontmatter:** standard with `Tags: дневник`
7. **Linked References:** always at the end of file
8. **S3 sync:** pull before, push after (handled automatically by processor)

## Work Notes (Рабочие заметки)

Trigger: user says "рабочие заметки", "добавь в рабочие заметки", "рабочую заметку" or similar.

### Rules:
1. **One file per day:** `vault/WorkDaily/Work YYYY-MM-DD.md` (e.g. `vault/WorkDaily/Work 2026-02-23.md`)
2. **Accumulates:** entries are ADDED, never overwritten
3. **Entry format:** `## HH:MM` header + cleaned text below
4. **Text cleanup:** minimal — remove word repetitions, tautology. Do NOT restructure, add lists, headers, conclusions
5. **What goes in:** only substantive work-related entries from session log. NOT commands, questions, greetings
6. **Frontmatter:** standard with `Tags: рабочий дневник`
7. **Linked References:** always at the end of file
8. **S3 sync:** pull before, push after (handled automatically by processor)

## Available Skills

| Skill | Purpose |
|-------|---------|
| `dbrain-processor` | Main daily processing |
| `todoist-ai` | Task management via MCP |
| `graph-builder` | Vault link analysis and building |

## Available Agents

| Agent | Purpose |
|-------|---------|
| `weekly-digest` | Weekly review with goal progress |
| `goal-aligner` | Check task-goal alignment |
| `note-organizer` | Organize vault, fix links |
| `inbox-processor` | GTD-style inbox processing |

## Path-Specific Rules

See `.claude/rules/` for format requirements:
- `thoughts-format.md` — thought notes format
- `goals-format.md` — goals format
- `telegram-report.md` — HTML report format

## MCP Servers

- `todoist` — Task management (add, find, complete tasks)
- `filesystem` — Vault file access

## CRITICAL: Tool Usage Policy

**ТЫ ОБЯЗАН ВЫЗЫВАТЬ MCP TOOLS НАПРЯМУЮ.**

Не существует ситуации, когда MCP tools "недоступны". Если ты получил эту инструкцию — у тебя есть доступ к:

- `mcp__todoist__*` — все Todoist операции
- File read/write — все файловые операции

ЗАПРЕЩЁННЫЕ ПАТТЕРНЫ (НИКОГДА не делай это):
- "MCP недоступен в текущем режиме"
- "Не удалось добавить автоматически"
- "Добавь вручную: ..."
- Любые инструкции для ручного выполнения

ПРАВИЛЬНЫЙ ПАТТЕРН:
1. Вызвать mcp__todoist__add-tasks tool
2. Получить результат (успех или ошибка)
3. Включить результат в HTML отчёт

При ошибке — показать ТОЧНУЮ ошибку от tool, не придумывать отговорки.

## Report Format

Reports use Telegram HTML:
- `<b>bold</b>` for headers
- `<i>italic</i>` for metadata
- Only allowed tags: b, i, code, pre, a

## Quick Commands

| Command | Action |
|---------|--------|
| `/process` | Run daily processing |
| `/do` | Execute arbitrary request |
| `/weekly` | Generate weekly digest |
| `/align` | Check goal alignment |
| `/organize` | Organize vault |
| `/graph` | Analyze vault links |

## /do Command Context

When invoked via /do, Claude receives arbitrary user requests. Common patterns:

**Task Management:**
- "перенеси просроченные задачи на понедельник"
- "покажи задачи на сегодня"
- "добавь задачу: позвонить клиенту"
- "что срочного на этой неделе?"

**Vault Queries:**
- "найди заметки про AI"
- "что я записал сегодня?"
- "покажи итоги недели"

**Combined:**
- "создай задачу из первой записи сегодня"
- "перенеси всё с сегодня на завтра"

## MCP Tools Available

**Todoist (mcp__todoist__*):**
- `add-tasks` — создать задачи
- `find-tasks` — найти задачи по тексту
- `find-tasks-by-date` — задачи за период
- `update-tasks` — изменить задачи
- `complete-tasks` — завершить задачи
- `user-info` — информация о пользователе

**Filesystem:**
- Read/write vault files

## Customization

For personal overrides: create `CLAUDE.local.md`

## Graph Builder

Analyze and maintain vault link structure. Use `/graph` command or invoke `graph-builder` skill.

**Commands:**
- `/graph analyze` — Full vault statistics
- `/graph orphans` — List unconnected notes
- `/graph suggest` — Get link suggestions
- `/graph add` — Apply suggested links

**Scripts:**
- `uv run .claude/skills/graph-builder/scripts/analyze.py` — Graph analysis
- `uv run .claude/skills/graph-builder/scripts/add_links.py` — Link suggestions

See `skills/graph-builder/` for full documentation.

## Learnings (from experience)

1. **Don't rewrite working code** without reason (KISS, DRY, YAGNI)
2. **Don't add checks** that weren't there — let the agent decide
3. **Don't propose solutions** without studying git log/diff first
4. **Don't break architecture** (process.sh → Claude → skill is correct)
5. **Problems are usually simple** (e.g., sed one-liner for HTML fix)

---

*System Version: 2.3*
*Updated: 2026-02-01*
