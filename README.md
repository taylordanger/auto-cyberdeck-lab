# Autonomous Server Agent Starter

A small, local-first autonomous coding experiment for a Debian/Ubuntu server or VM with Ollama installed.

The agent talks to a local Ollama model, asks for one small repo improvement, writes files, runs tests, and commits only if checks pass.

## Safety model

- One small task per run.
- Refuses blocked files like `.env`, SSH keys, and token files.
- Maximum 5 files changed per run.
- Runs checks before committing.
- Records decisions in `DECISIONS.md`.
- Records completed changes in `CHANGELOG.md`.
- Intended to run on `ai/autonomous`, not directly on `main`.

## First manual run

```bash
python3 forge/agent.py
```

## Suggested model

```bash
ollama pull qwen2.5-coder:7b
```

## Scheduling

Example systemd files are in `systemd/`. Edit the paths before installing them.
