#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORGE = ROOT / "forge"
STATE = FORGE / "state.json"
POLICY = FORGE / "policy.md"
DECISIONS = ROOT / "DECISIONS.md"
CHANGELOG = ROOT / "CHANGELOG.md"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
AUTO_COMMIT = os.environ.get("AUTO_COMMIT", "1") == "1"
MAX_FILES = 5
MAX_FILE_CHARS = 30000

BLOCKED_EXACT = {".env", ".git/config"}
BLOCKED_PARTS = {".git", ".ssh", "__pycache__"}
BLOCKED_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}


def read(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(cmd: list[str], check: bool = False, timeout: int = 120):
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check, timeout=timeout)


def sh(command: str, timeout: int = 300):
    blocked = ["rm -rf", "sudo ", "curl ", "wget ", "ssh ", "scp ", "dd ", "mkfs", "chmod 777"]
    if any(x in command.lower() for x in blocked):
        raise ValueError(f"Blocked command: {command}")
    return subprocess.run(command, cwd=ROOT, shell=True, text=True, capture_output=True, timeout=timeout)


def load_state() -> dict[str, Any]:
    try:
        return json.loads(read(STATE, "{}"))
    except json.JSONDecodeError:
        return {"version": 1, "runs": 0, "consecutive_failures": 0}


def save_state(state: dict[str, Any]) -> None:
    write(STATE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def files_list() -> str:
    out = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if p.is_file():
            out.append(str(rel))
    return "\n".join(sorted(out))


def git_log() -> str:
    r = run(["git", "log", "--oneline", "-8"], timeout=20)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else "(no git history yet)"


def git_status() -> str:
    r = run(["git", "status", "--short"], timeout=20)
    return r.stdout.strip()


def safe_path(rel: str) -> Path:
    if rel in BLOCKED_EXACT:
        raise ValueError(f"Blocked path: {rel}")
    p = Path(rel)
    if p.is_absolute():
        raise ValueError(f"Absolute path blocked: {rel}")
    if any(part in BLOCKED_PARTS for part in p.parts):
        raise ValueError(f"Blocked path component: {rel}")
    if p.suffix in BLOCKED_SUFFIXES:
        raise ValueError(f"Blocked sensitive suffix: {rel}")
    resolved = (ROOT / p).resolve()
    if not str(resolved).startswith(str(ROOT.resolve())):
        raise ValueError(f"Path escapes repo: {rel}")
    return resolved


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").replace("json\n", "", 1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in model output")
        return json.loads(text[start:end + 1])


def ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_ctx": 8192},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read().decode())
    return data.get("response", "")


def prompt() -> str:
    state = load_state()
    return f"""
You are a local autonomous coding agent maintaining this repository.

Follow this policy exactly:

{read(POLICY)}

Repository files:

{files_list()}

Recent git log:

{git_log()}

Current git status:

{git_status() or '(clean)'}

ROADMAP.md:

{read(ROOT / 'ROADMAP.md')[-4000:]}

Recent DECISIONS.md:

{read(DECISIONS)[-5000:]}

Recent CHANGELOG.md:

{read(CHANGELOG)[-3000:]}

STATE:

{json.dumps(state, indent=2)}

Choose one small useful task.

Return JSON only. No markdown. No explanation outside JSON.

Required shape:
{{
  "summary": "one sentence summary",
  "files": [
    {{"path": "relative/path.txt", "content": "full new file content"}}
  ],
  "test_command": "python3 -m compileall .",
  "commit_message": "short commit message"
}}

Important:
- Include full file content for every file you edit.
- Do not edit more than {MAX_FILES} files.
- Keep files reasonably small.
- Always update DECISIONS.md.
- Update CHANGELOG.md if you made a meaningful change.
"""


def apply_plan(plan: dict[str, Any]) -> list[str]:
    items = plan.get("files", [])
    if not isinstance(items, list):
        raise ValueError("files must be a list")
    if len(items) > MAX_FILES:
        raise ValueError(f"Too many files: {len(items)}")
    changed = []
    for item in items:
        rel = item.get("path")
        content = item.get("content")
        if not isinstance(rel, str) or not isinstance(content, str):
            raise ValueError("Each file needs string path and content")
        if len(content) > MAX_FILE_CHARS:
            raise ValueError(f"File too large: {rel}")
        write(safe_path(rel), content)
        changed.append(rel)
    return changed


def fail_note(reason: str) -> None:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    old = read(DECISIONS)
    write(DECISIONS, old + f"\n\n## {now}\n\nAutonomous run failed before commit.\n\n```text\n{reason[-3000:]}\n```\n")


def commit(message: str) -> None:
    if not AUTO_COMMIT:
        print("AUTO_COMMIT=0, leaving changes uncommitted.")
        return
    if not git_status():
        print("No changes to commit.")
        return
    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", message[:120] or "autonomous update"], check=True)
    print("Committed changes.")


def main() -> int:
    state = load_state()
    state["runs"] = int(state.get("runs", 0)) + 1
    state["last_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_state(state)

    if int(state.get("consecutive_failures", 0)) >= 3:
        print("Refusing to run: 3 consecutive failures. Reset forge/state.json after review.")
        return 2

    try:
        plan = extract_json(ollama(prompt()))
        print("Model summary:", plan.get("summary", "(none)"))
        changed = apply_plan(plan)
        print("Changed files:", ", ".join(changed) if changed else "(none)")
        test_command = str(plan.get("test_command") or "python3 -m compileall .")
        result = sh(test_command)
        print("Test command:", test_command)
        print("Test return code:", result.returncode)
        if result.stdout:
            print(result.stdout[-3000:])
        if result.stderr:
            print(result.stderr[-3000:])
        if result.returncode != 0:
            raise RuntimeError("Tests/checks failed; refusing to commit.")
        state["consecutive_failures"] = 0
        state["last_summary"] = str(plan.get("summary", ""))
        state["last_finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        save_state(state)
        commit(str(plan.get("commit_message") or "autonomous update"))
        return 0
    except Exception as exc:
        state["consecutive_failures"] = int(state.get("consecutive_failures", 0)) + 1
        state["last_error"] = str(exc)
        state["last_finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        save_state(state)
        fail_note(str(exc))
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
