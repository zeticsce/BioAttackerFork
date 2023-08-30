import os
import shutil
import asyncio
import requests
import random

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

        os.system("git pull https://github.com/kawasaji/BioAttacker")
        await message.reply("🪛 Команда на клонирование гит репозитория отправлена")
        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        exit()

    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        exit()

@dp.message_handler(commands=["export", "exp"])
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
    if message.text == "биоеб":
        """
            Команда заражения
        """
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: 
            '''Получает рандомного пользователя из базы данных'''
            ran_user = labs.get_random_victum()

            # Использовать labs.get_user(tag), если пользователь решил заразить по тегу, если юзер не найден, вернет None

            '''
                Сохранение жертвы

                Метод lab.save_victum(victum_id, profit) принимает два параметра, айди жертвы и профит с жертвы

                Еще необходимо изменить вручную:

                    lab.all_operations (возможно было несколько неудачных попыток в одном заражении, надо записать)
                    lab.patogens (возможно будет затрачено несколько патогенов при заражении)
            
            '''

            '''Пример с сохранением жертв'''
            if lab.patogens > 0:
                profit = random.randrange(1, 100)
                lab.save_victum(ran_user['user_id'], profit)
                lab.all_operations += 1
                lab.patogens -= 1

                lab.save()


                await message.reply(text=f"Вы подвергли заражению пользователя [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']}), получив за это {profit} био!", parse_mode="Markdown")
            else: await message.reply(text=f"Попытка заразить юзера [{ran_user['name']}](tg://openmessage?user_id={ran_user['user_id']}) провалилась... У Вас недостаточно патогенво!", parse_mode="Markdown")

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

        

