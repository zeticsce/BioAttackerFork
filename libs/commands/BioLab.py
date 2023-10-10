'''

Модуль с показом лабы

'''

import os
import re
import time
import datetime
import html

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs

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
            corp корп           айди корпы
            patogen_name        имя патогена пользователя

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
        """


        def get_impr_count(start, biores, power): # подсчет колва доступных уровней прокачки
            count = 0
            price = 0
            while price <= biores:
                count += 1
                price += floor((int(start) + count) ** power)
            return count - 1
        


        '''  Название вируса '''

        text = f'🦠 Информация о вирусе: `{lab.patogen_name if lab.patogen_name != None else "неизвестно"}`\n\n'

        '''  Владелец лабы '''
        owner_link = f'https://t.me/{lab.user_name}' if lab.user_name != None else f'tg://openmessage?user_id={lab.user_id}'
        text += f'👺 Владелец: [{lab.name}]({owner_link})\n'

        ''' Корпорация '''
        if lab.corp != None: text += f'🏢 Относится к корпорации: [{lab.corp_name}](tg://openmessage?user_id={lab.corp_owner_id})\n\n'
        else: text += f'\n'
        
        ''' Количество патогенов ''' 
        text += f'🧪 Патогенов: {lab.patogens} из {lab.all_patogens} (`+{get_impr_count(lab.all_patogens, lab.bio_res, 2)}`)\n'

        ''' Уровень разработки '''  
        if lab.qualification < 60: 
            qualification_count = get_impr_count(lab.qualification, lab.bio_res, 2.6)
            qualification_count = qualification_count if qualification_count + lab.qualification <= 60 else 60 - lab.qualification
            text += f'👨🏻‍🔬 Разработка: {lab.qualification} (`{61 - lab.qualification} мин.` | `+{qualification_count}`) \n\n'
        else: text += f'👨🏻‍🔬 Разработка: {lab.qualification} (`1 мин.`) \n\n'
        
        ''' Навыки '''
        text += f'🔬 **НАВЫКИ:**\n'
        text += f'🦠 Заразность: {lab.infectiousness} ур. (`+{get_impr_count(lab.infectiousness, lab.bio_res, 2.5)}`)\n'
        text += f'🛡 Иммунитет: {lab.immunity} ур. (`+{get_impr_count(lab.immunity, lab.bio_res, 2.45)}`)\n'
        text += f'☠️ Летальность: {lab.mortality} ур. (`+{get_impr_count(lab.mortality, lab.bio_res, 1.95)}`)\n'
        text += f'🕵️‍♂️ Безопасность: {lab.security} ур. (`+{get_impr_count(lab.security, lab.bio_res, 2.1)}`)\n\n'

        ''' Данные ''' 
        text += f'⛩ **ДАННЫЕ:**\n'
        text += f'☣️ Био-опыт: {strconv.num_to_str(lab.bio_exp)}\n'
        text += f'🧬 Био-ресурс: {strconv.num_to_str(lab.bio_res)}\n'

        text += f'😷 Спецопераций: {lab.suc_operations}/{lab.all_operations} (`{round(100 * int(lab.suc_operations) / int(lab.all_operations if lab.all_operations != 0 else 1))}%`)\n'
        text += f'🥽 Предотвращены: {lab.prevented_issue}/{lab.all_issue} (`{round(100* int(lab.prevented_issue) / int(lab.all_issue if lab.all_issue != 0 else 1))}%`)\n\n'

        ''' Горячка '''
        if lab.illness != None:
            declination = "" # склонение минуту/минуты/минут
            untill = floor(lab.illness['illness'] / 60)
            if untill <= 20:
                if untill == 1: declination = "минута"
                elif untill <= 4: declination = "минуты"
                else: declination = "минут"
            else: 
                if untill%10 == 1: declination = "минута"
                elif untill%10 <= 4: declination = "минуты"
                else: declination = "минут"

            text += f'🥴 Горячка вызванная патогеном `{lab.illness["patogen"]}` ещё `{untill}` {declination}.'

        await bot.send_message(chat_id=message.chat.id, 
            text=text, 
            reply_to_message_id=message.message_id, 
            parse_mode="Markdown",
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
        text = f'Болезни игрока [{message_name}](tg://openmessage?user_id={from_user_id})\n\n'
        
        count = 0
        in_list = []
        for item in list(reversed(lab.get_issues())):
            if item['user_id'] in in_list: continue
            if item['until_infect'] > int(time.time()):
                until = datetime.datetime.fromtimestamp(item['until_infect']).strftime("%d.%m.%Y")
                if item['hidden'] == 0: text += f'{count + 1}. [{strconv.escape_markdown(item["pat_name"])}](tg://openmessage?user_id={item["user_id"]}) | до {until}\n'
                else: text += f'{count + 1}. {strconv.escape_markdown(item["pat_name"])} | до {until}\n'
                in_list.append(item['user_id'])

                count += 1
                if count == 25: break
                
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
        name = html.escape(strconv.deEmojify(query.from_user.first_name), quote=True)
        name = name if name.replace(" ", "") != "" else item["user_id"]

        text = f'Жертвы игрока <a href="tg://openmessage?user_id={query.from_user.id}">{name}</a>\n\n'
        profit = 0

        count = 0
        victims = lab.get_victums()
        for item in list(reversed(victims)):
            if item['until_infect'] > int(time.time()):
                profit += item["profit"]
                if count < 25:
                    name = html.escape(strconv.deEmojify(item["name"]), quote=True)
                    name = name if name.replace(" ", "") != "" else item["user_id"]
                    until = datetime.datetime.fromtimestamp(item['until_infect']).strftime("%d.%m.%Y")
                    text += f'{count + 1}. <a href="tg://openmessage?user_id={item["user_id"]}">{name}</a> | +{item["profit"]} | до {until}\n'

                count += 1
        
        text += f'\nОбщая прибыль: +{strconv.format_nums(profit)} био-ресурсов 🧬'

        
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