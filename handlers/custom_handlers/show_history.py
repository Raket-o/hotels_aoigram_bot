""" Модуль отображения истории запросов пользователей."""

import json
from database import database
from aiogram import types
from loader import dp
from keyboards.inline.del_history import callback_del_history


@dp.message_handler(commands=["history"])
async def show_history(message: types.Message) -> None:
    """ Функция show_history. Ид пользователя передаёт в функцию database.seek_history,
    получает строки из базы данной и выводит в сообщение, c двумя кнопками
    (удалить история, вернуться в главное меню)."""
    details_history = database.seek_history(message.from_id)

    for count, row in enumerate(details_history):
        country, city, city_area, list_hotels, method_sort_for_history = row[4:]
        list_hotels = json.loads(list_hotels)

        answer = (f"""<b>Запрос №{count + 1}</b>
<b>Страна-</b> <em>{country}</em>
<b>Город-</b> <em>{city}</em>
<b>Округ-</b> <em>{city_area}</em>
<b>Сортировка-</b> <em>{method_sort_for_history}</em>
<b>Результат поиска отелей:</b>
""")

        result_hotels = ""
        for i_hotel in list_hotels:
            result_hotels += f"<em>{i_hotel[0]}- {i_hotel[2]}</em>\n"

        await message.answer(answer+result_hotels, parse_mode="HTML")

    await message.answer("Запрос выполнен.", reply_markup=callback_del_history())
