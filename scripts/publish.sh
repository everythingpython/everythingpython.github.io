#!/usr/bin/env bash
# Publish an EverythingPython post: flip it out of draft, commit, and push.
# Pushing triggers the GitHub Action that builds and deploys everythingpython.in.
#
#   ./scripts/publish.sh <slug>
#   ./scripts/publish.sh content/blog/my-post/index.md
#
# Shows what will be committed and asks before pushing.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <slug> [section]   |   $0 <path-to-index.md>" >&2
  exit 1
fi

ARG="$1"
SECTION="${2:-blog}"

# Resolve the post file, whether given a slug (new page-bundle or old flat file) or a path.
if [ -f "$ARG" ]; then
  FILE="$ARG"
elif [ -f "$ROOT_DIR/content/$SECTION/$ARG/index.md" ]; then
  FILE="$ROOT_DIR/content/$SECTION/$ARG/index.md"
elif [ -f "$ROOT_DIR/content/$SECTION/$ARG.md" ]; then
  FILE="$ROOT_DIR/content/$SECTION/$ARG.md"
else
  echo "Can't find that post. Looked in content/$SECTION for a page bundle, a flat .md, or a direct path." >&2
  exit 1
fi

# Page bundle -> stage the folder (text + images). Flat file -> stage the file.
case "$FILE" in
  */index.md) TARGET="$(dirname "$FILE")" ;;
  *)          TARGET="$FILE" ;;
esac
TITLE="$(sed -n -E 's/^title:[[:space:]]*"?([^"]*)"?[[:space:]]*$/\1/p' "$FILE" | head -1)"

if grep -qE '^draft:[[:space:]]*true' "$FILE"; then
  sed -i '' -E 's/^draft:[[:space:]]*true/draft: false/' "$FILE"
  echo "Marked as published (draft: false)."
else
  echo "Already out of draft — committing your latest changes."
fi

cd "$ROOT_DIR"
git add "$TARGET"

if git diff --cached --quiet; then
  echo "Nothing to commit — no changes staged." >&2
  exit 0
fi

echo
echo "About to commit and push:"
git --no-pager diff --cached --stat
echo
printf 'Push and deploy? [y/N] '
read -r REPLY
case "$REPLY" in
  y|Y|yes|Yes) ;;
  *) echo "Left it staged, not pushed. Commit yourself when ready."; exit 0 ;;
esac

git commit -m "Publish: ${TITLE:-$(basename "$TARGET")}"
git push origin HEAD
echo "Pushed. everythingpython.in will rebuild in a minute or two."
