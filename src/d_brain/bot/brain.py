"""Shared brain function — routes every message through Claude."""

import asyncio
import logging

from aiogram.types import Message

from d_brain.bot.formatters import format_process_report
from d_brain.config import get_settings
from d_brain.services.processor import ClaudeProcessor

logger = logging.getLogger(__name__)


async def process_with_brain(message: Message, user_text: str, user_id: int = 0) -> None:
    """Send message to Claude brain and return response.

    Args:
        message: Telegram message to reply to
        user_text: Text to process (transcription, raw text, caption, etc.)
        user_id: Telegram user ID for session context
    """
    status_msg = await message.answer("💭")

    settings = get_settings()
    processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)

    async def run_with_progress() -> dict:
        task = asyncio.create_task(
            asyncio.to_thread(processor.execute_prompt, user_text, user_id)
        )

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    mins = elapsed // 60
                    secs = elapsed % 60
                    await status_msg.edit_text(f"💭 {mins}m {secs}s...")
                except Exception:
                    pass

        return await task

    result = await run_with_progress()

    formatted = format_process_report(result)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        try:
            await status_msg.edit_text(formatted, parse_mode=None)
        except Exception:
            logger.exception("Failed to send brain response")
