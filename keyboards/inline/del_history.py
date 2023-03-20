"""Модуль создания клавиатуры."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def callback_del_history() -> InlineKeyboardMarkup:
    """
    Функция создания клавиатуры для модуля 'handlers.custom_handlers.show_history'
    :return: InlineKeyboardMarkup
    """
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Удалить историю запросов", callback_data="del_history")],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data="main_menu")]
    ])

    return ikeyboard
