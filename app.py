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

from libs.mysql_connect import query
from libs.handlers import main_handler 
from config import BOT_TOKEN



bot = Bot(
    token = BOT_TOKEN
)
dp = Dispatcher(bot)

dp.register_message_handler(main_handler)

executor.start_polling(dp, skip_updates=True)