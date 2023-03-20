""" Модуль запуска телеграмм бота"""

import logging
from aiogram import executor
from loader import dp, start_up, on_shutdown
from handlers.default_heandlers import start
from utils.logging import logger_root
from database import database
# from logging import Logger

logger = logging.getLogger("logger_main")

if __name__ == '__main__':
    database.init_db()

    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=start_up,
                           on_shutdown=on_shutdown)
