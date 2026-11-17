import os
import sqlite3
from typing import Any, Dict, List

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def is_registered(telegram_id: int) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()
        return row is not None


def save_user(data: Dict[str, Any]) -> bool:
    with get_connection() as conn:
        try:
            conn.execute(
                """
                INSERT INTO users (telegram_id, username, full_name, age, phone, address, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["telegram_id"],
                    data.get("username"),
                    data["full_name"],
                    data["age"],
                    data["phone"],
                    data["address"],
                    data["created_at"],
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            return False


def get_users_count() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
        return int(row[0]) if row else 0


def get_users_page(page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
    offset = (page - 1) * page_size
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT telegram_id, username, full_name, age, phone, address, created_at
            FROM users
            ORDER BY id ASC
            LIMIT ? OFFSET ?
            """,
            (page_size, offset),
        ).fetchall()
        return [dict(row) for row in rows]


def get_all_registered_users() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT telegram_id, username, full_name, age, phone, address, created_at FROM users ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]
