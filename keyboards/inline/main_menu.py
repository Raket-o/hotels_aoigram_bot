"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def callback_main_menu() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры с каллбэком на возврат главного меню
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")]
    ])

    return ikeyboard
