import os
import shutil
import requests
import random
import subprocess
import sys
import datetime
import re
import time

from app import dp, bot, query, strconv, save_message
from config import MYSQL_HOST
from Labs import Labs
from libs.Statistics import Statistics

statistics = Statistics()
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
from commands.marketplace import *


from aiogram import types
from aiogram.types import InputFile

work_path = os.path.abspath(os.curdir)

is_host = requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST

if is_host: # Необходимо, потому что команда /git и /restar работает только на хостинге
    @dp.message_handler(commands=["git"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        git_message = await bot.send_message(message.chat.id, "🪛 *Ожидаем клонирования...*", parse_mode="Markdown")

        pull_result = subprocess.Popen(["git", "pull", "https://github.com/kawasaji/BioAttacker"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
        output, errors = pull_result.communicate(input="Hello from the other side!")
        pull_result.wait()
        await bot.edit_message_text(f"🪛 *Ожидаем клонирования...*\n```Output\n{output}```", git_message.chat.id, git_message.message_id, parse_mode="Markdown")
        if "Already up to date.\n" != output:
            await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

            try: dp.stop_polling()
            except: pass
            try: await dp.wait_closed()
            except: pass

            os.system(f"sudo systemctl restart biobot")
        else: await bot.send_message(message.chat.id, f"*Файлы не затронуты, перезагрузка не требуется!*", parse_mode="Markdown" )
    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

        try: dp.stop_polling()
        except: pass
        try: await dp.wait_closed()
        except: pass

        os.system(f"sudo systemctl restart biobot")

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS, types.ContentType.LEFT_CHAT_MEMBER])
async def user_joined_chat(message: types.Message):
    if message.chat.id == -1001875205082:
    # if message.chat.id == -1001678995999:
        count = (await bot.get_chat_members_count(message.chat.id))
        count_str = strconv.skl(count)
        count_str = count_str[0].upper() + count_str[1:]    
        forms=('азербайджанец', 'азербайджанца', 'азербайджанцев')
        form = ''
        if count % 100 in (11, 12, 13, 14):
            form = forms[2]
        else:
            remainder = count % 10
            if remainder == 1:
                form = forms[0]
            elif 2 <= remainder <= 4:
                form = forms[1]
            else:
                form = forms[2]
        await bot.set_chat_title(message.chat.id, title=f"{count_str} {form}")

@dp.message_handler(commands=["exit"], commands_prefix='.')
async def hi_there(message: types.message):
    if message['from']['id'] not in [780882761, 1058211493]: return
    await bot.send_message(message.chat.id, f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
    if is_host: os.system(f"sudo systemctl stop biobot")
    else: sys.exit(0)

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
    if message.text in ('', '/'):
        try:
            await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path), filename='BioAttacker.zip'))
        except: await bot.send_message(message.chat.id, f"🪛 Произошла ошибка, возможно архив слишком тяжелый...")
        os.remove(work_path + "/files.zip")
    else:
        if not message.text.startswith('/'): message.text = "/" + message.text
        if os.path.exists(work_path + message.text):
            if not os.path.isfile(work_path + message.text):
                try:
                    await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path + message.text),  filename=message.text + ".zip"))
                except: await bot.send_message(message.chat.id, f"🪛 Произошла ошибка, возможно архив слишком тяжелый...")
                os.remove(work_path + "/files.zip")
            else: 
                try:
                    await bot.send_document(message.chat.id,  InputFile(work_path + message.text, filename=message.text))
                except: await bot.send_message(message.chat.id, f"🪛 Произошла ошибка, возможно файл слишком тяжелый...")
        else: await bot.send_message(message.chat.id, f"🪛 Путь `{message.text}` не найден")

@dp.message_handler(content_types=["text"]) 
async def handler(message: types.message):

    if message.text.lower() == "био":
        await bot.send_message(message.chat.id, f"*Бот на месте*", parse_mode='Markdown')

    if message.text.lower() == "/start":
        text = random.choice(start_text)
        text += "[Все команды бота](https://teletype.in/@kawasaji/commands_of_bio-cmo)"
        await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")

    if message.text.lower() == "-вирус" and not message.forward_from:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.patogen_name = None
            lab.save()

            await bot.send_message(message.chat.id, "✅ Название патогена удалено.")

    if message.text.lower() == "-лаб" and not message.forward_from:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.lab_name = None
            lab.save()

            await bot.send_message(message.chat.id, "✅ Имя лаборатории удалено.")

    if message.text.lower().startswith("+лаб ") and not message.forward_from:

        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            labName = message.text[5::].strip()

            if len(labName) > 30:
                await bot.send_message(message.chat.id, "Длина имени лаборатории не может быть больше 30 символов")
                return
            if len(labName) == 0:
                await bot.send_message(message.chat.id, "Имя лаборатории не может быть пустым!")
                return
            if re.fullmatch(r"([a-zA-Zа-яА-Я0-9_\s,.!?]*)", labName) is None: # Проверка на валидность имени
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

    if message.text.lower().startswith("+вирус ") and not message.forward_from:

        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            patName = message.text[7::].strip()

            if len(patName) > 50:
                await bot.send_message(message.chat.id, "Длина названия вируса не может быть больше 50 символов")
                return
            if len(patName) == 0:
                await bot.send_message(message.chat.id, "Вирус не может быть пустым!")
                return
            if re.fullmatch(r"([a-zA-Zа-яА-Я0-9_\s,.!?]*)", patName) is None: # Проверка на валидность имени патогена
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

    if message.text.lower() in ["+вирусы", "+сбчат"] and not message.forward_from:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            lab.virus_chat = message.chat.id
            lab.save()
            await bot.send_message(message.chat.id, text="Сообщения службы безопасности перенесены в этот чат", parse_mode="Markdown")

    if message.text.lower() in ("биожертвы", "биоежа") and not message.forward_from:
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

    if message.text.lower() in ("биоферма", "биофарма", "биофа", "майн") and not message.forward_from:

        lab = labs.get_lab(message['from']['id'])
        if not lab.has_lab: return
        if lab.last_farma + (60*60*4) > int(time.time()):
            minuts = 60*4 - int((int(time.time()) - lab.last_farma)/60)
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

        profit = random.randint(20, 100)

        lab.coins += profit
        lab.last_farma = int(time.time())
        lab.save()

        text = f'Вы успешно пофармили и получили {profit} коинов 💰!'

        await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")

    if message.text.lower() in ("биомеш", "биомешок", "биобаланс", "коины") and not message.forward_from:

        lab = labs.get_lab(message['from']['id'])

        text = f'Мешок игрока [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})\n\n'\
               f'Коины: _{lab.coins}_ 💰\n' \
               f'Био-коины: _{lab.bio_valuta}_ 🥑'

        await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")


    if message.text.lower() == "биохелп":
        await bot.send_message(message.chat.id, f"[Все команды бота](https://teletype.in/@kawasaji/commands_of_bio-cmo)", parse_mode="Markdown")
    if message.text.lower() == "влад": 
        await bot.send_message(message.chat.id, text='лох<a href="tg://user?id=5770061336">\xad</a>', parse_mode="HTML", disable_web_page_preview=True)

    reg = re.fullmatch(r'[.!/][\s]?ид(\s([@./:\\a-z0-9_?=]+))?', message.text.lower())
    if reg is not None and not message.forward_from:
        url = reg.group(2)
        name = None
        if url is not None:
            clear_url = url.replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
            if re.fullmatch(r"[a-z0-9_]+", clear_url) is not None:
                user = labs.get_user(clear_url)
                if user is not None:
                    name = strconv.normalaze(user['name'], str(user['user_id']))
                    user_id = user['user_id']
        elif message.reply_to_message:
            name = strconv.normalaze(message.reply_to_message.from_user.first_name, str(message.reply_to_message.from_user.id))
            user_id = message.reply_to_message.from_user.id
        else:
            name = strconv.normalaze(message.from_user.first_name, str(message.from_user.id))
            user_id = message.from_user.id
        if name is not None:
            text = f'🌊 Айди игрока <a href="tg://openmessage?user_id={user_id}">{name}</a> равен <code>@{user_id}</code>'
            await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_to_message_id=message.message_id)
        elif url is not None:
            await bot.send_message(chat_id=message.chat.id, text="Юзер не найден!", parse_mode="HTML", reply_to_message_id=message.message_id)

    # if message.text.startswith(".т"):
    #     reg = re.fullmatch(r".т(\s[a-zа-я0-9\s]+)?", message.text.lower())
    #     if reg == None: return
    #     if reg.group(1) == None:
    #         await bot.send_message(message.chat.id, "Что пожелаете сделать?)", reply_markup=first_change_theme_btn(message, message.from_user.id))
    #     else:
    #         th = reg.group(1).strip()
    #         if th in theme:
    #             lab = labs.get_lab(message.from_user.id)
    #             if lab.theme == th:
    #                 erpl = f"У вас уже стоит {theme[th]['theme_name'].lower()}"
    #             else:
    #                 lab.theme = th
    #                 erpl = f"✅ {theme[th]['theme_name']} установлена"

    #             await message.reply(erpl)
    #             lab.save()

    check = re.fullmatch(r'[.!/][\s]?чек(\s([@./:\\a-z0-9_?=]+))?', message.text, re.I)
    if check is not None and not message.forward_from:
        lab = labs.get_lab(message.from_user.id)

        if lab.has_lab:
            url = check.group(2)
            name = None
            user = None
            if url is not None:
                clear_url = url.replace(" ", "").replace("@", "").replace("tg://openmessage?user_id=", "").replace("tg://user?id=", "").replace("https://t.me/", "").replace("t.me/", "")
                if re.fullmatch(r"[a-z0-9_]+", clear_url) is not None:
                    user = labs.get_user(clear_url)
            elif message.reply_to_message:
                user = labs.get_user(message.reply_to_message.from_user.id)

            if user is None:
                await message.reply("Жертва не найдена")
                return

            bebra = query(f"SELECT * FROM `bio_attacker_data`.`victums{lab.user_id}` WHERE user_id = {user['user_id']}")
            if len(bebra) == 0:
                await message.reply("Жертва не найдена")
                return
            bebra = bebra[0]
            until = datetime.datetime.fromtimestamp(bebra['until_infect']).strftime("%d.%m.%Y")
            if bebra['until_infect'] > time.time():
                await message.reply(f"Жертва `@{bebra['user_id']}` приносит вам {bebra['profit']} ☣️ до {until}", parse_mode='Markdown')
            else:
                await message.reply("Жертва не найдена")




vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')


@dp.edited_message_handler()
async def other(message):
    save_message(message)
