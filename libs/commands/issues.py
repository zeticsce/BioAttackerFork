'''

Модуль с показом болезней

'''

import os
import time
import datetime

from app import dp, bot, strconv
from libs.handlers import labs

from aiogram import types

from math import floor

from aiogram.utils.callback_data import CallbackData

work_path = os.path.abspath(os.curdir)

def impr_price(start, end, power):
    price = 0
    for i in range(int(end) - int(start)):
        price += floor((int(start) + i + 1) ** power)
    return price

vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')

@dp.message_handler(content_types=["text"])
async def issues(message: types.Message):
    if message.text.lower() == "биоболь" and not message.forward_from:
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
                        if item['pat_name'] is not None:
                            text += f"[{strconv.escape_markdown(item['pat_name'])}](tg://openmessage?user_id={item['user_id']})"
                        else:
                            text += f"[Неизвестный патоген](tg://openmessage?user_id={item['user_id']})"
                    else: 
                        text += f'{count + 1}. '
                        if item['pat_name'] is not None:
                            text += f"{strconv.escape_markdown(item['pat_name'])}"
                        else:
                            text += "Неизвестный патоген"
                    text += f" | до {until}\n"
                    in_list.append(item['user_id'])

                    count += 1
                    if count == 30: break
            victims_keyboard = types.InlineKeyboardMarkup(row_width=1)
            victims_keyboard.row(
                types.InlineKeyboardButton('❌ Скрыть', callback_data=vote_cb.new(action='delete msg', id=message.from_user.id, chat_id=message.chat.id)),
            )
            await bot.send_message(message.chat.id, text=text, parse_mode="Markdown", reply_markup=victims_keyboard)
