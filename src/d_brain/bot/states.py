"""Bot FSM states."""

from aiogram.fsm.state import State, StatesGroup

# Available models for user selection
AVAILABLE_MODELS = {
    "sonnet": {"id": "claude-sonnet-4-5-20250929", "label": "Sonnet 4.5"},
    "opus": {"id": "claude-opus-4-6", "label": "Opus 4.6"},
}

DEFAULT_MODEL_KEY = "opus"


class DoCommandState(StatesGroup):
    """States for /do command flow."""

    waiting_for_input = State()  # Waiting for voice or text after /do
