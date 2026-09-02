#!/usr/bin/env bash
# Install skills into ~/.cursor/skills for Cursor discovery.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${HOME}/.cursor/skills"
mkdir -p "$DEST"

ln -sfn "$ROOT" "$DEST/mac-wechat-coach"
ln -sfn "$ROOT/skills/wechat-mac-export" "$DEST/wechat-mac-export"
ln -sfn "$ROOT/skills/qingsheng" "$DEST/qingsheng"

echo "Linked:"
echo "  $DEST/mac-wechat-coach"
echo "  $DEST/wechat-mac-export"
echo "  $DEST/qingsheng"
echo "Done. Restart or refresh Cursor Agent skills if needed."
