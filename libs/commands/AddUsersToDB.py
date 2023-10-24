'''

Штука для загрузки юзеров в бд

'''

import os
import re
import time
import datetime

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.callback_data import CallbackData

class LoadUsers:
    def __init__(self):
        self.users_stack = {}

load_users = LoadUsers()

@dp.message_handler(content_types=('text', 'sticker', 'video', 'photo', 'document', 'audio'))
async def LoadUsersHandler(message: types.Message):
    name = strconv.escape_sql(message.from_user.full_name)
    username = f"'{message.from_user.username}'" if message.from_user.username is not None else "NULL"
    user_id = message.from_user.id
    if len(query(f"SELECT * FROM `telegram_data`.`tg_users` WHERE `user_id` = {user_id}")) != 0:
        query(f"UPDATE `telegram_data`.`tg_users` SET `user_name` = {username}, `name` = '{name}' WHERE `tg_users`.`user_id` = '{user_id}'")
    else:
        query(f"INSERT INTO `telegram_data`.`tg_users` (`id`, `user_id`, `user_name`, `name`, `patogen_names`, `iris_name`) VALUES (NULL, '{user_id}', {username}, '{name}', NULL, NULL)")
