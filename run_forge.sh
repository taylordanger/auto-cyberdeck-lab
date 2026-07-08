#!/bin/zsh
set -e

cd /Users/darkstar/Downloads/autonomous-server-agent-starter

git checkout ai/m3-worker

if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git pull --rebase --autostash
fi

export OLLAMA_MODEL=qwen2.5-coder:7b
export AUTO_COMMIT=1

nice -n 15 /usr/bin/python3 forge/agent.py

git push -u origin ai/m3-worker
