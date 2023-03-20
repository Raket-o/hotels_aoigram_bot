""" Модуль обработки состояния method_sort_high"""

import loader
import logging
import sqlite3
from aiogram import types
from loader import dp
from states.contact_information import UserInfoState
from api_requests import get_meta_data
from keyboards.reply import list_button
from aiogram.dispatcher import FSMContext
from database import database
from datetime import date, timedelta
from keyboards.inline import main_menu
from loader import bot


logger = logging.getLogger("logger_handler_cmd_high")

REQ_SORT = (
    ("Высокая -> низкая цена", "PRICE_LOW_TO_HIGH"),
    ("Кол-во просмотров", "REVIEW"),
    ("Удалённость от центра", "DISTANCE"),
    ("Звездный рейтинг", "PROPERTY_CLASS"),
    ("Рекомендации", "RECOMMENDED")
)


@dp.message_handler(state=UserInfoState.method_sort_high)
async def get_met_sort_high(message: types.Message, state: FSMContext) -> None:
    """
    Функция get_met_sort_high. Проверят правильно ли выбран метод сортировки.
    Записывает в хранилище-бота "method_sort", "data_check_in", "data_check_out"
    "data_check_in", "data_check_out", "list_hotels". Вызывается функцию
    get_meta_data.list_hotels, Проходя циклом по листу отелей, передаёт
    их id в функцию get_meta_data.detal_hotel(id_hotel=id_hotel[1]),
    получая name_hotel- имя отеля, rating_hotel- рейтинг отеля,
    photo_location - URL фото с локацией, photos - URL фотографий отеля.
    Создаёт список с InputMediaPhoto и выводит всю информацию пользователю.
    При успешном выполнении запроса печатает сообщение с кнопкой
    возврат в главное меню.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    logger.info("HIGH")

    example_answer = [i[0] for i in REQ_SORT]

    if message.text in example_answer:
        method_sort, *_ = [i[1] for i in REQ_SORT if i[0] == message.text]
        check_in = date.today()
        check_out = date.today() + timedelta(days=7)
        adding_to_the_dict = {"sort": method_sort}

        try:
            async with state.proxy() as data:
                data["method_sort_for_history"] = message.text
                data["method_sort"] = method_sort
                data["data_check_in"] = check_in
                data["data_check_out"] = check_out
                qty_hotels=data["qty_hotels"]
                data["list_hotels"] = list_hotels = get_meta_data.list_hotels(region_id=data["id_city_area"],
                                                        check_in=check_in,
                                                        check_out=check_out,
                                                        qty_hotels=200,
                                                        adding_to_the_dict=adding_to_the_dict)[::-1][:qty_hotels]

                data["data_check_in"] = f"{check_in.year}-{check_in.month}-{check_in.day}"
                data["data_check_out"] = f"{check_out.year}-{check_out.month}-{check_out.day}"

                print(data)
                try:
                    database.rec_cmd_low(data)
                except sqlite3.OperationalError:
                    logger.error("База данных, либо таблица в ней не найдена")

            count = 0
            for id_hotel in list_hotels:
                if count == qty_hotels:
                    break
                name_hotel, rating_hotel, photo_location, photos = get_meta_data.detail_hotel(id_hotel=id_hotel[1])

                str_answer = f"""Название отеля: {name_hotel}
Цена на сутки (за номер): {id_hotel[2]}
Рейгтин: {rating_hotel}"""

                media = [types.InputMediaPhoto(photo_location, str_answer)]

                for i_photo in photos:
                    media.append(types.InputMediaPhoto(i_photo))

                await bot.send_media_group(chat_id=message.chat.id, media=media)
                count += 1

            await message.answer('Запрос выполнен.', reply_markup=main_menu.callback_main_menu())

        except TypeError:
            logger.error("get_met_sort")

            await message.answer('Упс, что-то случилось. Попробуйте снова и введите другой округ',
                                 reply_markup=main_menu.callback_main_menu())

    else:
        await message.answer('Некорректный выбор.')