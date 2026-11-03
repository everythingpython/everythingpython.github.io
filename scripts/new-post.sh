#!/usr/bin/env bash
# Start a new EverythingPython post with zero ceremony:
#   ./scripts/new-post.sh "My post title"
#
# Creates a Hugo page bundle (a folder per post) so images just live next
# to the text: drag an image into the post folder and reference it by
# filename, e.g. ![](diagram.png) — no /assets paths, no code.
# Opens the draft in your editor and starts a live-preview server.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # hugo root = repo root here

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 \"Post title\" [section]   (section defaults to blog)" >&2
  exit 1
fi

TITLE="$1"
SECTION="${2:-blog}"

SLUG="$(printf '%s' "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
[ -n "$SLUG" ] || { echo "Could not make a slug from the title." >&2; exit 1; }

DIR="$ROOT_DIR/content/$SECTION/$SLUG"
FILE="$DIR/index.md"

if [ -e "$DIR" ]; then
  echo "Already exists: $DIR" >&2
  exit 1
fi

mkdir -p "$DIR"
cat > "$FILE" <<EOF
---
title: "$TITLE"
date: $(date +%Y-%m-%d)
tags: []
draft: true
---

EOF

echo "New draft: $FILE"
echo "Drop images into:  $DIR/   and reference them as  ![alt](filename.png)"
echo "Publish it when ready with:  ./scripts/publish.sh $SLUG"

EDITOR_CMD="${EDITOR_CMD:-${VISUAL:-${EDITOR:-open}}}"
$EDITOR_CMD "$FILE" >/dev/null 2>&1 || true

if [ "${NO_PREVIEW:-}" != "1" ]; then
  echo "Starting live preview at http://localhost:1313/  (Ctrl+C to stop)"
  cd "$ROOT_DIR" && exec hugo server -D
fi
