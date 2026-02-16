"""Command handlers — /start only."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router(name="commands")


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    await message.answer(
        "<b>d-brain</b> — твой персональный AI-ассистент\n\n"
        "Просто говори или пиши — я пойму что нужно:\n"
        "создать задачу, сохранить мысль, ответить на вопрос.\n\n"
        "Голос / Текст / Фото / Пересылки",
        reply_markup=ReplyKeyboardRemove(),
    )
