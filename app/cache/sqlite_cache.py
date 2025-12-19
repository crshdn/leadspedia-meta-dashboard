from __future__ import annotations

import hashlib
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def sha256_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SqliteCache:
    db_path: Path

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
              k TEXT PRIMARY KEY,
              v TEXT NOT NULL,
              created_at INTEGER NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_created ON cache(created_at)")
        conn.commit()
        return conn

    def get(self, key: str, *, ttl_seconds: int) -> Optional[str]:
        now = int(time.time())
        cutoff = now - max(int(ttl_seconds), 0)
        with self._connect() as conn:
            row = conn.execute("SELECT v, created_at FROM cache WHERE k = ?", (key,)).fetchone()
            if not row:
                return None
            v, created_at = row
            if int(created_at) < cutoff:
                conn.execute("DELETE FROM cache WHERE k = ?", (key,))
                conn.commit()
                return None
            return str(v)

    def set(self, key: str, value: str) -> None:
        now = int(time.time())
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache(k, v, created_at) VALUES(?, ?, ?)",
                (key, value, now),
            )
            conn.commit()

    def prune(self, *, max_age_seconds: int) -> int:
        now = int(time.time())
        cutoff = now - max(int(max_age_seconds), 0)
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM cache WHERE created_at < ?", (cutoff,))
            conn.commit()
            return int(cur.rowcount or 0)


