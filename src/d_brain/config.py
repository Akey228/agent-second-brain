"""Application configuration using Pydantic Settings."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_bot_token: str = Field(description="Telegram Bot API token")
    deepgram_api_key: str = Field(description="Deepgram API key for transcription")
    todoist_api_key: str = Field(default="", description="Todoist API key for tasks")
    s3_endpoint: str = Field(default="", description="S3 endpoint URL")
    s3_access_key: str = Field(default="", description="S3 access key ID")
    s3_secret_key: str = Field(default="", description="S3 secret access key")
    s3_bucket: str = Field(default="", description="S3 bucket name")
    vault_path: Path = Field(
        default=Path("./vault"),
        description="Path to Obsidian vault directory",
    )
    allowed_user_ids: list[int] = Field(
        default_factory=list,
        description="List of Telegram user IDs allowed to use the bot",
    )
    allow_all_users: bool = Field(
        default=False,
        description="Whether to allow access to all users (security risk!)",
    )

    @property
    def daily_path(self) -> Path:
        """Path to daily notes directory."""
        return self.vault_path / "daily"

    @property
    def attachments_path(self) -> Path:
        """Path to attachments directory."""
        return self.vault_path / "attachments"

    @property
    def thoughts_path(self) -> Path:
        """Path to thoughts directory."""
        return self.vault_path / "thoughts"

    @property
    def inbox_path(self) -> Path:
        """Path to inbox directory for new notes."""
        return self.vault_path / "1. Inbox"

    @property
    def s3_enabled(self) -> bool:
        """Whether S3 sync is configured."""
        return bool(self.s3_endpoint and self.s3_access_key and self.s3_secret_key and self.s3_bucket)


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
