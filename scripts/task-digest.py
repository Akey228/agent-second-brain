#!/usr/bin/env python
"""Task digest — sends today's Todoist tasks to Telegram.

Runs 3 times daily (6:00, 15:00, 19:00) via systemd timer.
Shows work tasks first (label "работа"), then the rest.
If no tasks — sends "На сегодня задач нет".
"""

import asyncio
import logging
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from todoist_api_python.api import TodoistAPI

from d_brain.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

TZ = ZoneInfo("Asia/Krasnoyarsk")
WORK_LABEL = "работа"


def get_today_tasks(api: TodoistAPI) -> list[dict]:
    """Fetch today's tasks (including overdue) from Todoist API."""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    try:
        all_tasks = []
        for page in api.filter_tasks(query="today | overdue"):
            all_tasks.extend(page)
    except Exception:
        logger.exception("Failed to fetch tasks from Todoist")
        return []

    result = []
    for task in all_tasks:
        due = task.due
        due_date_str = due.date if due else None
        # due.date can be a string "YYYY-MM-DD" or datetime.date
        if isinstance(due_date_str, date):
            is_overdue = due_date_str < today
        elif isinstance(due_date_str, str):
            is_overdue = due_date_str < today_str
        else:
            is_overdue = False
        result.append({
            "id": task.id,
            "content": task.content,
            "due_date": str(due_date_str) if due_date_str else None,
            "labels": task.labels or [],
            "is_overdue": is_overdue,
        })

    return result


def format_digest(tasks: list[dict]) -> str:
    """Format task list as Telegram HTML.

    Work tasks (label "работа") go first, then the rest.
    No section headers — just a flat list with work tasks on top.
    """
    now = datetime.now(TZ)
    time_str = now.strftime("%H:%M")
    today_str = now.strftime("%d.%m.%Y")

    header = f"<b>Задачи на сегодня</b> ({today_str}, {time_str})\n"

    if not tasks:
        return header + "\nНа сегодня задач нет"

    # Split into work and other
    work_tasks = [t for t in tasks if WORK_LABEL in t["labels"]]
    other_tasks = [t for t in tasks if WORK_LABEL not in t["labels"]]

    # Ordered: work first, then other
    ordered = work_tasks + other_tasks

    lines = [header]
    for i, task in enumerate(ordered, 1):
        overdue_mark = " <i>(просрочена)</i>" if task["is_overdue"] else ""
        lines.append(f"{i}. {task['content']}{overdue_mark}")

    return "\n".join(lines)


async def send_digest(bot: Bot, chat_id: int, text: str) -> None:
    """Send digest message to Telegram."""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception:
        # Fallback: send without HTML
        try:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=None)
        except Exception:
            logger.exception("Failed to send digest to Telegram")


async def main() -> None:
    """Fetch tasks and send digest to Telegram."""
    settings = get_settings()

    if not settings.todoist_api_key:
        logger.error("TODOIST_API_KEY not configured")
        return

    user_id = settings.allowed_user_ids[0] if settings.allowed_user_ids else None
    if not user_id:
        logger.error("No allowed user IDs configured")
        return

    # Fetch tasks
    api = TodoistAPI(settings.todoist_api_key)
    tasks = get_today_tasks(api)

    # Format
    digest = format_digest(tasks)

    logger.info("Digest: %d tasks found, sending to user %s", len(tasks), user_id)

    # Send
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    try:
        await send_digest(bot, user_id, digest)
        logger.info("Task digest sent successfully")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
