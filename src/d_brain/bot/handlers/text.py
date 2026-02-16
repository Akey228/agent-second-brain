"""Text message handler — route through brain."""

import logging
from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from d_brain.bot.brain import process_with_brain
from d_brain.config import get_settings
from d_brain.services import create_storage
from d_brain.services.session import SessionStore

router = Router(name="text")
logger = logging.getLogger(__name__)


@router.message(lambda m: m.text is not None and not m.text.startswith("/"))
async def handle_text(message: Message) -> None:
    """Handle text messages — save and route through Claude brain."""
    if not message.text or not message.from_user:
        return

    settings = get_settings()
    storage = create_storage(settings)

    # Save to daily file
    timestamp = datetime.fromtimestamp(message.date.timestamp())
    storage.append_to_daily(message.text, timestamp, "[text]")

    # Log to session
    session = SessionStore(settings.vault_path)
    session.append(
        message.from_user.id,
        "text",
        text=message.text,
        msg_id=message.message_id,
    )

    logger.info("Text message saved: %d chars", len(message.text))

    # Route through brain
    await process_with_brain(message, message.text, message.from_user.id)
