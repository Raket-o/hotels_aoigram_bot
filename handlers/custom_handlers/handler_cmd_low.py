""" Модуль обработки состояния method_sort_low"""
import logging
import sqlite3
from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from api_requests import get_meta_data
from database import database
from keyboards.inline import main_menu
from loader import bot, dp
from states.contact_information import UserInfoState

logger = logging.getLogger("logger_handler_cmd_low")


REQ_SORT = (
    ("Низкая -> высокая цена", "PRICE_LOW_TO_HIGH"),
    ("Кол-во просмотров", "REVIEW"),
    ("Удалённость от центра", "DISTANCE"),
    ("Звездный рейтинг", "PROPERTY_CLASS"),
    ("Рекомендации", "RECOMMENDED"),
)


@dp.message_handler(state=UserInfoState.method_sort_low)
async def get_met_sort_low(message: types.Message, state: FSMContext) -> None:
    """
    Функция get_met_sort_low. Проверят правильно ли выбран метод сортировки.
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
    logger.info("LOW")

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
                list_hotels = get_meta_data.list_hotels(
                    region_id=data["id_city_area"],
                    check_in=check_in,
                    check_out=check_out,
                    qty_hotels=data["qty_hotels"],
                    adding_to_the_dict=adding_to_the_dict,
                )

                data[
                    "data_check_in"
                ] = f"{check_in.year}-{check_in.month}-{check_in.day}"
                data[
                    "data_check_out"
                ] = f"{check_out.year}-{check_out.month}-{check_out.day}"
                data["list_hotels"] = list_hotels
                print(data)
                try:
                    database.rec_cmd_low(data)
                except sqlite3.OperationalError:
                    logger.error("База данных, либо таблица в ней не найдена")

            for id_hotel in list_hotels:
                (
                    name_hotel,
                    rating_hotel,
                    photo_location,
                    photos,
                ) = get_meta_data.detail_hotel(id_hotel=id_hotel[1])

                str_answer = f"""Название отеля: {name_hotel}
Цена на сутки (за номер): {id_hotel[2]}
Рейгтин: {rating_hotel}"""

                media = [types.InputMediaPhoto(photo_location, str_answer)]

                for i_photo in photos:
                    media.append(types.InputMediaPhoto(i_photo))

                await bot.send_media_group(chat_id=message.chat.id, media=media)

            await message.answer(
                "Запрос выполнен.", reply_markup=main_menu.callback_main_menu()
            )

        except TypeError:
            logger.error("get_met_sort")

            await message.answer(
                "Упс, что-то случилось. Попробуйте снова и введите другой округ",
                reply_markup=main_menu.callback_main_menu(),
            )

    else:
        await message.answer("Некорректный выбор.")
