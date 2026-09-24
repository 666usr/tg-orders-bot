"""Обработчики сообщений и кнопок.

Логика бота: старт, меню, приём заявки по шагам (FSM), админ-просмотр.
"""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import keyboards
import storage
from config import get_admin_ids

router = Router()


class OrderForm(StatesGroup):
    """Шаги заполнения заявки."""

    name = State()
    contact = State()
    description = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здравствуйте! Это бот приёма заявок.\n"
        "Выберите действие на клавиатуре ниже.",
        reply_markup=keyboards.main_menu(),
    )


@router.message(F.text == "Услуги")
async def services(message: Message):
    await message.answer(
        "Мы делаем:\n"
        "1. Telegram-ботов\n"
        "2. Автоматизацию отчётов\n"
        "3. Сбор данных с сайтов\n\n"
        "Чтобы оставить заявку, нажмите «Оставить заявку».",
        reply_markup=keyboards.main_menu(),
    )


@router.message(F.text == "Контакты")
async def contacts(message: Message):
    await message.answer(
        "Связаться с нами: @your_username\n"
        "Телефон: +7 000 000-00-00",
        reply_markup=keyboards.main_menu(),
    )


@router.message(F.text == "Отменить")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Действие отменено. Вы в главном меню.",
        reply_markup=keyboards.main_menu(),
    )


@router.message(F.text == "Оставить заявку")
async def order_start(message: Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer(
        "Как вас зовут? (или нажмите «Отменить»)",
        reply_markup=keyboards.cancel_keyboard(),
    )


@router.message(OrderForm.name)
async def order_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое. Напишите, пожалуйста, ещё раз.")
        return
    await state.update_data(name=name)
    await state.set_state(OrderForm.contact)
    await message.answer(
        "Как с вами связаться? (телефон, почта или @username)",
        reply_markup=keyboards.cancel_keyboard(),
    )


@router.message(OrderForm.contact)
async def order_contact(message: Message, state: FSMContext):
    contact = message.text.strip()
    if len(contact) < 3:
        await message.answer("Контакт слишком короткий. Напишите, пожалуйста, ещё раз.")
        return
    await state.update_data(contact=contact)
    await state.set_state(OrderForm.description)
    await message.answer(
        "Опишите задачу в паре предложений.",
        reply_markup=keyboards.cancel_keyboard(),
    )


@router.message(OrderForm.description)
async def order_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    order_id = storage.add_order(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        name=data.get("name", ""),
        contact=data.get("contact", ""),
        description=message.text.strip(),
    )

    await message.answer(
        "Спасибо! Заявка №" + str(order_id) + " принята. Мы свяжемся с вами.",
        reply_markup=keyboards.main_menu(),
    )

    text = (
        "Новая заявка №" + str(order_id) + "\n"
        "Имя: " + data.get("name", "") + "\n"
        "Контакт: " + data.get("contact", "") + "\n"
        "Задача: " + message.text.strip()
    )
    for admin_id in get_admin_ids():
        try:
            await message.bot.send_message(admin_id, text)
        except Exception:
            # Если админ не начал диалог с ботом, отправка не пройдёт - это ок.
            pass


@router.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id not in get_admin_ids():
        await message.answer("Команда доступна только администратору.")
        return

    orders = storage.list_orders(limit=10)
    if not orders:
        await message.answer("Заявок пока нет.")
        return

    blocks = []
    for order in orders:
        blocks.append(
            "№" + str(order["id"]) + " · " + order["status"] + " · " + order["created_at"] + "\n"
            + order["name"] + " · " + order["contact"] + "\n"
            + order["description"]
        )
    await message.answer("Последние заявки:\n\n" + "\n\n".join(blocks))
