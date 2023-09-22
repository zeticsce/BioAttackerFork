import os
import shutil
import asyncio
import requests
import random
import subprocess
import sys
import datetime
import re
import time
import math

from app import dp, bot, query, strconv, save_message, is_host
from config import MYSQL_HOST
from Labs import Labs

labs = Labs()

from commands.improvements import *
from commands.BioTop import *

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from math import ceil, floor

work_path = os.path.abspath(os.curdir)


async def skloneniye(num):
    names = ['день', 'дня', 'дней']
    n = num % 100
    if n >= 5 and n <= 20: return names[2]
    n = num % 10
    if n == 1: return names[0]
    if n >= 2 and n <= 4: return names[1]
    return names[2]


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

            try:
                dp.stop_polling()
                await dp.wait_closed()
                await bot.close()
            except: pass

            os.system(f"python {work_path}/app.py &")
            sys.exit(0)
        else: await message.reply(f"*Файлы не затронуты, перезагрузка не требуется!*", parse_mode="Markdown")
    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

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
    save_message(message)
    bio_infect = re.fullmatch(r"(биоеб)( \d{1,2})?( \S+)?", message.text.lower()) # регулярка на заражения
    if bio_infect != None:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab:  #проверка на наличие лабы
            attempts = int(bio_infect.group(2)) if bio_infect.group(2) != None else None # колво попыток
            if attempts == None: attempts = 1 # если колво попыток не определено, задавать 1

            if attempts > 10: # ограничивает колво попыток до 10
                await message.reply(text=f"👺 За раз максимум 10 попыток!",  parse_mode="Markdown")
                return

            if lab.patogens <= 0: # проверка на паты
                await message.reply(text=f"👺 Жди новых патогенов!",  parse_mode="Markdown")
                return

            victim_tag = bio_infect.group(3).strip().replace("tg://openmessage?user_id=", "").replace("https://t.me/", "").replace("@", "") if bio_infect.group(3) != None else None # тег жертвы из сообщения, None если его небыло

            victim = None # жертва (пиздец я всегда victum использовал)
            chance = random.random() # рандомыш от 0 до 1

            profit = 0
            pats = 0

            if message.reply_to_message: # нахождение айди жертвы при реплае
                if message.reply_to_message["from"]["is_bot"] == True: # фильтр на ботов
                    await message.reply("Нельзя заразить бота")
                    return
                victim = labs.get_user(message.reply_to_message["from"]["id"]) # обьект жертвы user_id, user_name, name


            if victim_tag != None: # если все хорошо, у нас останется victim_user, которая содержит айди юзера
                # в приоретете victim_tag, если будет реплай, то он сначала чекнет victim_tag, если он присутсвует, то будет бить его
                if re.fullmatch(r"[\w]+", victim_tag) == None: # проверка на валидность тега, нет ли там русских букв, спец символов и тд
                    await message.reply(text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                    return
                else:
                    victim = labs.get_user(victim_tag) # проверка есть ли он в базе
                    if victim == None:
                        await message.reply(text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                        return
                    elif is_host: # на хосте проверяет кд до следующего удара по юзеру
                        victim_in_list = lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{victim['user_id']}'")
                        if len(victim_in_list) != 0:
                            victim_in_list = victim_in_list[0]
                            if victim_in_list['from_infect'] > (int(time.time())-3600):
                                untill = math.floor((victim_in_list['from_infect'] - (int(time.time())-3600)) / 60) # колво минут
                                declination = "" # склонение минуту/минуты/минут
                                if untill <= 20:
                                    if untill == 1: declination = "минута"
                                    elif untill <= 4: declination = "минуты"
                                    else: declination = "минут"
                                else: 
                                    if untill%10 == 1: declination = "минута"
                                    elif untill%10 <= 4: declination = "минуты"
                                    else: declination = "минут"

                                await message.reply(text=f"👺 Ты сможешь заразить его повторно через {untill} {declination}!",  parse_mode="Markdown")
                                return 

            if victim == None: # тут происходит рандомный выбор жертвы
                if chance < 0.40: victim = labs.get_random_victum() # 40% абсолютно рандомный чел из бд
                elif chance < 0.40:
                    victims = lab.get_victums(params="ORDER BY RAND() LIMIT 4") # 40% перебив случайной жертвы
                    victim = None
                    for i in victims:
                        if i["from_infect"] <= int(time.time()) - (60*60): # проверка на кд
                            victim = i
                            break
                elif chance < 0.90: 
                    victim = query("SELECT * FROM `bio_attacker`.`labs` INNER JOIN `telegram_data`.`tg_users` ON `telegram_data`.`tg_users`.`user_id`=`bio_attacker`.`labs`.`user_id` ORDER BY RAND() LIMIT 1;")[0] # 10% жертва из уже созданных лаб
                    
                    """Штука снизу отвечает за исключение повторных заражений, но мне дико не нравится, что теперь постоянно пишет, что жертва не найдена (это пишется потому, что очень мало игроков)"""
                    # victim = victim if len(lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{victim['user_id']}' AND `victums{lab.user_id}`.`from_infect` <= {int(time.time()) - (60*60)}")) != 0 else None # проверка кд
                    
                else: victim = None # 10% неудачный поиск

            if victim == None:
                lab.save()
                del lab
                await message.reply(text=f"👺 Жертва не найдена!",  parse_mode="Markdown")
            else:

                attack_chance = random.random() # рандом от 0 до 1
                success = False
                    
                labOfVictim = labs.get_lab(victim['user_id']) # лаба жертвы

                if labOfVictim.has_lab: # если у жертвы есть лаба, то по другому пересчитывать шансы

                    delta = labOfVictim.immunity - lab.infectiousness # разница заразности и иммунитета

                    if delta <= 0: #если иммун жертвы меньше/равно заразности атакующего, то успех 100%
                        success = True
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1

                    # elif attempts > 1: # если применяет несколько попыток заражения, считается по экспоненте 1/(x^2)
                    #     pats = 0
                    #     for i in range(attempts):
                    #         if lab.patogens <= 0: break
                    #         lab.all_operations += 1
                    #         lab.patogens -= 1
                    #         pats += 1
                    #         success = random.random()
                    #         if success: break

                else:
                    if attempts > 1: # если попыток задано больше 1, то он увеличивает шанс на поражение :)
                        pats = 0
                        for i in range(attempts):
                            if lab.patogens <= 0: break
                            lab.all_operations += 1
                            lab.patogens -= 1
                            pats += 1
                            success = random.random() > 0.3
                            if success: break

                    elif attack_chance < 0.2: # 20% шанс на неудачу при атаке, success остается False по умолчанию
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1
                    else: # если все другие иф не сработали, то значит успешно пробил 
                        success = True
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1
                if success: # если по всем шансам прошло успешно, то идет дальше отрабатывать жертву 
                    if labOfVictim.has_lab:

                        labOfVictim.all_issue += 1

                        profit = int(labOfVictim.bio_exp / 10)
                        profit = 1 if profit < 1 else profit # мин профит 1

                        labOfVictim.bio_exp -= int(labOfVictim.bio_exp / 10)
                        labOfVictim.bio_exp = 1 if labOfVictim.bio_exp < 1 else labOfVictim.bio_exp # чтобы не ушло в 0 или -

                        labOfVictim.save()

                    else: profit = random.randint(1, 100)

                    lab.save_victum(victim['user_id'], profit)
                    lab.save()

                    text = f"😎 Вы подвергли заражению пользователя "
                    text += f"[{victim['name']}](tg://openmessage?user_id={victim['user_id']})\n\n"
                    text += f"🧪 Затрачено патогенов `{pats}`.\n"
                    text += f"☠️ Заражение на `{lab.mortality}` "      
                    text += await skloneniye(lab.mortality)
                    text += ".\n"
                    text += f"☣️ `{profit}` био-опыта."

                    await message.reply(text=text, parse_mode="Markdown")
                        
                    ''' Отправка уведомления '''

                    if labOfVictim.has_lab:
                        chat = labOfVictim["virus_chat"]
                        text = ""
                        chance = random.randint(1, 100)

                        if lab.security < labOfVictim.security:

                            if pats > 1:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\nБыло произведено {pats} попыток вашего заражения\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            else:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            await bot.send_message(chat_id=chat, text=text, parse_mode="Markdown")
                            return

                        if lab.security > labOfVictim.security :
                            
                            sp = (lab.infectiousness - labOfVictim.security)**2

                            if chance > sp:
                                
                                if pats > 1:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\nБыло произведено {pats} попыток вашего заражения\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                                else:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            else:
                                
                                if pats > 1:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\nБыло произведено {pats} попыток вашего заражения\n\n_Вы потеряли ☣️ {profit} опыта_'
                                else:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            
                            await bot.send_message(chat_id=chat, text=text, parse_mode="Markdown")

                else:
                    await message.reply(text=f"👺 Попытка заразить [{victim['name']}](tg://openmessage?user_id={victim['user_id']}) провалилась!\nВероятно у вашего вируса слабая заразность.",  parse_mode="Markdown")
                    
                    labOfVictim = labs.get_lab(victim['user_id'])
                    if labOfVictim.has_lab:
                        labOfVictim.all_issue += 1
                        labOfVictim.save()

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
            prevented_issue     колличество успешных попыток заразить этого юзера
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
            qualification_count = qualification_count if qualification_count + lab.qualification <= 60 else lab.qualification - qualification_count
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

        await bot.send_message(chat_id=message.chat.id, 
            text=text, 
            reply_to_message_id=message.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        lab.save() 

    if message.text.lower() == "био":
        await message.reply(f"*Бот на месте*", parse_mode='Markdown')


    if message.text.lower().startswith("+вирус "):

        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            patName = message.text[7::].strip()

            if len(patName) > 50:
                await message.reply("Длина названия вируса не может быть больше 50 символов")
                return
            if len(patName) == 0:
                await message.reply("Вирус не может быть пустым!")
                return
            if re.fullmatch(r"([a-zA-Zа-яА-Я0-9_\s,.!?]*)", patName) == None: # Проверка на валидность имени патогена
                await message.reply("В вирусе не может быть недопустимых символов!")
                return

            lab.patogen_name = patName
            lab.save()

            await message.reply("✅ Название патогена успешно обновлено!")

    if message.text.lower() in ("биожертвы", "биоежа"):
        lab = labs.get_lab(message['from']['id'])
        text = f'Жертвы игрока [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})\n\n'
        profit = 0

        count = 0
        for item in list(reversed(lab.get_victums())):
            if item['until_infect'] > int(time.time()):
                profit += item["profit"]
                name = strconv.deEmojify(item["name"])
                until = datetime.datetime.fromtimestamp(item['until_infect']).strftime("%d.%m.%Y")
                text += f'{count + 1}. [{strconv.escape_markdown(name)}](tg://openmessage?user_id={item["user_id"]}) | _+{item["profit"]}_ | до {until}\n'

                count += 1
                if count == 50: break
        
        text += f'\n*Общая прибыль:* _+{profit} био-ресурсов 🧬_'

        await message.reply(text=text, parse_mode="Markdown")

    if message.text.lower() in ("биоферма", "биофарма", "биофа", "майн"):
        
        lab = labs.get_lab(message['from']['id'])
        profit = random.randint(20, 200)

        lab.coins += profit
        lab.save()

        text = f'Вы успешно пофармили и получили {profit} коинов 💰!'

        await message.reply(text=text, parse_mode="Markdown")

    if message.text.lower() in ("биомеш", "биомешок", "биобаланс", "коины"):

        lab = labs.get_lab(message['from']['id'])

        text = f'Мешок игрока [{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})\n\n'\
               f'Коины: _{lab.coins}_ 💰\n' \
               f'Био-коины: _{lab.bio_valuta}_ 🥑'

        await message.reply(text=text, parse_mode="Markdown")

    
    if message.text.lower() == "биохелп":
        await message.reply(f"[Все команды бота](https://telegra.ph/Komandy-dlya-igry-v-Bio-CHma-09-15-2)", parse_mode="Markdown")





@dp.edited_message_handler()
async def other(message):
    save_message(message)