"""Точка входа: создаёт бота и запускает опрос Telegram.

Запуск:
    python bot.py
"""

import asyncio

from aiogram import Bot, Dispatcher

import handlers
import storage
from config import get_token


def create_bot():
    return Bot(get_token())


def create_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.include_router(handlers.router)
    return dispatcher


async def main():
    storage.init_db()
    bot = create_bot()
    dispatcher = create_dispatcher()
    print("Бот запущен. Для остановки нажмите Ctrl+C.")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
