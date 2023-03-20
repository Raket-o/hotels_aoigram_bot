"""Модуль хранения данных (состояний) пользователя"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInfoState(StatesGroup):
    """ Класс UserInfoState. Хранит состояние, информацию и данные вводимые пользователем"""
    user_id = State()
    user_name = State()
    country = State()
    city = State()
    city_area = State()
    id_city_area = State()
    list_city_area = State()
    qty_hotels = State()
    id_hotels = State()
    list_id_hotels = State()
    data_check_in = State()
    data_check_out = State()
    command = State()
    method_sort = State()
    method_sort_for_history = State()
    method_sort_low = State()
    method_sort_high = State()
    method_sort_custom = State()
    custom_filter = State()
    set_price = State()
    set_mealPlan = State()
    set_lodging = State()
    set_amenities = State()
    set_star = State()
