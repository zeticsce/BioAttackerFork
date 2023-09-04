import os
import shutil
import asyncio
import requests
import random
import subprocess
import sys
import datetime
import re

from app import dp, bot, query, strconv
from config import MYSQL_HOST
from Labs import Labs

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


work_path = os.path.abspath(os.curdir)
labs = Labs()


if requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST: # Необходимо, потому что команда /git и /restar работает только на хостинге
    @dp.message_handler(commands=["git"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        git_message = await message.reply("🪛 *Ожидаем клонирования...*", parse_mode="Markdown")

        pull_result = subprocess.Popen(["git", "pull", "https://github.com/kawasaji/BioAttacker"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
        output, errors = pull_result.communicate(input="Hello from the other side!")
        pull_result.wait()
        await bot.edit_message_text(f"🪛 *Ожидаем клонирования...\nРезультат:*\n`{output}`", git_message.chat.id, git_message.message_id, parse_mode="Markdown")
        if "Already up to date.\n" != output:
            await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

            dp.stop_polling()
            await dp.wait_closed()
            await bot.close()

            os.system(f"python {work_path}/app.py &")
        else: await message.reply(f"*Файлы не затронуты, перезагрузка не требуется!*", parse_mode="Markdown")
    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        sys.exit(0)

@dp.message_handler(commands=["exit"], commands_prefix='.')
async def hi_there(message: types.message):
    if message['from']['id'] not in [780882761, 1058211493]: return
    await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
    sys.exit(0)

@dp.message_handler(commands=["start"], commands_prefix='!/.')
async def hi_there(message: types.message):
    await message.reply("Привет! *** придумать текст ***")


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
        print(message)
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
        else: await message.reply(f"🪛 Путь `{message.text}` не найден")


@dp.message_handler(content_types=['text']) 
async def handler(message: types.message):
    bio_infect = re.fullmatch(r"(биоеб)( \d{1,2})?( \S+)?", message.text.lower()) # регулярка на заражения
    if bio_infect != None:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab:  

            attempts = int(bio_infect.group(2)) if bio_infect.group(2) != None else None # колво попыток
            victim_tag = bio_infect.group(3).strip().replace("tg://openmessage?user_id=", "").replace("https://t.me/", "").replace("@", "") if bio_infect.group(3) != None else None # тег жертвы из сообщения, None если его небыло

            victim = None # жертва (пиздец я всегда victum использовал)
            chance = random.random() # рандомыш от 0 до 1

            profit = 0
            pats = 0  

            if victim_tag != None: # если все хорошо, у нас останется victim_user, которая содержит айди юзера
                if re.fullmatch(r"[\w]+", victim_tag) == None: # проверка на валидность тега, нет ли там русских букв, спец символов и тд
                    await message.reply(text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                    return
                else:
                    victim = labs.get_user(victim_tag) # проверка есть ли он в базе
                    if victim == None:
                        await message.reply(text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                        return

            if attempts == None: attempts = 1 # если колво попыток не определено, задавать 1
            
            if attempts > 10: # ограничивает колво попыток до 10
                await message.reply(text=f"👺 За раз максимум 10 попыток!",  parse_mode="Markdown")
                return

            if lab.patogens <= 0: # проверка на паты
                await message.reply(text=f"👺 Жди новых патогенов!",  parse_mode="Markdown")
                return


            if victim == None:
                if chance < 0.40: victim = labs.get_random_victum() # 40% абсолютно рандомный чел из бд
                elif chance < 0.40: victim = lab.get_victums(params="ORDER BY RAND() LIMIT 1")[0] # 40% перебив случайной жертвы
                elif chance < 0.90: victim = query("SELECT * FROM `bio_attacker`.`labs` INNER JOIN `telegram_data`.`tg_users` ON `telegram_data`.`tg_users`.`user_id`=`bio_attacker`.`labs`.`user_id` ORDER BY RAND() LIMIT 1;")[0] # 10% жертва из уже созданных лаб
                else: victim = None # 10% неудачный поиск

            if victim == None:
                lab.save()
                await message.reply(text=f"👺 Жертва не найдена!",  parse_mode="Markdown")
            else:

                attack_chance = random.random() # рандом от 0 до 1
                success = False

                if attempts > 1: # если попыток задано больше 1, то он увеличивает шанс на поражение
                    pats = 0
                    for i in range(attempts):
                        if lab.patogens <= 0: break
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats += 1
                        success = random.random() > 0.3
                        if success: break

                elif attack_chance < (0.2): # 20% шанс на неудачу при атаке, success остается False по умолчанию
                    lab.all_operations += 1
                    lab.patogens -= 1
                    pats = 1
                else:
                    success = True
                    lab.all_operations += 1
                    lab.patogens -= 1
                    pats = 1
                if success:
                    profit = random.randrange(1, 100)
                    lab.save_victum(victim['user_id'], profit)
                    lab.save()
                    if pats > 1:
                        await message.reply(text=f"😎 Вы подвергли заражению пользователя [{victim['name']}](tg://openmessage?user_id={victim['user_id']})\nИ получили за это {profit} ☣️\n\nатрачено патогенов: {pats}", parse_mode="Markdown")
                    else: await message.reply(text=f"😎 Вы подвергли заражению пользователя [{victim['name']}](tg://openmessage?user_id={victim['user_id']})\nИ получили за это {profit} ☣️", parse_mode="Markdown")

                    ''' Отправка уведомления '''

                    try:
                        chat = labs.get_lab(victim["user_id"])["virus_chat"]
                        text = ""
                        chance = random.random()

                        if chance < 0.4:
                            attacker = labs.get_lab(message['from']['id'])
                            if pats > 1:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{attacker["name"]}](tg://openmessage?user_id={victim["user_id"]}) подверг вас заражению.\nБыло произведено {pats} попыток вашего заражения\n\nНазвание патогена: `{attacker["patogen_name"]}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            else:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{attacker["name"]}](tg://openmessage?user_id={victim["user_id"]}) подверг вас заражению.\n\nНазвание патогена: `{attacker["patogen_name"]}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                        
                        else:
                            attacker = labs.get_lab(message['from']['id'])
                            if pats > 1:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{attacker["patogen_name"]}`\nБыло произведено {pats} попыток вашего заражения\n\n_Вы потеряли ☣️ {profit} опыта_'
                            else:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{attacker["patogen_name"]}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                        
                        
                        await bot.send_message(chat_id=chat, text=text, parse_mode="Markdown")
                    
                        
                    except Exception as e:
                        print(e)
                else:
                    await message.reply(text=f"👺 Попытка заразить [{victim['name']}](tg://openmessage?user_id={victim['user_id']}) провалилась!\nВероятно у вашего вируса слабая заразность.",  parse_mode="Markdown")
                    lab.save()

    if message.text == "биолаб":

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
            immunity уровень    иммунитета
            mortality уровень   летальности
            security уровень    безопасноси

            bio_exp             био опыт
            bio_res             био ресурс

            all_operations      колличество операций заражения
            suc_operations      колличество успешных операций заражения
            all_issue           колличество всех попыток заразить этого юзера
            prevented_issue     колличество успешных попыток заразить этого юзера
            victims             колличество жертв
            disease             колличество болезней
            coins               колличество коинов
            bio_valuta          колличество какой либо валюты / ирисок

            last_farma          время последнего использования комманды ферма
            last_issue          время последнего заражения

            virus_chat          чат айди, куда отправлять вирусы (None если в лс)
        """

        '''  Название вируса '''
        text = f'🦠 Информация о вирусе: {lab.patogen_name if lab.patogen_name != None else "неизвестно"}\n\n'

        '''  Владелец лабы '''
        owner_link = f'https://t.me/{lab.user_name}' if lab.user_name != None else f'tg://openmessage?user_id={lab.user_id}'
        text += f'👺 Владелец: [{lab.name}]({owner_link})\n'

        ''' Корпорация '''
        if lab.corp != None: text += f'🏢 Относится к корпорации: [{lab.corp_name}](tg://openmessage?user_id={lab.corp_owner_id})\n\n'
        else: text += f'\n'
        
        ''' Количество патогенов ''' 
        text += f'🧪 Патогенов: {lab.patogens} из {lab.all_patogens}\n'

        ''' Уровень разработки '''  
        text += f'👨🏻‍🔬 Разработка: {lab.qualification} ({61 - lab.qualification} мин.) \n\n'
        
        ''' Навыки '''
        text += f'🔬 **НАВЫКИ:**\n'
        text += f'🦠 Заразность: {lab.infectiousness} ур.\n'
        text += f'🛡 Иммунитет: {lab.immunity} ур.\n'
        text += f'☠️ Летальность: {lab.mortality} ур.\n'
        text += f'🕵️‍♂️ Безопасность: {lab.security} ур.\n\n'

        ''' Данные ''' 
        text += f'⛩ **ДАННЫЕ:**\n'
        text += f'☣️ Био-опыт: {strconv.num_to_str(lab.bio_exp)}\n'
        text += f'🧬 Био-ресурс: {strconv.num_to_str(lab.bio_res)}\n'
        text += f'😷 Спецопераций: {lab.suc_operations}/{lab.all_operations} (`{round(100 * int(lab.suc_operations) / int(lab.all_operations) )}%`)\n'
        try:
            text += f'🥽 Предотвращены: {lab.prevented_issue}/{lab.all_issue} (`{round(100* int(lab.prevented_issue) / int(lab.all_issue))}`)\n\n'
        except ZeroDivisionError:
            text += f'🥽 Предотвращены: {lab.prevented_issue}/{lab.all_issue} (`0%`)\n\n'

        await bot.send_message(chat_id=message.chat.id, 
            text=text, 
            reply_to_message_id=message.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        lab.save() 

        

