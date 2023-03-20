""" Модуль обработки команды 'start' """

from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext


START_MESSAGE = """<b>/low</b> - <em>Запросить минимальные значения.</em>
<b>/high</b> - <em>Запросить максимальные значения.</em>
<b>/custom</b> - <em>Отфильтровать по значениям.</em>
<b>/history</b> -  <em>Узнать историю запросов.</em>
<b>/help</b> -  <em>Описание команд.</em>
"""


@dp.message_handler(commands=["start"])
async def stars_command(message: types.Message) -> None:
    """ Функция stars_command. Обрабатывает команду 'start' """
    await message.answer(START_MESSAGE, parse_mode="HTML")
