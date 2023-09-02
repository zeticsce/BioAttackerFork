import os
import shutil
import asyncio
import requests
import random
import subprocess
import sys
import datetime


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

        pull_result = subprocess.Popen(["git", "pull", "/home/bots/BioAttacker/"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
        output, errors = pull_result.communicate(input="Hello from the other side!")
        pull_result.wait()
        await bot.edit_message_text(f"🪛 *Ожидаем клонирования...\nРезультат:*\n`{output}`", git_message.chat.id, git_message.message_id, parse_mode="Markdown")
        await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()
        
        """ИЗМЕНЕНИЯ СУЩЕСТВУЮТ"""

        os.system(f"python {work_path}/app.py &")
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
    if "биоеб" in message.text.lower().split(" ")[0]:
        
        """
                Команда заражения
        """
        
        if len(message.text.split(" ")) == 1:
            
            lab = labs.get_lab(message['from']['id'])
            if lab.has_lab: 
                if lab.patogens > 0:
                    import chances
                    '''
                        casual - случайный юзер
                        victim - жертва
                        bioattacker - игрок

                    '''
                    karma = ("casual", "victim")
                    
                    random_choice = random.choice(karma)
                    ran_user = int()

                    if random_choice == "casual":
                        ran_user = labs.get_random_victum()

                    elif random_choice == "victim":
                        ran_user = lab.get_victums(params="ORDER BY RAND() LIMIT 1")[0]

                    else:
                        pass

                    chance = chances.get_chance()

                    if chance == 1:

                        lab.all_operations += 1
                        lab.patogens -= 1

                        lab.save()
                        await message.reply(text=f"👺 Попытка заразить [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']}) провалилась!\nВероятно у вашего вируса слабая заразность.",  parse_mode="Markdown")
                    
                    else:
                        profit = random.randrange(1, 100)
                        lab.save_victum(ran_user['user_id'], profit)
                        lab.all_operations += 1
                        lab.patogens -= 1

                        lab.save()

                        await message.reply(text=f"😎 Вы подвергли заражению пользователя [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']})\nИ получили за это {profit} ☣️", parse_mode="Markdown")
                
                else: await message.reply(text=f"🧪 У Вас недостаточно патогенов!", parse_mode="Markdown")
            
        elif len(message.text.split(" ")) == 2:
            ''' биоеб @username or @user_id '''

            lab = labs.get_lab(message['from']['id'])

            if lab.patogens > 0:
                
                import chances
                
                ran_user = int()

                text_message = message.text.split(" ")
                # await message.reply(str(text_message))

                if text_message[1][0] == "@":
                    ran_user = labs.get_user(text_message[1][1::])
                
                else:
                    ran_user = labs.get_user(text_message[1])

                
                ''' Если юзер существует '''
                if str(ran_user).lower() not in ("none", "null"):
                    
                    
                    chance = chance = chances.get_chance()
                    if chance == 1:

                        lab.all_operations += 1
                        lab.patogens -= 1

                        lab.save()
                        await message.reply(text=f"👺 Попытка заразить [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']}) провалилась!\nВероятно у вашего вируса слабая заразность.",  parse_mode="Markdown")
                    else:
                        profit = random.randrange(1, 100)
                        lab.save_victum(ran_user['user_id'], profit)
                        lab.all_operations += 1
                        lab.patogens -= 1

                        lab.save()
                        await message.reply(text=f"😎 Вы подвергли заражению пользователя [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']})\nИ получили за это {profit} ☣️", parse_mode="Markdown")

                else:
                    await message.reply("Такого пользователя не существует!")

            else: await message.reply(text=f"🧪 У Вас недостаточно патогенов!", parse_mode="Markdown")

        elif len(message.text.split(" ")) == 3:

            ''' биоеб (@user_id) (attempts) '''

            lab = labs.get_lab(message['from']['id'])

            if lab.patogens > 0:
                ran_user = int()

                text_message = message.text.split(" ")
                # await message.reply(str(text_message))

                if text_message[1][0] == "@":
                    ran_user = labs.get_user(text_message[1][1::])
                
                else:
                    ran_user = labs.get_user(text_message[1])
            
                if str(ran_user).lower() not in ("none", "null"):
                    
                    if int(text_message[2]) > 10:
                        await message.reply("Максимальное кол-во попыток за раз — 10")

                    else:
                        
                        import chances

                        for i in range(int(text_message[2])):
                            chance = chances.get_chance(params=1)

                            if chance == 1:
                                lab.patogens -= 1
                                lab.all_operations += 1
                                lab.save()
                            else:
                                profit = random.randrange(1, 100)
                                lab.save_victum(ran_user['user_id'], profit)
                                lab.all_operations += 1
                                lab.patogens -= 1

                                lab.save()
                                
                                await message.reply(text=f"😎 Вы подвергли заражению пользователя [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']}) c {i + 1} попытки!\nИ получили за это {profit} ☣️", parse_mode="Markdown")

                                break

                else:
                    await message.reply("Такого пользователя не существует!")
            
            else: await message.reply(text=f"🧪 У Вас недостаточно патогенов!", parse_mode="Markdown")

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
        text += f'🧪 Доступных патогенов: {lab.patogens} из {lab.all_patogens}\n'

        ''' Уровень разработки '''  
        text += f'👨🏻‍🔬 Уровень разработки: {lab.qualification} (время в минутах)\n\n'
        
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
        text += f'😷 Спецопераций: {lab.suc_operations}/{lab.all_operations}\n'
        text += f'🥽 Предотвращены: {lab.prevented_issue}/{lab.all_issue}\n\n'


        await bot.send_message(chat_id=message.chat.id, 
            text=text, 
            reply_to_message_id=message.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        lab.save() 

        

