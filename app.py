import pymysql
from pymysql.cursors import DictCursor

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import sys
import asyncio
import time

sys.path.insert(1, 'libs')

from libs.mysql_connect import query

from config import BOT_TOKEN, OWNER_ID

from libs.handlers import *


bot = Bot(
    token = BOT_TOKEN,
    parse_mode="Markdown"
)
dp = Dispatcher(bot)

async def start_notify(dp):
    await dp.bot.send_message(OWNER_ID, "Бот запущен")

async def on_startup(dp):
    await start_notify(dp)



if __name__ == '__main__':
    from libs.handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

