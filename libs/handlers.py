import os
import shutil
import string
import requests
import random
import subprocess
import sys
import datetime
import re
import time
import json
import copy

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from Labs import Labs

labs = Labs()

from commands.improvements import *
from commands.BioTop import *
from commands.BioLab import *
from commands.AddUsersToDB import *
from commands.Attack import *
from commands.issues import *
from commands.messages import *
from commands.rp_module import *
from commands.corps import *


from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from math import ceil, floor

work_path = os.path.abspath(os.curdir)


if requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST: # Необходимо, потому что команда /git и /restar работает только на хостинге
    @dp.message_handler(commands=["git"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        git_message = await bot.send_message(message.chat.id, "🪛 *Ожидаем клонирования...*", parse_mode="Markdown")

        pull_result = subprocess.Popen(["git", "pull", "https://github.com/kawasaji/BioAttacker"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
        output, errors = pull_result.communicate(input="Hello from the other side!")
        pull_result.wait()
        await bot.edit_message_text(f"🪛 *Ожидаем клонирования...\nРезультат:*\n`{output}`", git_message.chat.id, git_message.message_id, parse_mode="Markdown")
        if "Already up to date.\n" != output:
            await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

            try:
                dp.stop_polling()
                await dp.wait_closed()
                await bot.close()
            except: pass

            os.system(f"python {work_path}/app.py &")
            sys.exit(0)
        else: await bot.send_message(message.chat.id, f"*Файлы не затронуты, перезагрузка не требуется!*", parse_mode="Markdown")
    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

        try:
            dp.stop_polling()
            await dp.wait_closed()
            await bot.close()
        except: pass


        os.system(f"python {work_path}/app.py &")
        sys.exit(0)

@dp.message_handler(commands=["exit"], commands_prefix='.')
async def hi_there(message: types.message):
    if message['from']['id'] not in [780882761, 1058211493]: return
    await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
    sys.exit(0)

@dp.message_handler(commands=["start"], commands_prefix='!/.')
async def hi_there(message: types.message):
    text = random.choice(start_text)
    text += "[Все команды бота](https://teletype.in/@kawasaji/commands_of_bio-cmo)"
    await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")


@dp.message_handler(commands=["export", "exp"], commands_prefix='!/.')
async def handler(message: types.message):
    """
        Экспорт файлов из бота команда /export <путь к файлу>
        Просто /export создает архив всего бота
    """
    if message['from']['id'] not in [780882761, 1058211493]: return
    message.text = message.text.split(" ")
    message.text.pop(0)
    message.text = ' '.join(message.text).replace("\\", "/").replace(" ", "")
    if message.text == '' or message.text == '/':
        await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path), filename='BioAttacker.zip'))
        os.remove(work_path + "/files.zip")
    else:
        if not message.text.startswith('/'): message.text = "/" + message.text
        if os.path.exists(work_path + message.text):
            if not os.path.isfile(work_path + message.text):
                await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path + message.text),  filename=message.text + ".zip"))
                os.remove(work_path + "/files.zip")
            else:
                await bot.send_document(message.chat.id,  InputFile(work_path + message.text, filename=message.text))
        else: await bot.send_message(message.chat.id, f"🪛 Путь `{message.text}` не найден")

@dp.message_handler(content_types=["text"]) 
async def handler(message: types.message):

    if message.text.lower() == "био":
        await bot.send_message(message.chat.id, f"*Бот на месте*", parse_mode='Markdown')

    if message.text.lower() == "-вирус":
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.patogen_name = None
            lab.save()

            await bot.send_message(message.chat.id, "✅ Название патогена удалено.")

    if message.text.lower() == "-лаб":
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.lab_name = None
            lab.save()

            await bot.send_message(message.chat.id, "✅ Имя лаборатории удалено.")

    if message.text.lower().startswith("+лаб "):

        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            labName = message.text[5::].strip()

            if len(labName) > 30:
                await bot.send_message(message.chat.id, "Длина имени лаборатории не может быть больше 30 символов")
                return
            if len(labName) == 0:
                await bot.send_message(message.chat.id, "Имя лаборатории не может быть пустым!")
                return
            if re.fullmatch(r"([a-zA-Zа-яА-Я0-9_\s,.!?]*)", labName) == None: # Проверка на валидность имени
                await bot.send_message(message.chat.id, "В названии присутствуют недопустимые символы!")
                return

            this_name_lab = query(f"SELECT * FROM `bio_attacker`.`labs` WHERE `lab_name` = '{strconv.escape_sql(labName)}'")
            if len(this_name_lab) != 0:
                if this_name_lab[0]['user_id'] != lab.user_id:
                    await bot.send_message(message.chat.id, "Такое имя лаборатории уже существует!")
                    lab.save()
                    return

            lab.lab_name = labName
            lab.save()

            await bot.send_message(message.chat.id, "✅ Имя лаборатории успешно обновлено!")

    if message.text.lower().startswith("+вирус "):

        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            patName = message.text[7::].strip()

            if len(patName) > 50:
                await bot.send_message(message.chat.id, "Длина названия вируса не может быть больше 50 символов")
                return
            if len(patName) == 0:
                await bot.send_message(message.chat.id, "Вирус не может быть пустым!")
                return
            if re.fullmatch(r"([a-zA-Zа-яА-Я0-9_\s,.!?]*)", patName) == None: # Проверка на валидность имени патогена
                await bot.send_message(message.chat.id, "В названии присутствуют недопустимые символы!")
                return
            virus_lab = query(f"SELECT * FROM `bio_attacker`.`labs` WHERE `patogen_name` = '{strconv.escape_sql(patName)}'")
            if len(virus_lab) != 0:
                if virus_lab[0]['user_id'] != lab.user_id:
                    await bot.send_message(message.chat.id, "Такой вирус уже существует!")
                    return

            lab.patogen_name = patName
            lab.save()

            await bot.send_message(message.chat.id, "✅ Название патогена успешно обновлено!")

    if message.text.lower() == "+вирусы":
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.virus_chat = message.chat.id
            lab.save()
            await bot.send_message(message.chat.id, text="Сообщения службы безопасности перенесены в этот чат", parse_mode="Markdown")

    if message.text.lower() in ("биожертвы", "биоежа"):
        lab = labs.get_lab(message['from']['id'])
        
        text = f'Жертвы игрока <a href="tg://openmessage?user_id={message.from_user.id}">{strconv.normalaze(message.from_user.first_name, replace=str(message["from"]["id"]))}</a>\n\n'
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
            types.InlineKeyboardButton('❌', callback_data=vote_cb.new(action='delete msg', id=message['from']['id'], chat_id=message['chat']['id'])),
        )


        await bot.send_message(message.chat.id, text=text, parse_mode="HTML", reply_markup=victims_keyboard)

    if message.text.lower() in ("биоферма", "биофарма", "биофа", "майн"):
        
        lab = labs.get_lab(message['from']['id'])
        if lab.last_farma + (60*60) > int(time.time()):
            minuts = 60 - int((int(time.time()) - lab.last_farma)/60)
            if minuts <= 20:
                if minuts == 1: declination = "минута"
                elif minuts <= 4: declination = "минуты"
                else: declination = "минут"
            else: 
                if minuts%10 == 1: declination = "минута"
                elif minuts%10 <= 4: declination = "минуты"
                else: declination = "минут"

            await bot.send_message(message.chat.id, text=f'Ожидайте еще {minuts} {declination} до следующей фармы!!', parse_mode="Markdown")
            lab.save()
            return
        
        profit = random.randint(20, 200)

        lab.coins += profit
        lab.last_farma = int(time.time())
        lab.save()

        text = f'Вы успешно пофармили и получили {profit} коинов 💰!'

        await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")

    if message.text.lower() in ("биомеш", "биомешок", "биобаланс", "коины"):

        lab = labs.get_lab(message['from']['id'])

        text = f'Мешок игрока [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})\n\n'\
               f'Коины: _{lab.coins}_ 💰\n' \
               f'Био-коины: _{lab.bio_valuta}_ 🥑'

        await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")

    
    if message.text.lower() == "биохелп":
        await bot.send_message(message.chat.id, f"[Все команды бота](https://teletype.in/@kawasaji/commands_of_bio-cmo)", parse_mode="Markdown")

    reg = re.fullmatch(r'[\./!]ид(\s([@./:\\a-z0-9_?=]+))?', message.text.lower())
    if reg != None:
        url = reg.group(2)
        name = None
        if url != None:
            clear_url = url.replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
            if re.fullmatch(r"[a-z0-9_]+", clear_url) != None:
                user = labs.get_user(clear_url)
                if user != None:
                    name = strconv.normalaze(user['name'], str(user['user_id']))
                    user_id = user['user_id']
        elif message.reply_to_message:
            name = strconv.normalaze(message.reply_to_message.from_user.first_name, str(message.reply_to_message.from_user.id))
            user_id = message.reply_to_message.from_user.id
        else:
            name = strconv.normalaze(message.from_user.first_name, str(message.from_user.id))
            user_id = message.from_user.id
        if name != None:
            text = f'🌊 Айди игрока <a href="tg://openmessage?user_id={user_id}">{name}</a> равен <code>@{user_id}</code>'
            await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id)
        elif url != None:
            await bot.send_message(chat_id=message.chat.id, text="Юзер не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)


vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')

def back_btn(message: types.Message, usid):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.row(
        types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action='desc', id=usid, chat_id=message.chat.id)),

    )

    return keyboard_markup

def first_change_theme_btn(message: types.Message, usid):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.row(
        types.InlineKeyboardButton(text='Выбрать', callback_data=vote_cb.new(action='choose', id=usid, chat_id=message.chat.id)),
        types.InlineKeyboardButton(text='Посмотреть описания', callback_data=vote_cb.new(action='desc', id=usid, chat_id=message.chat.id)),

    )

    keyboard_markup.add(
        types.InlineKeyboardButton(text='❌', callback_data=vote_cb.new(action='close', id=usid, chat_id=message.chat.id)),
    )



    return keyboard_markup

def second_change_theme_btn(message: types.Message, usid):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.row(
        types.InlineKeyboardButton(text='Стандартная тема', callback_data=vote_cb.new(action='desc_standard', id=usid, chat_id=message.chat.id)),
        

    )
    keyboard_markup.add(
        types.InlineKeyboardButton(text='🇦🇿 Азербайджанская тема', callback_data=vote_cb.new(action='desc_azeri', id=usid, chat_id=message.chat.id)),
    )
    keyboard_markup.add(
        types.InlineKeyboardButton(text='Хеллоуинская тема', callback_data=vote_cb.new(action='desc_hell', id=usid, chat_id=message.chat.id)),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(text='🇺🇦 Украинская тема', callback_data=vote_cb.new(action='desc_ukraine', id=usid, chat_id=message.chat.id)),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action='back', id=usid, chat_id=message.chat.id)),
    )

    return keyboard_markup

def change_theme_btn(message: types.Message, usid):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.row(
        types.InlineKeyboardButton(text='Стандартная', callback_data=vote_cb.new(action='standard', id=usid, chat_id=message.chat.id)),
        types.InlineKeyboardButton(text='🇦🇿 Азербайджанская', callback_data=vote_cb.new(action='azeri', id=usid, chat_id=message.chat.id)),
        types.InlineKeyboardButton(text='Хеллоуинская', callback_data=vote_cb.new(action='hell', id=usid, chat_id=message.chat.id)),
        types.InlineKeyboardButton(text='🇺🇦 Украинская', callback_data=vote_cb.new(action='ukraine', id=usid, chat_id=message.chat.id)),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action='back', id=usid, chat_id=message.chat.id)),
    )


    return keyboard_markup

@dp.message_handler(commands=["тема", "т"], commands_prefix='!/.')
async def handler(message: types.message):

    await bot.send_message(message.chat.id, "Что пожелаете сделать?)", reply_markup=first_change_theme_btn(message, message.from_user.id))

@dp.callback_query_handler(vote_cb.filter(action='back'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):

        await bot.edit_message_text(chat_id=chat_id, text="Что пожелаете сделать?)", message_id=query.message.message_id, reply_markup=first_change_theme_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='desc_standard'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        text = f"Название темы: {theme['standard']['theme_name']}\n\n"
        text += f"Описание темы: {theme['standard']['theme_desc']}"
        await bot.edit_message_text(chat_id=chat_id, text=text, message_id=query.message.message_id, reply_markup=back_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='desc_ukraine'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        text = f"Название темы: {theme['ukraine']['theme_name']}\n\n"
        text += f"Описание темы: {theme['ukraine']['theme_desc']}"
        await bot.edit_message_text(chat_id=chat_id, text=text, message_id=query.message.message_id, reply_markup=back_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='desc_azeri'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        text = f"Название темы: {theme['azeri']['theme_name']}\n\n"
        text += f"Описание темы: {theme['azeri']['theme_desc']}"
        await bot.edit_message_text(chat_id=chat_id, text=text, message_id=query.message.message_id, reply_markup=back_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")
    
@dp.callback_query_handler(vote_cb.filter(action='desc_hell'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        text = f"Название темы: {theme['hell']['theme_name']}\n\n"
        text += f"Описание темы: {theme['hell']['theme_desc']}"
        await bot.edit_message_text(chat_id=chat_id, text=text, message_id=query.message.message_id, reply_markup=back_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='desc'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        await bot.edit_message_text(chat_id=chat_id, text="Выберите тему для того чтобы посмотреть его описание", message_id=query.message.message_id, reply_markup=second_change_theme_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='close'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        await bot.delete_message(chat_id, query.message.message_id)
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='choose'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    chat_id = callback_data["chat_id"]
    from_user_id = callback_data["id"]
    if from_user_id == str(query.from_user.id):
        await bot.edit_message_text(chat_id=chat_id, text="Выберите тему", message_id=query.message.message_id, reply_markup=change_theme_btn(query.message, from_user_id))
    else:
        await query.answer("Эта кнопка не для тебя :)")
    # await bot.send_message(chat_id, "Выберите тему", reply_markup=change_theme_btn(query.message))  

@dp.callback_query_handler(vote_cb.filter(action='standard'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]
    lab = labs.get_lab(from_user_id)
    if from_user_id == str(query.from_user.id):
        if lab.theme == None:

            await bot.edit_message_text(chat_id=chat_id, text="У вас и так стандартная тема!", message_id=query.message.message_id)
            return
        else:
            lab.theme = None
            lab.save()
            await bot.edit_message_text(chat_id=chat_id, text="✅ Стандартная тема установлена!", message_id=query.message.message_id)

    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='ukraine'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]
    lab = labs.get_lab(from_user_id)
    if from_user_id == str(query.from_user.id):
        if lab.theme == "ukraine":

            await bot.edit_message_text(chat_id=chat_id, text="У вас українська тема!", message_id=query.message.message_id)
            return
        else:
            lab.theme = "ukraine"
            lab.save()
            await bot.edit_message_text(chat_id=chat_id, text="✅ Українську тему встановлено!", message_id=query.message.message_id)

    else:
        await query.answer("Эта кнопка не для тебя :)")
    
@dp.callback_query_handler(vote_cb.filter(action='azeri'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]
    lab = labs.get_lab(from_user_id)
    if from_user_id == str(query.from_user.id):
        if lab.theme == "azeri":

            await bot.edit_message_text(chat_id=chat_id, text="У вас и так азербайджанская тема!", message_id=query.message.message_id)
            return
        else:
            lab.theme = "azeri"
            lab.save()
            await bot.edit_message_text(chat_id=chat_id, text="✅ Азербайджанская тема установлена!", message_id=query.message.message_id)

    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='hell'))
async def change_theme(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    chat_id = callback_data["chat_id"]
    lab = labs.get_lab(from_user_id)
    if from_user_id == str(query.from_user.id):
        if lab.theme == "hell":

            await bot.edit_message_text(chat_id=chat_id, text="У вас и так хеллоуинская тема!", message_id=query.message.message_id)
            return
        else:
            lab.theme = "hell"
            lab.save()
            await bot.edit_message_text(chat_id=chat_id, text="✅ Хеллоуинская тема установлена!", message_id=query.message.message_id)

    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.edited_message_handler()
async def other(message):
    save_message(message)
