"""Vault storage service for saving entries."""

from __future__ import annotations

import logging
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from d_brain.services.s3_sync import S3SyncService

logger = logging.getLogger(__name__)


class VaultStorage:
    """Service for storing entries in Obsidian vault."""

    def __init__(
        self,
        vault_path: Path,
        s3: S3SyncService | None = None,
    ) -> None:
        self.vault_path = Path(vault_path)
        self.daily_path = self.vault_path / "daily"
        self.attachments_path = self.vault_path / "attachments"
        self.inbox_path = self.vault_path / "1. Inbox"
        self._s3 = s3

    def _ensure_dirs(self) -> None:
        """Ensure required directories exist."""
        self.daily_path.mkdir(parents=True, exist_ok=True)
        self.attachments_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

    def _sync_to_s3(self, local_path: Path) -> None:
        """Upload file to S3 if sync is configured."""
        if self._s3 is None:
            return
        try:
            self._s3.upload_file(local_path, self.vault_path)
        except Exception:
            logger.exception("S3 sync failed for %s", local_path)

    def get_daily_file(self, day: date) -> Path:
        """Get path to daily file for given date."""
        self._ensure_dirs()
        return self.daily_path / f"{day.isoformat()}.md"

    def read_daily(self, day: date) -> str:
        """Read content of daily file."""
        file_path = self.get_daily_file(day)
        if not file_path.exists():
            return ""
        return file_path.read_text(encoding="utf-8")

    def append_to_daily(
        self,
        text: str,
        timestamp: datetime,
        msg_type: str,
    ) -> None:
        """Append entry to daily file.

        Args:
            text: Content to append
            timestamp: Entry timestamp
            msg_type: Type marker like [voice], [text], [photo], [forward from: Name]
        """
        self._ensure_dirs()
        file_path = self.get_daily_file(timestamp.date())

        time_str = timestamp.strftime("%H:%M")
        entry = f"\n## {time_str} {msg_type}\n{text}\n"

        with file_path.open("a", encoding="utf-8") as f:
            f.write(entry)

        self._sync_to_s3(file_path)

    def get_attachments_dir(self, day: date) -> Path:
        """Get attachments directory for given date."""
        dir_path = self.attachments_path / day.isoformat()
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def save_attachment(
        self,
        data: bytes,
        day: date,
        timestamp: datetime,
        extension: str = "jpg",
    ) -> str:
        """Save attachment and return relative path for Obsidian embed.

        Args:
            data: File bytes
            day: Date for organizing
            timestamp: Timestamp for filename
            extension: File extension

        Returns:
            Relative path for Obsidian embed: attachments/YYYY-MM-DD/img-HHMMSS.ext
        """
        dir_path = self.get_attachments_dir(day)
        time_str = timestamp.strftime("%H%M%S")
        filename = f"img-{time_str}.{extension}"
        file_path = dir_path / filename

        file_path.write_bytes(data)

        self._sync_to_s3(file_path)

        return f"attachments/{day.isoformat()}/{filename}"

    def create_note(
        self,
        title: str,
        content: str,
        tag: str = "idea",
        reference: str = "",
        links: list[str] | None = None,
    ) -> Path:
        """Create a new note in inbox/ with Obsidian properties.

        Matches exact format used in Nikita's vault:
        - created: ISO timestamp (YYYY-MM-DDTHH:MM)
        - References: source reference
        - Tags: note type (info, idea, action, diary)
        - Links: related notes as [[wikilinks]]
        - Dataview query for backlinks at the bottom

        Args:
            title: Note title (used as filename).
            content: Note body text.
            tag: Note type tag — info, idea, action, diary.
            reference: Source reference (book, video, etc.).
            links: List of related notes (e.g. ["MOC - Obsidian", "MOC - YouTube"]).

        Returns:
            Path to the created note file.
        """
        self._ensure_dirs()

        now = datetime.now()
        created = now.strftime("%Y-%m-%dT%H:%M")

        # Build YAML frontmatter matching vault template
        lines = [
            "---",
            f"created: {created}",
            f"References: {reference}" if reference else "References:",
            "Tags:",
            f"  - {tag}",
            "Links:",
        ]
        if links:
            for link in links:
                lines.append(f'  - "[[{link}]]"')
        lines.append("---")

        frontmatter = "\n".join(lines) + "\n"

        # Dataview backlinks query
        dataview = (
            f'\n\n#### Linked References to "{title}"\n'
            "```dataview\n"
            f'list from [[{title}]]\n'
            "```\n"
        )

        # Sanitize filename
        safe_title = title.replace("/", "-").replace("\\", "-").replace(":", "-")
        filename = f"{safe_title}.md"
        file_path = self.inbox_path / filename

        file_path.write_text(frontmatter + content + dataview, encoding="utf-8")

        self._sync_to_s3(file_path)

        logger.info("Created note: %s", file_path)
        return file_path
