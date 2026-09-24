"""Кнопки бота.

Клавиатуры вынесены отдельно, чтобы меню можно было менять в одном месте.
"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_menu():
    """Главное меню бота."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Услуги"), KeyboardButton(text="Оставить заявку")],
            [KeyboardButton(text="Контакты")],
        ],
        resize_keyboard=True,
    )


def cancel_keyboard():
    """Клавиатура на время заполнения заявки."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отменить")]],
        resize_keyboard=True,
    )


STATUSES = ["новая", "в работе", "закрыта"]


def status_keyboard(order_id):
    """Кнопки смены статуса для одной заявки (для админа)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=status,
                    callback_data="status:" + str(order_id) + ":" + status,
                )
            ]
            for status in STATUSES
        ]
    )
