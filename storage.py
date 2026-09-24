"""Хранение заявок в базе SQLite.

Специально вынесено отдельно от бота: так эту часть можно тестировать
без Telegram и без токена.
"""

import sqlite3
from contextlib import closing
from datetime import datetime

DEFAULT_DB = "orders.db"


def connect(db_path=None):
    """Открывает соединение с базой (по умолчанию orders.db)."""
    connection = sqlite3.connect(db_path or DEFAULT_DB)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path=None):
    """Создаёт таблицу заявок, если её ещё нет."""
    with closing(connect(db_path)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                contact TEXT,
                description TEXT,
                status TEXT DEFAULT 'новая',
                created_at TEXT
            )
            """
        )
        connection.commit()


def add_order(user_id, username, name, contact, description, db_path=None):
    """Добавляет заявку и возвращает её номер."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with closing(connect(db_path)) as connection:
        cursor = connection.execute(
            "INSERT INTO orders "
            "(user_id, username, name, contact, description, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'новая', ?)",
            (user_id, username, name, contact, description, created_at),
        )
        connection.commit()
        return cursor.lastrowid


def list_orders(db_path=None, limit=20):
    """Возвращает последние заявки (сначала новые)."""
    with closing(connect(db_path)) as connection:
        cursor = connection.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]


def count_orders(db_path=None):
    """Возвращает общее число заявок."""
    with closing(connect(db_path)) as connection:
        cursor = connection.execute("SELECT COUNT(*) AS n FROM orders")
        return cursor.fetchone()["n"]


def get_order(order_id, db_path=None):
    """Возвращает одну заявку по номеру (или None)."""
    with closing(connect(db_path)) as connection:
        cursor = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        return dict(row) if row is not None else None


def update_status(order_id, status, db_path=None):
    """Меняет статус заявки. Возвращает число изменённых строк (0 или 1)."""
    with closing(connect(db_path)) as connection:
        cursor = connection.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
        )
        connection.commit()
        return cursor.rowcount
