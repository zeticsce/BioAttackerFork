from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import sys
import asyncio
import time
import datetime

from config import BOT_TOKEN, OWNER_ID

from libs.mysql_connect import query
from libs.handlers import *
from libs.StringConverters import StringConv
from libs.ChatHistory import save_message
sys.path.append(os.path.abspath(os.curdir) + "/libs")

strconv = StringConv()  
bot = Bot(
    token = BOT_TOKEN
)
dp = Dispatcher(bot)

async def on_startup(dp):
    await dp.bot.send_message(OWNER_ID, f"*Вход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

if __name__ == '__main__':
    from libs.handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



