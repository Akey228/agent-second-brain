"""Process command handler — daily summary."""

import asyncio
import logging
from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from d_brain.bot.formatters import format_process_report
from d_brain.config import get_settings
from d_brain.services.git import VaultGit
from d_brain.services.processor import ClaudeProcessor

router = Router(name="process")
logger = logging.getLogger(__name__)


@router.message(Command("process"))
async def cmd_process(message: Message) -> None:
    """Handle /process command — generate daily summary."""
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info("Process command triggered by user %s", user_id)

    status_msg = await message.answer("📊 Готовлю сводку дня...")

    settings = get_settings()
    processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)
    git = VaultGit(settings.vault_path)

    async def process_with_progress() -> dict:
        task = asyncio.create_task(
            asyncio.to_thread(processor.process_daily, date.today())
        )

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    await status_msg.edit_text(
                        f"📊 Готовлю сводку... ({elapsed // 60}m {elapsed % 60}s)"
                    )
                except Exception:
                    pass

        return await task

    report = await process_with_progress()

    # Commit and push changes
    if "error" not in report:
        today = date.today().isoformat()
        await asyncio.to_thread(git.commit_and_push, f"chore: daily summary {today}")

    # Format and send report
    formatted = format_process_report(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        await status_msg.edit_text(formatted, parse_mode=None)
