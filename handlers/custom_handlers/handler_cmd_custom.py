""" Модуль обработки состояния method_sort_custom"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.custom_handlers.filter_amenities import AMENITIES
from handlers.custom_handlers.filter_lodging import LODGING
from handlers.custom_handlers.filter_meal_plan import MEAL_PLAN
from handlers.custom_handlers.filter_star import STAR
from keyboards.reply import list_button
from loader import dp
from states.contact_information import UserInfoState

logger = logging.getLogger("logger_handler_cmd_custom")

REQ_CUSTOM = (
    ("Цена от * до *", "price"),
    ("Питание", "mealPlan"),
    ("Вид жилья", "lodging"),
    ("Особенности", "amenities"),
    ("Звездный рейтинг", "star")
)


@dp.message_handler(state=UserInfoState.method_sort_custom)
async def get_met_sort_custom(message: types.Message, state: FSMContext) -> None:
    """
    Функция get_met_sort_custom. Проверят правильно ли выбран метод сортировки.
    В зависимости от выбранной категории перенаправляет диалог пользователя.
    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    logger.info("CUSTOM")

    example_answer = [i[0] for i in REQ_CUSTOM]

    if message.text in example_answer:
        method_sort, *_ = [i[1] for i in REQ_CUSTOM if i[0] == message.text]

        async with state.proxy() as data:
            data["method_sort_for_history"] = message.text

        if method_sort == "price":
            await message.answer('Введите цену в $ (от ** "пробел" до **).')
            await UserInfoState.set_price.set()

        elif method_sort == "mealPlan":
            kb = list_button.list_button(MEAL_PLAN)
            await message.answer('Выберите рацион.', reply_markup=kb)
            await UserInfoState.set_mealPlan.set()

        elif method_sort == "lodging":
            kb = list_button.list_button(LODGING)
            await message.answer('Выберите вид жилья.', reply_markup=kb)
            await UserInfoState.set_lodging.set()

        elif method_sort == "amenities":
            kb = list_button.list_button(AMENITIES)
            await message.answer('Выберите особенность.', reply_markup=kb)
            await UserInfoState.set_amenities.set()

        elif method_sort == "star":
            kb = list_button.list_button(STAR)
            await message.answer('Выберите звёздность отеля.', reply_markup=kb)
            await UserInfoState.set_star.set()

    else:
        await message.answer('Некорректный выбор.')

