"""Forwarded message handler — save and route through brain."""

import logging
from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from d_brain.bot.brain import process_with_brain
from d_brain.config import get_settings
from d_brain.services import create_storage
from d_brain.services.session import SessionStore

router = Router(name="forward")
logger = logging.getLogger(__name__)


@router.message(lambda m: m.forward_origin is not None)
async def handle_forward(message: Message, state: FSMContext) -> None:
    """Handle forwarded messages — save and route through Claude brain."""
    if not message.from_user:
        return

    settings = get_settings()
    storage = create_storage(settings)

    # Determine source name
    source_name = "Unknown"
    origin = message.forward_origin

    if hasattr(origin, "sender_user") and origin.sender_user:
        user = origin.sender_user
        source_name = user.full_name
    elif hasattr(origin, "sender_user_name") and origin.sender_user_name:
        source_name = origin.sender_user_name
    elif hasattr(origin, "chat") and origin.chat:
        chat = origin.chat
        source_name = f"@{chat.username}" if chat.username else chat.title or "Channel"
    elif hasattr(origin, "sender_name") and origin.sender_name:
        source_name = origin.sender_name

    content = message.text or message.caption or "[media]"
    msg_type = f"[forward from: {source_name}]"

    timestamp = datetime.fromtimestamp(message.date.timestamp())
    storage.append_to_daily(content, timestamp, msg_type)

    # Log to session
    session = SessionStore(settings.vault_path)
    session.append(
        message.from_user.id,
        "forward",
        text=content,
        source=source_name,
        msg_id=message.message_id,
    )

    logger.info("Forwarded message saved from: %s", source_name)

    # Route through brain
    brain_text = f"[Переслано от {source_name}]: {content}"
    data = await state.get_data()
    await process_with_brain(message, brain_text, message.from_user.id, data.get("model_key", ""))
