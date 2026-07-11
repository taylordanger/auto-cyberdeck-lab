#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT_DIR"

LOCKDIR="$ROOT_DIR/forge/run.lock"

if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "Forge is already running. Exiting."
  exit 0
fi

trap 'rmdir "$ROOT_DIR/forge/run.lock" 2>/dev/null || true' EXIT

if git rev-parse --verify MERGE_HEAD >/dev/null 2>&1; then
  echo "Resolving unfinished merge state"
  git merge --abort || true
fi

if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || git rev-parse --verify REBASE_HEAD >/dev/null 2>&1; then
  echo "Resolving unfinished rebase state"
  git rebase --abort || true
fi

git checkout ai/m3-worker

if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git pull --rebase --autostash
fi

export OLLAMA_MODEL=${OLLAMA_MODEL:-qwen2.5-coder:14b}
export AUTO_COMMIT=${AUTO_COMMIT:-1}

if [ "${FORGE_SKIP_RUN:-0}" = "1" ]; then
  echo "Skipping forge run because FORGE_SKIP_RUN=1"
  exit 0
fi

nice -n 8 /usr/bin/python3 forge/agent.py

git push -u origin ai/m3-worker
