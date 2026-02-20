# Todoist Integration

<!--
╔══════════════════════════════════════════════════════════════════╗
║  КАК НАСТРОИТЬ ЭТОТ ФАЙЛ                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Замените [Your Clients] на имена ваших клиентов              ║
║  2. Замените [Your Company] на название вашей компании           ║
║  3. Замените [@your_channel] на ваш Telegram-канал               ║
║  4. Измените примеры задач на релевантные для вас                ║
║  5. Удалите этот комментарий после настройки                     ║
╚══════════════════════════════════════════════════════════════════╝
-->

## Available MCP Tools

### Reading Tasks
- `get-overview` — all projects with hierarchy
- `find-tasks` — search by text, project, section
- `find-tasks-by-date` — tasks by date range

### Writing Tasks
- `add-tasks` — create new tasks
- `complete-tasks` — mark as done
- `update-tasks` — modify existing

---

## Pre-Creation Checklist

### Check Duplicates (REQUIRED)

```
find-tasks:
  searchText: "key words from new task"
```

If similar exists → mark as duplicate, don't create.

---

## Date Mapping

| Context | dueString |
|---------|-----------|
| **Client deadline** | exact date |
| **Urgent ops** | today / tomorrow |
| **This week** | friday |
| **Next week** | next monday |
| **Strategic/R&D** | in 7 days |
| **Not specified** | in 3 days |

### Russian → dueString

| Russian | dueString |
|---------|-----------|
| сегодня | today |
| завтра | tomorrow |
| послезавтра | in 2 days |
| в понедельник | monday |
| в пятницу | friday |
| на этой неделе | friday |
| на следующей неделе | next monday |
| через неделю | in 7 days |
| 15 января | January 15 |

---

## Task Creation

```
add-tasks:
  tasks:
    - content: "Task title"
      dueString: "friday"  # MANDATORY
      projectId: "..."     # if known
```

### Task Title Style

User prefers: прямота, ясность, конкретика

<!-- Замените примеры на релевантные для вас -->
Good:
- "Отправить презентацию клиенту"
- "Созвон с командой по проекту"
- "Написать пост про [тема]"

Bad:
- "Подумать о презентации"
- "Что-то с клиентом"
- "Разобраться с AI"

All tasks go to Inbox by default (no projectId), unless user explicitly specifies a project.

---

## Anti-Patterns (НЕ СОЗДАВАТЬ)

Based on user preferences:

- "Подумать о..." -- конкретизируй действие
- "Разобраться с..." -- что именно сделать?
- Абстрактные задачи без Next Action
- Дубликаты существующих задач
- Задачи без дат

---

## Error Handling

CRITICAL: Никогда не предлагай "добавить вручную".

If `add-tasks` fails:
1. Include EXACT error message in report
2. Continue with next entry
3. Don't mark as processed
4. User will see error and can debug

WRONG output:
  "Не удалось добавить (MCP недоступен). Добавь вручную: Task title"

CORRECT output:
  "Ошибка создания задачи: [exact error from MCP tool]"
