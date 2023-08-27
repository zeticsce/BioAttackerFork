import os
import shutil
from app import dp, bot, query
from config import MYSQL_HOST

from Labs import Labs
import asyncio
import requests

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
        if message['from']['id'] in labs.has_lab_users:
            ran_user = labs.get_random_victum()
            await message.reply(text=f"{ran_user['user_id']}, {ran_user['name']}")
            # labs.save_victum(message['from']['id'], 2563739, 100)

    if message.text == "биолаб":

        """
            Команда вывода лаборатории юзера
        """

        lab = labs.get_lab(message['from']['id']) # Вернет None, если лаба не найдена
        if lab == None: lab = labs.create_lab(message['from']['id'])

        # дальше лаба точно существует и полностью содежится в lab
        """
            поле                описание

            user_id             юзер айди пользователя
            name                имя пользователя
            user_name           юз пользователя
            corp корп           айди пользователя
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
        print(lab)
        lab.save() 

        

