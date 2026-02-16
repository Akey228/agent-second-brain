"""S3 sync service for syncing vault files to S3 (Remotely Save compatible)."""

import logging
from pathlib import Path

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3SyncService:
    """Sync local vault files to S3 bucket used by Remotely Save."""

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
    ) -> None:
        self.bucket = bucket
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=BotoConfig(signature_version="s3v4"),
        )

    def upload_file(self, local_path: Path, vault_path: Path) -> bool:
        """Upload a local file to S3 with its vault-relative path as key.

        Remotely Save uses relative paths from vault root as S3 keys.

        Args:
            local_path: Absolute path to the local file.
            vault_path: Absolute path to the vault root directory.

        Returns:
            True if upload succeeded.
        """
        relative = local_path.relative_to(vault_path)
        key = str(relative)

        try:
            self._client.upload_file(
                str(local_path),
                self.bucket,
                key,
                ExtraArgs={"ContentType": self._guess_content_type(key)},
            )
            logger.info("Uploaded %s to s3://%s/%s", local_path, self.bucket, key)
            return True
        except ClientError:
            logger.exception("Failed to upload %s", key)
            return False

    def upload_bytes(self, data: bytes, key: str) -> bool:
        """Upload raw bytes to S3.

        Args:
            data: File content.
            key: S3 key (vault-relative path).

        Returns:
            True if upload succeeded.
        """
        try:
            self._client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType=self._guess_content_type(key),
            )
            logger.info("Uploaded bytes to s3://%s/%s", self.bucket, key)
            return True
        except ClientError:
            logger.exception("Failed to upload bytes to %s", key)
            return False

    def file_exists(self, key: str) -> bool:
        """Check if a file exists in S3."""
        try:
            self._client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    @staticmethod
    def _guess_content_type(key: str) -> str:
        if key.endswith(".md"):
            return "text/markdown"
        if key.endswith(".json"):
            return "application/json"
        if key.endswith(".jpg") or key.endswith(".jpeg"):
            return "image/jpeg"
        if key.endswith(".png"):
            return "image/png"
        return "application/octet-stream"
