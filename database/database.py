""" Модуль работы с базой данных"""

import sqlite3
import json


def init_db() -> None:
    """ Функция init_db. При отсутствии базы донной создаёт ёё. """
    with sqlite3.connect('database/database.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_user_request'; 
            """
        )
        exists = cursor.fetchone()
    # exists: Optional[tuple[str, ]] = cursor.fetchone()
    # now in `exist` we have tuple with table name if table really exists in DB

    if not exists:
        cursor.executescript(
            """
            CREATE TABLE `table_user_request` (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER DEFAULT 0,
                user_name TEXT DEFAULT NULL,                   
                command TEXT DEFAULT NULL,
                country TEXT DEFAULT NULL,
                city TEXT DEFAULT NULL,                    
                city_area TEXT DEFAULT NULL,
                list_hotels TEXT DEFAULT NULL,                    
                method_sort TEXT DEFAULT NULL                  
            )
            """
        )
    conn.commit()


def rec_cmd_low(dict_data) -> None:
    """ Функция rec_cmd_low. Записывает данные в базу данных"""
    with sqlite3.connect('database/database.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO table_user_request (user_id, user_name, command, country, city, city_area, list_hotels, method_sort)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)         
            """,
            (
                dict_data["user_id"],
                dict_data["user_name"],
                dict_data["command"],
                dict_data["country"],
                dict_data["city"],
                dict_data["city_area"],
                json.dumps(dict_data["list_hotels"]),
                dict_data["method_sort_for_history"]
            )
        )
        conn.commit()


def seek_history(user_id: int):
    """
    Функция seek_history. Находит по user_id и возвращает строки из бд.
    :param user_id: Ид пользователя
    :return: список[со строками из бд]
    """
    with sqlite3.connect('database/database.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM table_user_request WHERE user_id = ?
            """,
            (user_id, )
        )
        detail_history = cursor.fetchall()

        return detail_history


def delete_history_db(user_id: int) -> None:
    """
    Функция delete_history_db. Принимает на вход user_id
    и удаляет все строки с данным user_id
    :param user_id: user_id
    :return: None
    """
    with sqlite3.connect('database/database.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM table_user_request WHERE user_id = ?
            """,
            (user_id, )
        )
