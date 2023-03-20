""" Модуль обработки каллбэка с датой del_history"""
from aiogram import types
from loader import dp
from database.database import delete_history_db


@dp.callback_query_handler(lambda callback_query: callback_query.data == "del_history")
async def delete_history(callback: types.CallbackQuery) -> None:
    """
    Функия delete_history. Передаёт user.id в функцию delete_history_db
    для поиска и удаления строк из бд.
    """
    delete_history_db(callback.from_user.id)
    await callback.answer(text="История удалена")
