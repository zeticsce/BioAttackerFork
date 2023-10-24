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

    reg = re.fullmatch(r'-корп', message.text.lower())
    if reg != None:
        lab = labs.get_lab(message.from_user.id)
        if not lab.has_lab: return

        if lab.corp == None:
            await bot.send_message(chat_id=message.chat.id, text="Вы не являетесь участником какой либо корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        corp = query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_key` = '{lab.corp}'")
        if len(corp) == 0: 
            lab.corp = None
            lab.save()
            return
        corp = corp[0]
        if corp['corp_head'] == lab.user_id:
            await bot.send_message(chat_id=message.chat.id, text="Вы не можете выйти из корпорации так как являетесь ее главой!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        lab.corp = None
        lab.save()

        corp['members'] = json.loads(corp['members'])
        if str(lab.user_id) in corp['members']:
            await bot.send_message(chat_id=message.chat.id, text=f'Вы вышли из корпорации <a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>', parse_mode="HTML", reply_to_message_id=message.message_id)

        del corp['members'][str(lab.user_id)]

        query(f"UPDATE `bio_attacker`.`corporations` SET `members` = '{json.dumps(corp['members'])}' WHERE `corp_key` = '{corp['corp_key']}'")



    reg = re.fullmatch(r'\+корп ([а-яa-z0-9]+)', message.text.lower())
    if reg != None:
        key = reg.group(1).strip()

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
        if str(message.from_user.id) in json.loads(corp['members']):
            await bot.send_message(chat_id=message.chat.id, text="Вы уже являетесь участником этой корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        if len(query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_head` = {lab.user_id}")) != 0:
            await bot.send_message(chat_id=message.chat.id, text="Владелец корпорации не пожет подать заявку в другую корпорацию!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
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
        try: await bot.send_message(chat_id=corp['corp_chat'], text=f'Пришла заявка на вступление в корпорацию «<a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>»\n\nВведите <code>!принять @{lab.user_id}</code> или <code>!отклонить @{lab.user_id}</code>\nВсе заявки: <code>!заявки</code>', parse_mode="HTML")
        except: pass
        query(f"INSERT INTO `bio_attacker`.`corps_applications` (`id`, `user_id`, `corp`, `from_date`, `corp_name`) VALUES (NULL, '{lab.user_id}', '{key}', '{int(time.time())}', '{corp['corp_name']}')")
        text = f'Заявка на вступление в корпорацию «<a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>» отправлена!'
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id)

    reg = re.fullmatch(r'[\./!][\s]?заявки', message.text.lower())
    if reg != None:

        corp = query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_head` = {message.from_user.id}")
        if len(corp) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Вам необходимо быть главой корпорации для доступа к этой команде!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        else: corp = corp[0]
        applications = query(f"SELECT * FROM bio_attacker.corps_applications LEFT JOIN telegram_data.tg_users ON tg_users.user_id = corps_applications.user_id WHERE `corp` LIKE '{corp['corp_key']}';")

        text = f'Список заявок в корпорацию <a href="tg://openmessage?user_id={corp["corp_head"]}">{corp["corp_name"]}</a>:'
        count = 0
        for appl in applications:
            count += 1
            text += f'\n {count}. <a href="tg://openmessage?user_id={appl["user_id"]}">{appl["name"]}</a> <code>@{appl["user_id"]}</code>'
        text += f"\nВсего заявок: {count}"
        text += f"\n<code>!принять</code> <code>!отклонить</code>"
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id)

    reg = re.fullmatch(r'[\./!][\s]?отклонить(\s([@./:\\a-z0-9_?=]+))', message.text.lower())
    if reg != None:
        url = reg.group(2).replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
        if re.fullmatch(r"[a-z0-9_]+", url) == None: return

        corp = query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_head` = {message.from_user.id}")
        if len(corp) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Вам необходимо быть главой корпорации для доступа к этой команде!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        else: corp = corp[0]

        user = labs.get_user(url)
        if user == None:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        name = strconv.normalaze(user['name'], str(user['user_id']))
        user_id = user['user_id']

        lab = labs.get_lab(user_id)
        if not lab.has_lab:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        if len(query(f"SELECT * FROM `bio_attacker`.`corps_applications` WHERE `user_id` = {user_id} AND `corp` LIKE '{corp['corp_key']}'")) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Заявок в вашу корпорацию не найдено!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        corp['members'] = json.loads(corp['members'])
        if str(user_id) in corp['members']:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь уже является участником данной корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        lab.corp = None
        lab.save()

        query(f"DELETE FROM `bio_attacker`.`corps_applications` WHERE `corp` = '{corp['corp_key']}'")
        await bot.send_message(chat_id=message.chat.id, text=f"Заявка пользователя ликвидирована! <b>(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})</b>", parse_mode="HTML", reply_to_message_id=message.message_id)

    reg = re.fullmatch(r'[\./!][\s]?принять(\s([@./:\\a-z0-9_?=]+))', message.text.lower())
    if reg != None:
        time_start = time.time()
        url = reg.group(2).replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
        if re.fullmatch(r"[a-z0-9_]+", url) == None: return

        corp = query(f"SELECT * FROM `bio_attacker`.`corporations` WHERE `corp_head` = {message.from_user.id}")
        if len(corp) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Вам необходимо быть главой корпорации для доступа к этой команде!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return
        else: corp = corp[0]

        user = labs.get_user(url)
        if user == None:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        name = strconv.normalaze(user['name'], str(user['user_id']))
        user_id = user['user_id']

        lab = labs.get_lab(user_id)
        if not lab.has_lab:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        if len(query(f"SELECT * FROM `bio_attacker`.`corps_applications` WHERE `user_id` = {user_id} AND `corp` LIKE '{corp['corp_key']}'")) == 0:
            await bot.send_message(chat_id=message.chat.id, text="Заявок в вашу корпорацию не найдено!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        corp['members'] = json.loads(corp['members'])
        if str(user_id) in corp['members']:
            await bot.send_message(chat_id=message.chat.id, text="Пользователь уже является участником данной корпорации!", parse_mode="HTML", reply_to_message_id=message.message_id)
            return

        lab.corp = corp['corp_key']
        lab.save()

        clear_lab = copy.copy(lab.__dict__)
        clear_lab.pop("_UserLab__start_data")
        corp['members'][str(user_id)] = clear_lab
        query(f"UPDATE `bio_attacker`.`corporations` SET `members` = '{json.dumps(corp['members'])}' WHERE `corp_key` = '{corp['corp_key']}'")
        query(f"DELETE FROM `bio_attacker`.`corps_applications` WHERE `corp` = '{corp['corp_key']}'")
        await bot.send_message(chat_id=message.chat.id, text=f"Пользователь был принят в корпорацию! <b>(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})</b>", parse_mode="HTML", reply_to_message_id=message.message_id)

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
        await bot.send_message(chat_id=message.chat.id, text=f'Корпорация <a href="tg://openmessage?user_id={user_id}">им. {strconv.normalaze(lab.name, lab.user_id)}</a> успешно создана!\nКей корпы: <code>{key}</code>', parse_mode="HTML", reply_to_message_id=message.message_id)

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
