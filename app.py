import pymysql
from pymysql.cursors import DictCursor

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import sys
import asyncio

from libs.mysql_connect import query
from config import BOT_TOKEN



bot = Bot(
    token = BOT_TOKEN
)
dp = Dispatcher(bot)

@dp.message_handler() 
async def handler(message: types.message):
    print(message)