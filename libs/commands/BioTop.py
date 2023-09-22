'''

Модуль с биотопом

'''

import os
import re

from app import dp, bot, query, strconv, save_message, is_host
from config import MYSQL_HOST
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile


@dp.message_handler(content_types=['text'])
async def improve(message: types.Message):
    if message.text.lower() == "биоб":
        text = "Биотоп чмоней"
        count = 0
        for lab in labs.bio_top:
            count += 1
            text += f"\n{count}. [{strconv.deEmojify(lab['name'])}](tg://openmessage?user_id={lab['user_id']}) | {strconv.num_to_str(lab['bio_exp'])} опыта"
        await message.reply(text=text, parse_mode="Markdown")