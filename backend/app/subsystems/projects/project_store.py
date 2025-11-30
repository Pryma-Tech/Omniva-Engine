"""Filesystem-backed project store for the v0.1 backend."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Tuple


def _noop_session_factory() -> None:  # pragma: no cover - placeholder for future DB
    return None


class ProjectStore:
    """Persist simple project metadata as JSON files.

    This is a direct adaptation of the omniva-v2 ProjectStore, with the
    storage base relocated under ``backend/storage/projects_meta`` and
    database hooks stubbed out for future use.
    """

    def __init__(
        self,
        base_path: str | None = None,
        session_factory: Callable[[], Any] | None = None,
    ) -> None:
        if base_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            default_base = os.path.join(base_dir, "..", "..", "storage", "projects_meta")
            self.base = os.path.abspath(default_base)
        else:
            self.base = os.path.abspath(base_path)
        os.makedirs(self.base, exist_ok=True)
        # Maintain compatibility with JSON snapshots while mirroring into SQLite for
        # structured access (the session factory can be replaced with a real DB later).
        storage_root = Path(self.base)
        storage_root.mkdir(parents=True, exist_ok=True)
        self._db_path = storage_root / "projects_meta.sqlite3"
        self._auto_relational = session_factory is None
        self._session_factory: Callable[[], Any] | None = session_factory or self._create_sqlite_factory()
        self._schema_ready = False

    def _create_sqlite_factory(self) -> Callable[[], sqlite3.Connection]:
        db_path = str(self._db_path)

        def _factory() -> sqlite3.Connection:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn

        return _factory

    def _get_session(self):
        """Provide a database session for relational storage."""
        if self._session_factory is None:
            return None
        return self._session_factory()

    def _ensure_schema(self, session: Any) -> None:
        if self._schema_ready or session is None:
            return
        session.execute(
            """
            CREATE TABLE IF NOT EXISTS projects_meta (
                project_id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )
        self._schema_ready = True

    @contextmanager
    def _session_scope(self, session: Any | None) -> Iterator[Tuple[Any | None, bool]]:
        if session is not None:
            self._ensure_schema(session)
            yield session, False
            return
        internal = self._get_session()
        if internal is None:
            yield None, False
            return
        try:
            self._ensure_schema(internal)
            yield internal, True
        finally:
            try:
                internal.close()
            except Exception:
                pass

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def _with_defaults(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        defaults: Dict[str, Any] = {
            "project_id": project_id,
            "id": project_id,
            "creators": [],
            "keywords": [],
            "schedule": {"enabled": False, "cron": "0 */6 * * *"},
            "autonomous": False,
            "shadow_mode": True,
            "daily_limit": 3,
            "auto_publish_mode": "schedule",
            "clips": [],
        }
        merged = {**defaults, **(data or {})}
        merged["project_id"] = project_id
        merged["id"] = merged.get("id", project_id)
        return merged

    def _load_from_json(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._with_defaults(project_id, {})
        with open(path, "r", encoding="utf-8") as project_file:
            raw = json.load(project_file)
        return self._with_defaults(project_id, raw)

    def _relational_fetch(self, project_id: int, session: Any | None) -> Dict[str, Any] | None:
        with self._session_scope(session) as (db, managed):
            if db is None:
                return None
            row = db.execute(
                "SELECT payload FROM projects_meta WHERE project_id = ?",
                (project_id,),
            ).fetchone()
            if managed:
                db.commit()
            if not row:
                return None
            payload = json.loads(row[0] if isinstance(row, tuple) else row["payload"])
            return self._with_defaults(project_id, payload)

    def get(self, project_id: int, session: Any | None = None) -> Dict[str, Any]:
        relational = self._relational_fetch(project_id, session)
        if relational is not None:
            return relational
        return self._load_from_json(project_id)

    def save(self, project_id: int, data: Dict[str, Any], session: Any | None = None) -> Dict[str, Any]:
        payload = self._with_defaults(project_id, data)
        with self._session_scope(session) as (db, managed):
            if db is not None:
                db.execute(
                    """
                    INSERT INTO projects_meta (project_id, payload)
                    VALUES (?, ?)
                    ON CONFLICT(project_id) DO UPDATE SET payload = excluded.payload
                    """,
                    (project_id, json.dumps(payload)),
                )
                if managed:
                    db.commit()
        with open(self._path(project_id), "w", encoding="utf-8") as project_file:
            json.dump(payload, project_file, indent=2)
        return payload

    def list_all(self, session: Any | None = None) -> List[Dict[str, Any]]:
        projects: List[Dict[str, Any]] = []
        with self._session_scope(session) as (db, managed):
            if db is not None:
                rows = db.execute("SELECT project_id, payload FROM projects_meta ORDER BY project_id").fetchall()
                if managed:
                    db.commit()
                if rows:
                    for row in rows:
                        payload = json.loads(row[1] if isinstance(row, tuple) else row["payload"])
                        projects.append(self._with_defaults(row[0], payload))
                    return projects
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            project_id = int(file_name.replace(".json", ""))
            projects.append(self._load_from_json(project_id))
        return projects

    def list_ids(self, session: Any | None = None) -> List[int]:
        with self._session_scope(session) as (db, managed):
            if db is not None:
                rows = db.execute("SELECT project_id FROM projects_meta ORDER BY project_id").fetchall()
                if managed:
                    db.commit()
                if rows:
                    return [row[0] if isinstance(row, tuple) else row["project_id"] for row in rows]
        ids: List[int] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            ids.append(int(file_name.replace(".json", "")))
        return sorted(ids)
