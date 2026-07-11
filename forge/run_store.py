"""Persistent storage for autonomous forge runs."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DATABASE_PATH = Path(__file__).with_name("forge.db")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunStore:
    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = WAL")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT NOT NULL,
                    branch TEXT,
                    task_summary TEXT,
                    model_summary TEXT,
                    test_command TEXT,
                    test_return_code INTEGER,
                    stdout TEXT,
                    stderr TEXT,
                    commit_hash TEXT,
                    parent_run_id INTEGER,
                    FOREIGN KEY (parent_run_id) REFERENCES runs(id)
                );

                CREATE TABLE IF NOT EXISTS run_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    path TEXT NOT NULL,
                    change_type TEXT,
                    diff_text TEXT,
                    FOREIGN KEY (run_id) REFERENCES runs(id)
                );

                CREATE TABLE IF NOT EXISTS run_errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    error_type TEXT,
                    message TEXT NOT NULL,
                    traceback TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (run_id) REFERENCES runs(id)
                );

                CREATE TABLE IF NOT EXISTS agent_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def start_run(
        self,
        *,
        branch: str,
        task_summary: str | None = None,
        parent_run_id: int | None = None,
    ) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO runs (
                    started_at,
                    status,
                    branch,
                    task_summary,
                    parent_run_id
                )
                VALUES (?, 'starting', ?, ?, ?)
                """,
                (
                    utc_now(),
                    branch,
                    task_summary,
                    parent_run_id,
                ),
            )

            return int(cursor.lastrowid)

    def update_run(self, run_id: int, **fields: Any) -> None:
        allowed = {
            "finished_at",
            "status",
            "task_summary",
            "model_summary",
            "test_command",
            "test_return_code",
            "stdout",
            "stderr",
            "commit_hash",
        }

        invalid = set(fields) - allowed
        if invalid:
            raise ValueError(f"Unsupported run fields: {sorted(invalid)}")

        if not fields:
            return

        assignments = ", ".join(f"{field} = ?" for field in fields)
        values = list(fields.values()) + [run_id]

        with self.connect() as connection:
            connection.execute(
                f"UPDATE runs SET {assignments} WHERE id = ?",
                values,
            )

    def finish_run(
        self,
        run_id: int,
        *,
        status: str,
        test_return_code: int | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
    ) -> None:
        self.update_run(
            run_id,
            finished_at=utc_now(),
            status=status,
            test_return_code=test_return_code,
            stdout=stdout,
            stderr=stderr,
        )

    def record_error(
        self,
        run_id: int,
        *,
        message: str,
        error_type: str | None = None,
        traceback_text: str | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO run_errors (
                    run_id,
                    error_type,
                    message,
                    traceback,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    error_type,
                    message,
                    traceback_text,
                    utc_now(),
                ),
            )

    def record_file(
        self,
        run_id: int,
        *,
        path: str,
        change_type: str | None = None,
        diff_text: str | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO run_files (
                    run_id,
                    path,
                    change_type,
                    diff_text
                )
                VALUES (?, ?, ?, ?)
                """,
                (run_id, path, change_type, diff_text),
            )

    def set_state(self, key: str, value: Any) -> None:
        encoded = json.dumps(value)

        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO agent_state (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (key, encoded, utc_now()),
            )

    def get_state(self, key: str, default: Any = None) -> Any:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT value FROM agent_state WHERE key = ?",
                (key,),
            ).fetchone()

        if row is None:
            return default

        return json.loads(row["value"])

    def get_unfinished_run(self) -> sqlite3.Row | None:
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT *
                FROM runs
                WHERE status IN (
                    'starting',
                    'planning',
                    'implementing',
                    'testing',
                    'reviewing',
                    'repair_required'
                )
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()