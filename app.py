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
    token = '6262610716:AAHnxnu4vyHgU_QFIDI1EXzN6oevEp5lc5k',
    proxy="http://H7zDFP:pvGSnG@45.155.202.95:8000/"
)
dp = Dispatcher(bot)

@dp.message_handler() 
async def handler(message: types.message):
    print(message)