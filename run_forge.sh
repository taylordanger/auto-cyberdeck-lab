#!/bin/zsh
set -e
cd /Users/darkstar/downloads/autonomous-server-agent-starter

export OLLAMA_MODEL=qwen2.5-coder:7b
export AUTO_COMMIT=1

/usr/bin/python3 forge/agent.py

git push
