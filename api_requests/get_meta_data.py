""" Модуль запросов информации по отелям"""
import sqlite3
import json
import re
import logging
from typing import List, Tuple, Any
from config_data import config
from datetime import date, timedelta
from requests import request


URL_COUNTRY = "https://hotels4.p.rapidapi.com/get-meta-data"
URL_CITIES = "https://hotels4.p.rapidapi.com/locations/search"
URL_CITY_AREA = "https://hotels4.p.rapidapi.com/locations/v2/search"
URL_HOTELS = "https://hotels4.p.rapidapi.com/properties/v2/list"
URL_DETAL_HOTEL = "https://hotels4.p.rapidapi.com/properties/v2/detail"

logger = logging.getLogger("logger_get_meta_data")


def list_country() -> List[Tuple[str, int]]:
    """
    Функция list_country. Делает запрос и парсит список стран.
    :return: Список[кортеж[название страны | 0]] - в кортеже второй элемент обязателен,
            для функции создания кнопок
    """
    response = request("GET", URL_COUNTRY, headers=config.HAEDERS_RAPID, timeout=1000)

    data = json.loads(response.text)
    print(data)
    lst_country = [(i_country["name"], 0)
                   for i_country in data
                   if not re.findall(r'_', i_country["name"])]
    lst_country.append(("AMERICA", 0))

    return lst_country


def list_cities(user_country: str = None) -> List[Tuple[str, int]]:
    """
    Функция list_country. Принимает на вход название страну. Делает запрос и парсит список городов.
    :return: Кортеж[кортеж[название города, ид_города]]
    """
    querystring = {"query": user_country, "locale": "en_EN"}
    response = request("GET", URL_CITIES, headers=config.HAEDERS_RAPID, params=querystring, timeout=1000)
    data = json.loads(response.text)

    lst_city = []
    country = str(data['term'])
    if data['suggestions'][0]['group'] == 'CITY_GROUP':
        lst_city = tuple((i_city['name'], i_city['destinationId'])
                         for i_city in data['suggestions'][0]['entities']
                         if country.capitalize() in i_city['caption'])

    return lst_city


def list_cities_area(user_city: str = None) -> Tuple[Tuple[str, int]]:
    """
    Функция list_cities_area. Принимет на вход название города. Делает запрос и парсит список округов.
    :return: Кортеж[кортеж[название округа, ид_округа]]
    """
    querystring = {"query": user_city, "locale": "en_US", "currency": "USD"}
    response = request("GET", URL_CITY_AREA, headers=config.HAEDERS_RAPID, params=querystring, timeout=1000)
    data = json.loads(response.text)

    lst_city_area = tuple((j["name"], j["geoId"])
                          for i in data["suggestions"]
                          for j in i["entities"])

    return lst_city_area


def list_hotels(region_id: int,
                check_in: date,
                check_out: date,
                qty_hotels: int,
                adding_to_the_dict: dict) -> List[Tuple[Any, Any, str | Any]]:
    """
    Функция list_hotels. Принимет на вход ид_округа, дату заезда, дату выезда,
    метод сортировки и кол-во отелей которые нужно вывести.
    Делает запрос и парсит список отелей.
    :return: Кортеж[кортеж[название отеля, ид_отеля, стоимость номера за сутки]]
    """

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": check_in.day,
            "month": check_in.month,
            "year": check_in.year
        },
        "checkOutDate": {
            "day": check_out.day,
            "month": check_out.month,
            "year": check_out.year
        },
        "rooms": [
            {
                "adults": 1,
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": qty_hotels,
    }

    payload.update(adding_to_the_dict)

    response = request("POST", URL_HOTELS, json=payload, headers=config.HAEDERS_RAPID, timeout=1000)
    data = json.loads(response.text)

    print(data)

    lts_hotels = []
    for i in data["data"]["propertySearch"]["properties"]:
        name = i["name"]
        id_hotel = i["id"]
        try:
            price = i["price"]["options"][0]["formattedDisplayPrice"]
        except IndexError:
            price = "temporarily unavailable"
        lts_hotels.append((name, id_hotel, price))

    return lts_hotels


def detail_hotel(id_hotel: int):
    """
    Функция detal_hotel. Принимет на вход ид_отеля.
    Делает запрос и парсит список делати отеля.
    :return: Название отеля, URL фотографии с локацией, рейтинг отеля, список[URL фотографий]
    """

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "propertyId": id_hotel
    }

    response = request("POST", URL_DETAL_HOTEL, json=payload, headers=config.HAEDERS_RAPID, timeout=1000)
    # print(response.text)
    data = json.loads(response.text)
    name_hotel = data["data"]["propertyInfo"]["summary"]["name"]

    try:
        rating_hotel = data["data"]["propertyInfo"]["summary"]["overview"]["propertyRating"]["rating"]
    except TypeError:
        logger.error("detail_hotel - rating_hotel is temporarily unavailable")
        rating_hotel = "temporarily unavailable"

    photo_location = data["data"]["propertyInfo"]["summary"]["location"]["staticImage"]["url"]

    # photos = tuple(
    #     i["images"][0]["image"]["url"]
    #     for i in data["data"]["propertyInfo"]["propertyGallery"]["imagesGrouped"]
    # ) старый запрос-- изменили 14,03,2023

    photos = tuple(
        i["image"]["url"]
        for i in data["data"]["propertyInfo"]["propertyGallery"]["images"]
    )[:6]

    # print(name_hotel)
    # print(photo_location)
    # print(rating_hotel)
    # print(photos)

    return name_hotel, rating_hotel, photo_location, photos
