"""Кнопки бота.

Клавиатуры вынесены отдельно, чтобы меню можно было менять в одном месте.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    """Главное меню бота."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Услуги"), KeyboardButton(text="Оставить заявку")],
            [KeyboardButton(text="Контакты")],
        ],
        resize_keyboard=True,
    )
