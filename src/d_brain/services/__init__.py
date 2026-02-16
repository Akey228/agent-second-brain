"""Business logic services."""

from d_brain.config import Settings
from d_brain.services.storage import VaultStorage


def create_storage(settings: Settings) -> VaultStorage:
    """Create VaultStorage with optional S3 sync."""
    s3 = None
    if settings.s3_enabled:
        from d_brain.services.s3_sync import S3SyncService

        s3 = S3SyncService(
            endpoint=settings.s3_endpoint,
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
            bucket=settings.s3_bucket,
        )
    return VaultStorage(settings.vault_path, s3=s3)
