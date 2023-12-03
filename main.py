""" Модуль запуска телеграмм бота"""

import logging

from aiogram import executor

from database import database
from handlers.default_heandlers import start
from loader import dp, on_shutdown, start_up
from utils.logging import logger_root


logger = logging.getLogger("logger_main")

if __name__ == "__main__":
    database.init_db()

    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=start_up, on_shutdown=on_shutdown
    )
