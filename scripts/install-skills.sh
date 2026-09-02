#!/usr/bin/env bash
# Install skills into ~/.cursor/skills for Cursor discovery.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${HOME}/.cursor/skills"
mkdir -p "$DEST"

ln -sfn "$ROOT" "$DEST/pickled-fish"
ln -sfn "$ROOT/skills/wechat-mac-export" "$DEST/wechat-mac-export"
ln -sfn "$ROOT/skills/qingsheng" "$DEST/qingsheng"
ln -sfn "$ROOT/skills/kb-rag" "$DEST/kb-rag"

echo "Linked:"
echo "  $DEST/pickled-fish"
echo "  $DEST/wechat-mac-export"
echo "  $DEST/qingsheng"
echo "  $DEST/kb-rag"
echo "Knowledge packs live under: $ROOT/knowledge/"
echo "Done."
