""" Модуль команд "low", "high", "custom"""
import loader
import logging
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
from handlers.custom_handlers import handler_cmd_low, handler_cmd_high, handler_cmd_custom

logger = logging.getLogger("logger_survey")


@dp.message_handler(commands=["low", "high", "custom"])
async def stars_command(message: types.Message, state: FSMContext) -> None:
    """ Функция stars_command. Запускается от команды "low", "high", "custom".
    Записывает в хранилище бота: "user_id", "command", "user_name".
    Вызывается функция get_meta_data.list_country(), которая возвращает список стран.
    Список передаётся функции list_button.list_button(countries), которая возвращает
    клавиатурой с названиями стран. Далее печатает сообщение с этой клавиатурой.
    При окончании лимита или отключение интернета, обрабатывается исключение,
    которое выдаёт сообщение с копкой вернуться в главное меню.

    :param message: types.Message
    :param state: state: FSMContext
    :return: None
    """
    async with state.proxy() as data:
        data["user_id"] = message.from_id
        data["command"] = message.text
        data["user_name"] = message.from_user.first_name
        print(data)

    try:
        countries = get_meta_data.list_country()
        kb = list_button.list_button(countries)
        await message.answer('Введите страну (на английском языке):', reply_markup=kb)
        await UserInfoState.country.set()
        # await UserInfoState.city_area.set()

    except TypeError:
        logger.error("stars_command - You have exceeded the MONTHLY quota for Requests on your current plan, BASIC")
        await message.answer('Упс, что-то случилось. Попробуйте снова и введите другой округ',
                             reply_markup=main_menu.callback_main_menu())


@dp.message_handler(state=UserInfoState.country)
async def get_country(message: types.Message, state: FSMContext) -> None:
    """
    Функций get_country. Проверяет введённое сообщение пользователя.
    Если сообщение содержит только буквы, то записывается в хранилище-бота "country".
    Далее вызывается функция get_meta_data.list_cities(message.text.title()) и передаёт
    в неё название страны, возвращается список городов. После этот список передаётся
    в функцию list_button.list_button(cites), возвращается клавиатура с названиями городов.
    По окончанию печатает текст с клавиатурой, и меняет состояние UserInfoState.city.set().

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    country = message.text.replace(' ', '')
    if country.isalpha():
        async with state.proxy() as data:
            data["country"] = message.text.title()
            print(data)

        cites = get_meta_data.list_cities(message.text.title())
        kb = list_button.list_button(cites)
        await message.answer('Отличный выбор. Записал. Введите город (на английском языке):',
                             reply_markup=kb)
        await UserInfoState.city.set()

    else:
        await message.answer('Название страны может содержать только буквы')


@dp.message_handler(state=UserInfoState.city)
async def get_cities(message: types.Message, state: FSMContext) -> None:
    """
    Функций get_cities. Проверяет введённое сообщение пользователя.
    Если сообщение содержит только буквы, то вызывает функцию
    get_meta_data.list_cities_area(message.text.title()) и передаёт в неё название города,
    возвращается список округов, которые передаются в функцию list_button.list_button(city_area),
    возвращается клавиатура с названиями округов. Печатает сообщение с этой клавиатурой.
    Записывает в хранилище-бота "city", "list_id_city_area" и меняет состояние
    UserInfoState.city_area.set().
    При возращение пустого списка (не удавшемся поиске города) обрабатывается исключение,
    которое выдаёт сообщение с копкой вернуться в главное меню.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    city = message.text.replace(' ', '')
    try:
        if city.isalpha():
            city_area = get_meta_data.list_cities_area(message.text.title())
            kb = list_button.list_button(city_area)
            await message.answer('Отличный выбор. Записал. Введите округ (на английском языке):',
                                 reply_markup=kb)

            async with state.proxy() as data:
                data["city"] = message.text.title()
                data["list_id_city_area"] = city_area
                print(data)

            await UserInfoState.city_area.set()

        else:
            await message.answer('Название города может содержать только буквы')

    except ValueError:
        logger.error("get_cities")
        await message.answer('Упс, что-то случилось. Попробуйте снова и введите другой город',
                             reply_markup=main_menu.callback_main_menu())
        await state.finish()


@dp.message_handler(state=UserInfoState.city_area)
async def get_city_area(message: types.Message, state: FSMContext) -> None:
    """
    Функция get_city_area. По выбранному округу, находит его id.
    Записывается в хранилище бота "city_area", "id_city_area".
    Если id не находится, то выдаёт сообщение с копкой вернуться в главное меню.
    Иначе меняется состояние UserInfoState.qty_hotels.set().

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            id_city_area, *_ = set(i[1] for i in data["list_id_city_area"] if i[0] == message.text)
            data["city_area"] = message.text.title()
            data["id_city_area"] = id_city_area
            print(data)

        if not id_city_area:
            await message.answer('Упс, что-то случилось. Попробуйте снова и введите другой округ',
                                 reply_markup=main_menu.callback_main_menu())

        await UserInfoState.qty_hotels.set()

        await message.answer('Отличный выбор. Записал. Сколько отелей показать (не больше 10)?')

    except ValueError:
        logger.error("get_city_area")
        await message.answer('Упс, что-то случилось. Попробуйте снова и введите другой округ',
                             reply_markup=main_menu.callback_main_menu())


@dp.message_handler(state=UserInfoState.qty_hotels)
async def get_qty_hotels(message: types.Message, state: FSMContext) -> None:
    """
    Функция get_qty_hotels. Пробует перевести введённое сообщение в int.
    При ошибке обрабатывается исключение с кнопкой вернутся в главное меню.
    При успешном переводе в int, проверятся число, чтобы оно входило в диапазон от 1 до 10.
    В зависимости от выбранной категории перенаправляет диалог пользователя

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    async with state.proxy() as data:
        user_cmd = data["command"]

    try:
        qty_hotels = int(message.text)
        if qty_hotels in range(1, 11):

            if user_cmd == "/low":
                logger.info("low")
                kb = list_button.list_button(handler_cmd_low.REQ_SORT)

                await message.answer('Записал. Выберете по какой категории отсортировать отели.',
                                     reply_markup=kb)

                async with state.proxy() as data:
                    data["qty_hotels"] = qty_hotels
                    print(data)

                await UserInfoState.method_sort_low.set()

            elif user_cmd == "/high":
                logger.info("high")
                kb = list_button.list_button(handler_cmd_high.REQ_SORT)

                await message.answer('Записал. Выберете по какой категории отсортировать отели.',
                                     reply_markup=kb)

                async with state.proxy() as data:
                    data["qty_hotels"] = qty_hotels
                    print(data)

                await UserInfoState.method_sort_high.set()

            elif user_cmd == "/custom":
                logger.info("custom")
                kb = list_button.list_button(handler_cmd_custom.REQ_CUSTOM)

                await message.answer('Записал. Выберете по какой категории отфильтровать отели.',
                                     reply_markup=kb)

                async with state.proxy() as data:
                    data["qty_hotels"] = qty_hotels
                    print(data)

                await UserInfoState.method_sort_custom.set()

        else:
            await message.answer('Количество отелей может быть не больше 10.')

    except ValueError:
        logger.error("get_qty_hotels")
        await message.answer('Количество отелей может быть не больше 10.')
