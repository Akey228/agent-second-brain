"""Handler for /model command — select Claude model."""

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from d_brain.bot.states import AVAILABLE_MODELS, DEFAULT_MODEL_KEY

router = Router(name="model")
logger = logging.getLogger(__name__)

MODEL_CB_PREFIX = "model:"


def _build_keyboard(current_key: str) -> InlineKeyboardMarkup:
    """Build inline keyboard with model options."""
    buttons = []
    for key, info in AVAILABLE_MODELS.items():
        marker = " [x]" if key == current_key else ""
        buttons.append(
            InlineKeyboardButton(
                text=f"{info['label']}{marker}",
                callback_data=f"{MODEL_CB_PREFIX}{key}",
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@router.message(Command("model"))
async def cmd_model(message: Message, state: FSMContext) -> None:
    """Show model selection menu."""
    data = await state.get_data()
    current = data.get("model_key", DEFAULT_MODEL_KEY)
    current_label = AVAILABLE_MODELS[current]["label"]

    await message.answer(
        f"Текущая модель: <b>{current_label}</b>\n\nВыбери модель:",
        reply_markup=_build_keyboard(current),
    )


@router.callback_query(lambda c: c.data and c.data.startswith(MODEL_CB_PREFIX))
async def on_model_selected(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle model selection callback."""
    if not callback.data:
        return

    key = callback.data.removeprefix(MODEL_CB_PREFIX)
    if key not in AVAILABLE_MODELS:
        await callback.answer("Неизвестная модель")
        return

    await state.update_data(model_key=key)
    label = AVAILABLE_MODELS[key]["label"]

    await callback.answer(f"Модель: {label}")

    if callback.message:
        await callback.message.edit_text(
            f"Модель переключена на <b>{label}</b>",
            reply_markup=_build_keyboard(key),
        )
