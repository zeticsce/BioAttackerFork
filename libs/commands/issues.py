'''

Модуль с показом болезней

'''

import os
import time
import datetime

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from Labs import Labs
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from math import floor

work_path = os.path.abspath(os.curdir)

def impr_price(start, end, power):
    price = 0
    for i in range(int(end) - int(start)):
        price += floor((int(start) + i + 1) ** power)
    return price

@dp.message_handler(content_types=["text"])
async def issues(message: types.Message):
    if message.text.lower() == "биоболь":
        lab = labs.get_lab(message.from_user.id)
        if lab.has_lab:
            text = f'Болезни игрока [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})\n\n'
            
            count = 0
            in_list = []
            for item in list(reversed(lab.get_issues())):
                if item['user_id'] in in_list: continue
                if item['until_infect'] > int(time.time()):
                    until = datetime.datetime.fromtimestamp(item['until_infect']).strftime("%d.%m.%Y")
                    if item['hidden'] == 0: 
                        text += f'{count + 1}. '
                        if item['pat_name'] != None:
                            text += f"[{strconv.escape_markdown(item['pat_name'])}](tg://openmessage?user_id={item['user_id']})"
                        else:
                            text += f"[Неизвестный патоген](tg://openmessage?user_id={item['user_id']})"
                        text += f" | до {until}\n"
                    else: 
                        text += f'{count + 1}. '
                        if item['pat_name'] != None:
                            text += f"{strconv.escape_markdown(item['pat_name'])}"
                        else:
                            text += "Неизвестный патоген"
                    in_list.append(item['user_id'])

                    count += 1
                    if count == 50: break
            await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
