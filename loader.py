""" Модуль инициализации телеграмм бота"""

import logging
from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_data import config

logger = logging.getLogger("logger_loader")


async def start_up(_):
    """Функция start_up. При запуске выводит текст в консоль"""
    logger.info("Bot started")
    print("Bot started")


async def on_shutdown(_):
    """Функция on_shutdown. При завершении выводит текст в консоль"""
    logger.info("Bot stopped")
    print("Bot stopped")


bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage, loop=get_event_loop())
