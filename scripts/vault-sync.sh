#!/bin/bash
set -e

# Vault <-> S3 sync script
# Only syncs Obsidian content, excludes server-only files

export HOME="${HOME:-/home/$(whoami)}"
PROJECT_DIR="${PROJECT_DIR:-$HOME/projects/agent-second-brain}"
VAULT_DIR="$PROJECT_DIR/vault"
ENV_FILE="$PROJECT_DIR/.env"

# Load env
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# S3 config
S3_ENDPOINT="https://s3.regru.cloud"
S3_BUCKET="s3://akey-core"
export AWS_ACCESS_KEY_ID="LC0XBEHJ4B6A0B208Y0X"
export AWS_SECRET_ACCESS_KEY="zduPin99NY31J6qFhc0JIQGnI67XZD4vDGwW9MRU"

# Files/dirs to EXCLUDE from sync (server-only, not Obsidian content)
EXCLUDES=(
    "--exclude" ".claude/*"
    "--exclude" ".sessions/*"
    "--exclude" ".obsidian/*"
    "--exclude" "MEMORY.md"
    "--exclude" "CLAUDE.md"
    "--exclude" "memory/*"
    "--exclude" ".gitkeep"
    "--exclude" ".git/*"
    "--exclude" "*.credentials*"
    "--exclude" "s3-regru-credentials*"
)

ACTION="${1:-pull}"

case "$ACTION" in
    pull)
        echo "=== Pulling from S3 to vault ==="
        aws --endpoint-url "$S3_ENDPOINT" s3 sync "$S3_BUCKET/" "$VAULT_DIR/" --delete "${EXCLUDES[@]}"
        echo "=== Pull complete ==="
        ;;
    push)
        echo "=== Pushing vault to S3 ==="
        aws --endpoint-url "$S3_ENDPOINT" s3 sync "$VAULT_DIR/" "$S3_BUCKET/" --delete "${EXCLUDES[@]}"
        echo "=== Push complete ==="
        ;;
    *)
        echo "Usage: $0 [pull|push]"
        echo "  pull - download S3 content to vault (default)"
        echo "  push - upload vault content to S3"
        exit 1
        ;;
esac
