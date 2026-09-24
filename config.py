"""Настройки бота.

Токен и список администраторов читаются из переменных окружения.
Обычно они лежат в файле .env рядом с проектом (он не попадает в git!).
"""

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # Если python-dotenv не установлен, просто читаем переменные окружения.
    pass


def get_token():
    """Возвращает токен бота или понятно ругается, если его нет."""
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Не задан BOT_TOKEN. Создай файл .env по образцу .env.example "
            "и впиши токен, который выдал @BotFather."
        )
    return token


def get_admin_ids():
    """Возвращает список id администраторов (из переменной ADMIN_IDS)."""
    raw = os.environ.get("ADMIN_IDS", "")
    ids = []
    for part in raw.split(","):
        part = part.strip()
        if part:
            try:
                ids.append(int(part))
            except ValueError:
                pass
    return ids
