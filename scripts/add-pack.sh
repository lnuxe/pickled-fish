#!/usr/bin/env bash
# Install a knowledge pack from a git URL or local path into knowledge/custom/<id>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ID="${1:-}"
SRC="${2:-}"
if [[ -z "$ID" || -z "$SRC" ]]; then
  echo "Usage: $0 <pack-id> <git-url-or-local-path>"
  echo "Example: $0 love-skill https://github.com/pajamadot/love-skill"
  exit 1
fi
DEST="$ROOT/knowledge/custom/$ID"
if [[ -e "$DEST" ]]; then
  echo "Destination exists: $DEST"
  exit 1
fi
if [[ -d "$SRC" ]]; then
  cp -R "$SRC" "$DEST"
else
  git clone --depth 1 "$SRC" "$DEST"
  rm -rf "$DEST/.git"
fi
if [[ ! -f "$DEST/PACK.md" ]]; then
  cat > "$DEST/PACK.md" <<EOF
---
id: $ID
name: $ID
license: see upstream
source: $SRC
triggers: []
entry: SKILL.md
---

# PACK: $ID

Auto-added by add-pack.sh. Edit triggers and entry.
EOF
  echo "Wrote stub PACK.md — please edit triggers/entry."
fi
echo "Installed pack at $DEST"
echo "Update knowledge/REGISTRY.md if you want it listed as bundled."
