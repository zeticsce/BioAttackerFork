'''

Модуль с корпами

'''

import os
import time
import datetime
import re
import string
import random
import copy
import json

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from Labs import Labs
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.callback_data import CallbackData

vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')

from math import floor


work_path = os.path.abspath(os.curdir)

def impr_price(start, end, power):
    price = 0
    for i in range(int(end) - int(start)):
        price += floor((int(start) + i + 1) ** power)
    return price

@dp.message_handler(content_types=["text"])
async def issues(message: types.Message):
        
    reg = re.fullmatch(r'\+корп ([а-яa-z0-9]+)', message.text.lower())
    if reg != None:
        key = reg.group(1)

        lab = labs.get_lab(message.from_user.id)
        if not lab.has_lab: return
        if lab.corp == key:
            await bot.send_message(chat_id=message.chat.id, text="Вы уже являетесь участником этой корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        if re.fullmatch(r"[a-z]+", key) == None: 
            await bot.send_message(chat_id=message.chat.id, text="Корп айди не действителен!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        
        corp = query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_key` = '{key}'")
        if len(corp) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Корп айди не действителен!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        corp = corp[0]
        applications = query(f"SELECT * FROM `bio_attacker`.`corps_applications` WHERE `user_id` = {lab.user_id}")
        if len(applications) != 0:

            from_date = datetime.datetime.fromtimestamp(applications[0]['from_date']).strftime("%d.%m.%Y")
            clear_applications = types.InlineKeyboardMarkup(row_width=1)
            clear_applications.row(
                types.InlineKeyboardButton('Ликвидировать заявку', callback_data=vote_cb.new(action='clear apl', id=message['from']['id'], chat_id=message['chat']['id'])),
            )
            if applications[0]['corp'] != corp['corp_key']:
                text = f'У вас висит одна активная заявка\nЗаявка в корпорацию <a href="tg://openmessage?user_id={corp["corp_head"]}">{applications[0]["corp_name"]}</a> от {from_date}\nПеред отправкой новой заявки необходимо ликвидировать старую!'
            else: text = f'Вы уже отправили заявку в корпорацию <a href="tg://openmessage?user_id={corp["corp_head"]}">{applications[0]["corp_name"]}</a>'
            await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id, reply_markup=clear_applications)
            return
        try: await bot.send_message(chat_id=corp['corp_chat'], text=f'Отправлена заявка на вступление в корпорацию «<a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>»', parse_mode="HTML")
        except: pass
        query(f"INSERT INTO `bio_attacker`.`corps_applications` (`id`, `user_id`, `corp`, `from_date`, `corp_name`) VALUES (NULL, '{lab.user_id}', '{key}', '{int(time.time())}', '{corp['corp_name']}')")
        text=f'Заявка на вступление в корпорацию «<a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>» отправлена!'
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id)
        


    reg = re.fullmatch(r'[\./!]создать корп(\s([@./:\\a-z0-9_?=]+))', message.text.lower())
    if reg != None and message['from']['id'] in [780882761, 1058211493]:

        url = reg.group(2).replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
        if re.fullmatch(r"[a-z0-9_]+", url) == None: return

        user = labs.get_user(url)
        if user == None:
            await bot.send_message(chat_id=message.chat.id, text="Юзер не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        
        name = strconv.normalaze(user['name'], str(user['user_id']))
        user_id = user['user_id']

        lab = labs.get_lab(user_id)
        if not lab.has_lab:
            await bot.send_message(chat_id=message.chat.id, text="Юзер еще не создал лабораторию!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        
        clear_lab = copy.copy(lab.__dict__)
        clear_lab.pop("_UserLab__start_data")
        members = {
            str(user_id): clear_lab
        }

        if len(query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_head` = {user_id}")) != 0:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь уже является главой корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            
            lab.save()

            return

        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(6))
        lab.corp = key

        lab.save()

        data = {
            "was_created": int(time.time()),
            "from_user": message.from_user.id
        }

        q = f"INSERT INTO `bio_attacker`.`corporations` (`id`, `corp_key`, `corp_head`, `members`, `other_data`, `corp_name`, `corp_chat`) VALUES (NULL, '{key}', '{user_id}', '{json.dumps(members)}', '{json.dumps(data)}', 'им. {strconv.normalaze(lab.name, lab.user_id)}', '{user_id}')"
        query(q)

@dp.callback_query_handler(vote_cb.filter(action='clear apl'))
async def first_help_editor(_query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]

    lab = labs.get_lab(from_user_id)
    if not lab.has_lab: 
        await _query.answer()
        return

    rslt = query(f"SELECT * FROM `bio_attacker`.`corps_applications` WHERE `user_id` = {from_user_id};")
    if len(rslt) != 0:
        query(f"DELETE FROM `bio_attacker`.`corps_applications` WHERE `user_id` = {from_user_id};")
        await _query.answer("Заявка очищена")
    await _query.answer("Заявок не найдено")