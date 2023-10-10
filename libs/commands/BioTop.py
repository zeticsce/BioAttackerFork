'''

Модуль с биотопом

'''

import os
import re

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile


@dp.message_handler(content_types=["text"])
async def improve(message: types.Message):
    if message.text.lower() == "биоб":
        text = "Биотоп чмоней\n"
        count = 0
        all_bio_exp = query("SELECT SUM(bio_exp) as bio FROM `bio_attacker`.`labs`")[0]['bio']
        for lab in labs.bio_top:
            count += 1
            text += f'\n{count}. <a href="tg://openmessage?user_id={lab["user_id"]}">{strconv.deEmojify(lab["name"])}</a> | {strconv.num_to_str(lab["bio_exp"])} опыта'

        text += f"\n\nБанк био-опыта в игре: {strconv.num_to_str(all_bio_exp)}"
        await bot.send_message(message.chat.id, text=text, parse_mode="HTML")