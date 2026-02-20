"""Report formatters for Telegram messages."""

import asyncio
import html
import logging
import re
from typing import Any

from aiogram.types import Message

logger = logging.getLogger(__name__)


# Allowed HTML tags in Telegram
ALLOWED_TAGS = {"b", "i", "code", "pre", "a", "s", "u"}


def sanitize_telegram_html(text: str) -> str:
    """Sanitize HTML for Telegram, keeping only allowed tags.

    Telegram supports: <b>, <i>, <code>, <pre>, <a>, <s>, <u>

    Args:
        text: Raw HTML text from Claude

    Returns:
        Sanitized HTML safe for Telegram
    """
    if not text:
        return ""

    # First, escape any raw < > that are not part of tags
    # This regex matches < or > not followed/preceded by tag patterns
    result = []
    i = 0
    while i < len(text):
        if text[i] == "<":
            # Check if this looks like a valid tag
            tag_match = re.match(r"</?([a-zA-Z]+)(?:\s[^>]*)?>", text[i:])
            if tag_match:
                tag_name = tag_match.group(1).lower()
                if tag_name in ALLOWED_TAGS:
                    # Keep the allowed tag
                    result.append(tag_match.group(0))
                    i += len(tag_match.group(0))
                    continue
                else:
                    # Escape disallowed tag
                    result.append("&lt;")
                    i += 1
                    continue
            else:
                # Not a valid tag pattern, escape
                result.append("&lt;")
                i += 1
                continue
        elif text[i] == ">":
            # Standalone > should be escaped
            result.append("&gt;")
            i += 1
        elif text[i] == "&":
            # Check if already escaped
            entity_match = re.match(r"&(amp|lt|gt|quot|#\d+|#x[0-9a-fA-F]+);", text[i:])
            if entity_match:
                result.append(entity_match.group(0))
                i += len(entity_match.group(0))
            else:
                result.append("&amp;")
                i += 1
        else:
            result.append(text[i])
            i += 1

    return "".join(result)


def validate_telegram_html(text: str) -> bool:
    """Validate that HTML tags are properly closed.

    Args:
        text: HTML text to validate

    Returns:
        True if valid, False otherwise
    """
    tag_stack = []
    tag_pattern = re.compile(r"<(/?)([a-zA-Z]+)(?:\s[^>]*)?>")

    for match in tag_pattern.finditer(text):
        is_closing = match.group(1) == "/"
        tag_name = match.group(2).lower()

        if tag_name not in ALLOWED_TAGS:
            continue

        if is_closing:
            if not tag_stack or tag_stack[-1] != tag_name:
                return False
            tag_stack.pop()
        else:
            tag_stack.append(tag_name)

    return len(tag_stack) == 0


def _get_open_tags(text: str) -> list[str]:
    """Return list of currently open HTML tags in order."""
    tag_pattern = re.compile(r"<(/?)([a-zA-Z]+)(?:\s[^>]*)?>")
    open_tags: list[str] = []

    for match in tag_pattern.finditer(text):
        is_closing = match.group(1) == "/"
        tag_name = match.group(2).lower()

        if tag_name not in ALLOWED_TAGS:
            continue

        if is_closing and open_tags and open_tags[-1] == tag_name:
            open_tags.pop()
        elif not is_closing:
            open_tags.append(tag_name)

    return open_tags


def split_html(text: str, max_length: int = 4096) -> list[str]:
    """Split HTML text into chunks that fit Telegram's message limit.

    Splits on sentence boundaries when possible, keeps tags balanced
    across chunks by re-opening tags at the start of each new chunk.

    Args:
        text: HTML text to split
        max_length: Maximum length per chunk (Telegram limit is 4096)

    Returns:
        List of HTML chunks, each within max_length
    """
    if len(text) <= max_length:
        return [text]

    chunks: list[str] = []
    remaining = text

    while remaining:
        if len(remaining) <= max_length:
            chunks.append(remaining)
            break

        # Leave room for closing/opening tags
        cut_point = max_length - 100

        # Don't cut in the middle of a tag
        last_open = remaining.rfind("<", 0, cut_point)
        last_close = remaining.rfind(">", 0, cut_point)
        if last_open > last_close:
            cut_point = last_open

        # Try to cut at a sentence boundary (. ! ? followed by space or newline)
        sentence_end = -1
        for pattern in [". ", ".\n", "! ", "!\n", "? ", "?\n"]:
            pos = remaining.rfind(pattern, 0, cut_point)
            if pos > cut_point // 2:  # Only if reasonably far into the chunk
                sentence_end = max(sentence_end, pos + 1)

        # Try paragraph boundary
        para_end = remaining.rfind("\n\n", 0, cut_point)
        if para_end > cut_point // 2:
            sentence_end = max(sentence_end, para_end)

        if sentence_end > 0:
            cut_point = sentence_end

        chunk = remaining[:cut_point]
        remaining = remaining[cut_point:].lstrip()

        # Close open tags in this chunk
        open_tags = _get_open_tags(chunk)
        closing = "".join(f"</{tag}>" for tag in reversed(open_tags))
        chunk += closing

        chunks.append(chunk)

        # Re-open tags at start of next chunk
        if remaining and open_tags:
            opening = "".join(f"<{tag}>" for tag in open_tags)
            remaining = opening + remaining

    return chunks


async def send_long_message(
    message: Message, text: str, parse_mode: str | None = "HTML"
) -> None:
    """Send a message that may exceed Telegram's 4096 char limit.

    Splits into multiple messages if needed. Falls back to plain text
    on parse errors.
    """
    chunks = split_html(text) if parse_mode else [text[i:i + 4096] for i in range(0, len(text), 4096)]

    for chunk in chunks:
        try:
            await message.answer(chunk, parse_mode=parse_mode)
        except Exception:
            try:
                await message.answer(chunk, parse_mode=None)
            except Exception:
                logger.exception("Failed to send message chunk (%d chars)", len(chunk))
        if len(chunks) > 1:
            await asyncio.sleep(0.3)


def format_process_report(report: dict[str, Any]) -> str:
    """Format processing report for Telegram HTML.

    The report from Claude is expected to be in HTML format.
    We sanitize it to ensure only Telegram-safe tags are used.

    Args:
        report: Processing report from ClaudeProcessor

    Returns:
        Formatted HTML message for Telegram
    """
    if "error" in report:
        error_msg = html.escape(str(report["error"]))
        return f"[Ошибка] <b>Ошибка:</b> {error_msg}"

    if "report" in report:
        raw_report = report["report"]

        # Sanitize HTML, keeping allowed tags
        sanitized = sanitize_telegram_html(raw_report)

        # Validate tag balance
        if not validate_telegram_html(sanitized):
            # Fall back to plain text if tags are broken
            return html.escape(raw_report)

        return sanitized

    return "[OK] <b>Обработка завершена</b>"


def format_error(error: str) -> str:
    """Format error message for Telegram.

    Args:
        error: Error message

    Returns:
        Formatted HTML error message
    """
    return f"[Ошибка] <b>Ошибка:</b> {html.escape(error)}"


