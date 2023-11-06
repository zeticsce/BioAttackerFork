'''

Модуль с показом лабы

'''

import os
import re
import time
import datetime
import math

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs
from commands.messages import *

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.callback_data import CallbackData

from math import floor

vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')

def get_keyboard_first(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.row(
        types.InlineKeyboardButton('Жертвы', callback_data=vote_cb.new(action='victims', id=message.from_user.id, chat_id=message.chat.id)),
        types.InlineKeyboardButton('Болезни', callback_data=vote_cb.new(action='issues', id=message.from_user.id, chat_id=message.chat.id)),
        # types.InlineKeyboardButton('.д', callback_data=vote_cb.new(action='d', id=message.from_user.id)),
        # types.InlineKeyboardButton('Другое', callback_data=vote_cb.new(action='other', id=message.from_user.id)),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton('❌', callback_data=vote_cb.new(action='delete msg', id=message.from_user.id, chat_id=message.chat.id)),
    )

    return keyboard_markup

def get_impr_count(start, biores, power): # подсчет колва доступных уровней прокачки
    count = 0
    price = 0
    while price <= biores:
        count += 1
        price += floor((int(start) + count) ** power)
    return count - 1


@dp.message_handler(content_types=["text"])
async def show_lab(message: types.Message):

    if message.text.lower() == "биолаб":

        """
            Команда вывода лаборатории юзера
        """

        lab = labs.get_lab(message['from']['id'])
        if not lab.has_lab: 
            lab = labs.create_lab(message['from']['id'])

        # дальше лаба точно существует и полностью содежится в lab
        """
            поле                описание

            user_id             юзер айди пользователя
            name                имя пользователя
            user_name           юз пользователя
            corp                айди корпы
            patogen_name        имя патогена пользователя
            lab_name            имя лаборатории пользователя

            all_patogens        колличество всех патогенов у юзера
            patogens            колличество оставшихся патогенов у юзера
            last_patogen_time   время последнего израсходованного патогена (unix метка)

            qualification       уровень квалификации
            infectiousness      уровень заразности
            immunity            уровень иммунитета
            mortality           уровень летальности
            security            уровень безопасноси

            bio_exp             био опыт
            bio_res             био ресурс

            all_operations      колличество операций заражения
            suc_operations      колличество успешных операций заражения
            all_issue           колличество всех попыток заразить этого юзера
            prevented_issue     колличество предотвращенных попыток заразить этого юзера
            victims             колличество жертв
            disease             колличество болезней
            coins               колличество коинов
            bio_valuta          колличество какой либо валюты / ирисок

            last_farma          время последнего использования комманды ферма
            last_issue          время последнего заражения
            last_daily          время последнего получения ежи

            virus_chat          чат айди, куда отправлять вирусы (None если в лс)

            modules             JSON поле хранит данные в виде ключ => объект, предназначено для записей модулей
        """

        if lab.theme not in theme: themeId = "standard"
        else: themeId = lab.theme
    
        labTheme = theme[themeId]["biolab"]
        
        text = labTheme['lab']\
        .replace("{pats}", str(lab.patogens))\
        .replace("{all_pats}", str(lab.all_patogens))\
        .replace("{qual}", str(lab.qualification))\
        .replace("{infect}", str(lab.infectiousness))\
        .replace("{immunity}", str(lab.immunity))\
        .replace("{mortality}", str(lab.mortality))\
        .replace("{security}", str(lab.security))\
        .replace("{bio_res}", str(strconv.num_to_str(lab.bio_res)))\
        .replace("{bio_exp}", str(strconv.num_to_str(lab.bio_exp)))\
        .replace("{lab_name}", lab.lab_name if lab.lab_name != None else labTheme["no lab name"].replace("{name}", lab.name))\
        .replace("{patogen_name}", lab.patogen_name if lab.patogen_name != None else labTheme["no pathogen name"])\
        \
        .replace("{prevented_issue}", str(lab.prevented_issue))\
        .replace("{all_operations}", str(lab.all_operations))\
        .replace("{suc_operations}", str(lab.suc_operations))\
        .replace("{all_issue}", str(lab.all_issue))\
        \
        .replace("{issues_percent}", str(round(int(lab.prevented_issue/(lab.all_issue+1)*100))))\
        .replace("{operations_percent}", str(round(int(lab.suc_operations/(lab.all_operations+1)*100))))\
        \
        .replace("{pats_calk}", str(get_impr_count(lab.all_patogens, lab.bio_res, 2)))\
        .replace("{infect_calk}", str(get_impr_count(lab.infectiousness, lab.bio_res, 2.5)))\
        .replace("{immunity_calk}", str(get_impr_count(lab.immunity, lab.bio_res, 2.55)))\
        .replace("{mortality_calk}", str(get_impr_count(lab.mortality, lab.bio_res, 1.95)))\
        .replace("{security_calk}", str(get_impr_count(lab.security, lab.bio_res, 2.1)))\
        \
        .replace("{user_id}", str(lab.user_id))

        if lab.qualification < 60: 
            qualification_count = get_impr_count(lab.qualification, lab.bio_res, 2.6)
            qualification_count = qualification_count if qualification_count + lab.qualification <= 60 else 60 - lab.qualification
            qualification_calk = labTheme['qualification calk'].replace("{qual_time}", str(61 - lab.qualification)).replace("{qual_calk}", str(qualification_count))
        else:
            qualification_calk = labTheme['qualification calk 60'].replace("{qual_time}", str(61 - lab.qualification))
        text = text.replace("{qualification_calk}", qualification_calk)

        if lab.corp == None:
            text = text.replace("{corp}", labTheme["no corp"])
        else:
            text = text.replace("{corp}", labTheme["corp"].replace("{corp_name}", lab.corp_name).replace("{corp_owner_id}", str(lab.corp_owner_id)))

        if lab.patogens == lab.all_patogens:
            text = text.replace("{new_patogen}", labTheme["full patogens"])
        else:
            quala = (61 - lab.qualification) * 60
            if (quala - ( int(time.time()) - lab.last_patogen_time)) < 60:
                untill = quala - int(time.time()) + lab.last_patogen_time
                patogen_line = labTheme["next patogen sec"]
            else:
                untill = math.ceil(round(quala - ( int(time.time()) - lab.last_patogen_time )) / 60)
                patogen_line = labTheme["next patogen min"]
            text = text.replace("{new_patogen}", patogen_line.replace("{next_patogen_time}", str(untill)))

        if lab.illness != None:
            untill = floor(lab.illness['illness'] / 60)
            if lab.illness['patogen'] != None:
                text = text.replace("{fever}", labTheme['fever patogen'].replace("{fever_time}", str(untill)).replace("{fever_name}", lab.illness['patogen']))
            else:
                text = text.replace("{fever}", labTheme['fever'].replace("{fever_time}", str(untill)))
        else:
            text = text.replace("{fever}", labTheme['no fever'])

        await bot.send_message(chat_id=message.chat.id, 
            text=text, 
            reply_to_message_id=message.message_id, 
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_keyboard_first(message)
        )

        lab.save() 


@dp.callback_query_handler(vote_cb.filter(action='issues'))
async def first_help_editor(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    if from_user_id == str(query.from_user.id):

        lab = labs.get_lab(from_user_id)
        text = f'Болезни игрока [{strconv.normalaze(message_name, replace=str(from_user_id))}](tg://openmessage?user_id={from_user_id})\n\n'
        
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
            types.InlineKeyboardButton('❌', callback_data=vote_cb.new(action='delete msg', id=query.from_user.id, chat_id=chat_id)),
        )

        await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown", reply_markup=victims_keyboard)
        await query.message.edit_reply_markup(victims_keyboard)
        await query.answer()

    
    else:
        await query.answer("Эта кнопка не для тебя :)")


@dp.callback_query_handler(vote_cb.filter(action='victims'))
async def first_help_editor(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    if from_user_id == str(query.from_user.id):

        lab = labs.get_lab(from_user_id)

        text = f'Жертвы игрока <a href="tg://openmessage?user_id={query.from_user.id}">{strconv.normalaze(message_name, replace=str(from_user_id))}</a>\n\n'
        profit = 0

        count = 0
        victims = lab.get_victums()
        actual = 0
        for item in list(reversed(victims)):
            if item['until_infect'] > int(time.time()):
                actual += 1
                profit += item["profit"]
                if count < 50: 
                    name = strconv.normalaze(item["name"], replace=str(item["user_id"]))
                    until = datetime.datetime.fromtimestamp(item['until_infect']).strftime("%d.%m.%Y")
                    text += f'{count + 1}. <a href="tg://openmessage?user_id={item["user_id"]}">{name}</a> | +{item["profit"]} | до {until}\n'

                count += 1
        
        text += f'\n🤒 Итого {actual} зараженных'
        text += f'\n🧬 Общая прибыль: +{strconv.format_nums(profit)} био-ресурсов '

        
        victims_keyboard = types.InlineKeyboardMarkup(row_width=1)
        victims_keyboard.row(
            types.InlineKeyboardButton('❌', callback_data=vote_cb.new(action='delete msg', id=query.from_user.id, chat_id=chat_id)),
        )

        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=victims_keyboard)
        await query.message.edit_reply_markup(victims_keyboard)
        await query.answer()

    
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='delete msg'))
async def first_help_editor(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]
    if from_user_id == str(query.from_user.id):

        await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)

    else:
        await query.answer("Эта кнопка не для тебя :)")