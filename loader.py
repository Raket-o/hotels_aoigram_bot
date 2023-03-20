""" Модуль инициализации телеграмм бота"""

import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data import config
# from logging import Logger
from asyncio import get_event_loop

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
