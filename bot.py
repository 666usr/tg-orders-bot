"""Точка входа: создаёт бота и запускает опрос Telegram.

Запуск:
    .\\.venv\\Scripts\\python.exe bot.py
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import (
    TelegramConflictError,
    TelegramNetworkError,
    TelegramUnauthorizedError,
)

import handlers
import storage
from config import get_token


def create_bot():
    return Bot(get_token())


def create_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.include_router(handlers.router)
    return dispatcher


async def run():
    storage.init_db()

    try:
        bot = create_bot()
    except RuntimeError as error:
        print("Ошибка настройки: " + str(error))
        return

    # Проверяем токен и соединение с Telegram.
    try:
        me = await bot.get_me()
    except TelegramUnauthorizedError:
        print("Telegram отклонил токен. Проверь значение BOT_TOKEN в файле .env.")
        await bot.session.close()
        return
    except TelegramNetworkError:
        print(
            "Не удалось соединиться с Telegram (api.telegram.org).\n"
            "Проверь интернет, VPN или файрвол - возможно, доступ к Telegram "
            "заблокирован в этой сети. Попробуй другую сеть (например, мобильный интернет)."
        )
        await bot.session.close()
        return

    username = me.username or "?"
    print("Бот @" + username + " (" + me.full_name + ") запущен.")
    print("Открой в Telegram: https://t.me/" + username)
    print("Для остановки нажмите Ctrl+C.")

    dispatcher = create_dispatcher()
    try:
        await dispatcher.start_polling(bot)
    except TelegramConflictError:
        print(
            "Конфликт: этот токен уже используется другим запущенным ботом. "
            "Закрой лишние окна с ботом и запусти заново."
        )
    except TelegramNetworkError:
        print("Соединение с Telegram прервалось. Проверь интернет и запусти бота снова.")
    finally:
        await bot.session.close()


def main():
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Бот остановлен.")


if __name__ == "__main__":
    main()
