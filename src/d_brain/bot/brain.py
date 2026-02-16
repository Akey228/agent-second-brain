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
    settings = get_settings()
    processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)

    # Send typing immediately before starting processing
    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    except Exception as e:
        logger.warning("Failed to send initial typing action: %s", e)

    task = asyncio.create_task(
        asyncio.to_thread(processor.execute_prompt, user_text, user_id)
    )

    # Keep sending "typing..." every 4 seconds while model is thinking
    while not task.done():
        await asyncio.sleep(4)
        if not task.done():
            try:
                await message.bot.send_chat_action(
                    chat_id=message.chat.id, action="typing"
                )
            except Exception as e:
                logger.warning("Failed to send typing action in loop: %s", e)

    result = await task

    formatted = format_process_report(result)
    try:
        await message.answer(formatted)
    except Exception:
        try:
            await message.answer(formatted, parse_mode=None)
        except Exception:
            logger.exception("Failed to send brain response")
