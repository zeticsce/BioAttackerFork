'''

Модуль с прокачками лаб

'''



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
import calculate

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from math import ceil, floor

work_path = os.path.abspath(os.curdir)
labs = Labs()

@dp.message_handler(content_types=['text'])
async def improve(message: types.Message):
    save_message(message)
    lab = labs.get_lab(message['from']['id'])



    ''' ПРОКАЧКА ПАТОГЕНОВ '''

    if message.text.lower().startswith("+пат ") or message.text.lower().startswith("+патоген "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_patogens = lab.all_patogens

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return
                    total_cost = calculate.pt(current_patogens, (current_patogens+level))
                    total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                    text += f"Ваш текущий уровень патогена: `{current_patogens}` 🧪\n"
                    text += f"Улучшение на _+{level}_ будет стоить: "
                    text += f"`{total_cost}` 🧬\n\n"
                    text += f"*Чтобы подвердить улучшение напишите:* `++патоген {level}`"

                    await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  
        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    elif message.text.lower().startswith("++пат ") or message.text.lower().startswith("++патоген "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_patogens = lab.all_patogens

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    current_balance = lab.bio_res
                    total_cost = calculate.pt(current_patogens, (current_patogens+level))
                    if current_balance < total_cost:
                        await message.reply("*У вас недостаточно био-ресурсов!*", parse_mode="Markdown")

                    else:
                        lab.bio_res -= total_cost
                        lab.all_patogens += level
                        lab.patogens += level
                        lab.save()
                        total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                        text += f"Вы успешно добавили `{level}` патогенов!\n"
                        text += f"С баланса снято `{total_cost}` био-ресурсов 🧬"
                        await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  

        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    ''' ПРОКАЧКА КВАЛИФИКАЦИИ '''
    
    if message.text.lower().startswith("+квала ") or message.text.lower().startswith("+квалификация "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_qualification = lab.qualification

            if current_qualification == 60:
                await message.reply("У вас и так максимальный уровень квалификации -_-")
                return 

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if current_qualification + level > 60:
                        await message.reply("Квалификацию можно прокачать только до 60 уровня!")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    total_cost = calculate.ql(current_qualification, (current_qualification+level))
                    total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                    text += f"Ваш текущий уровень квалификации: `{current_qualification}` 👨🏻‍🔬\n"
                    text += f"Улучшение на _+{level}_ будет стоить: "
                    text += f"`{total_cost}` 🧬\n\n"
                    text += f"*Чтобы подвердить улучшение напишите:* `++квала {level}`"

                    await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  
        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    elif message.text.lower().startswith("++квала ") or message.text.lower().startswith("++квалификация "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_qualification = lab.qualification

            if current_qualification == 60:
                await message.reply("У вас и так максимальный уровень квалификации -_-")
                return 

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if current_qualification + level > 60:
                        await message.reply("Квалификацию можно прокачать только до 60 уровня!")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    current_balance = lab.bio_res
                    total_cost = calculate.ql(current_qualification, (current_qualification+level))
                    if current_balance < total_cost:
                        await message.reply("*У вас недостаточно био-ресурсов!*", parse_mode="Markdown")

                    else:
                        lab.bio_res -= total_cost
                        lab.qualification += level
                        lab.save()
                        total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                        text += f"Вы успешно добавили `+{level}` к квалификации!\n"
                        text += f"С баланса снято `{total_cost}` био-ресурсов 🧬"
                        await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  

        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    ''' ПРОКАЧКА ЗАРАЗНОСТИ '''

    if message.text.lower().startswith("+зар ") or message.text.lower().startswith("+заразность "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_infectiousness = lab.infectiousness

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return
                    total_cost = calculate.zz(current_infectiousness, (current_infectiousness+level))
                    total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                    text += f"Ваш текущий уровень заразности: `{current_infectiousness}` 🦠\n"
                    text += f"Улучшение на _+{level}_ будет стоить: "
                    text += f"`{total_cost}` 🧬\n\n"
                    text += f"*Чтобы подвердить улучшение напишите:* `++зар {level}`"

                    await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  
        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    elif message.text.lower().startswith("++зар ") or message.text.lower().startswith("++заразность "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_infectiousness = lab.infectiousness

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    current_balance = lab.bio_res
                    total_cost = calculate.zz(current_infectiousness, (current_infectiousness+level))
                    if current_balance < total_cost:
                        await message.reply("*У вас недостаточно био-ресурсов!*", parse_mode="Markdown")

                    else:
                        lab.bio_res -= total_cost
                        lab.infectiousness += level
                        lab.save()
                        total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                        text += f"Вы успешно добавили `{level}` заразности!\n"
                        text += f"С баланса снято `{total_cost}` био-ресурсов 🧬"
                        await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  

        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

        
    ''' ПРОКАЧКА ИММУНИТЕТА '''

    if message.text.lower().startswith("+имун ") or message.text.lower().startswith("+иммунитет "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_immunity = lab.immunity

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    total_cost = calculate.im(current_immunity, (current_immunity+level))
                    total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))

                    text += f"Ваш текущий уровень иммунитета: `{current_immunity}` 🛡\n"
                    text += f"Улучшение на _+{level}_ будет стоить: "
                    text += f"`{total_cost}` 🧬\n\n"
                    text += f"*Чтобы подвердить улучшение напишите:* `++имун {level}`"

                    await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  
        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    elif message.text.lower().startswith("++имун ") or message.text.lower().startswith("++иммунитет "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_immunity = lab.infectiousness

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    current_balance = lab.bio_res
                    total_cost = calculate.im(current_immunity, (current_immunity+level))
                    if current_balance < total_cost:
                        await message.reply("*У вас недостаточно био-ресурсов!*", parse_mode="Markdown")

                    else:
                        lab.bio_res -= total_cost
                        lab.immunity += level
                        lab.save()
                        total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                        text += f"Вы успешно добавили `{level}` иммунитета!\n"
                        text += f"С баланса снято `{total_cost}` био-ресурсов 🧬"
                        await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  

        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    ''' ПРОКАЧКА ЛЕТАЛЬНОСТИ '''

    if message.text.lower().startswith("+летал ") or message.text.lower().startswith("+летальность "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_mortality = lab.immunity

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    total_cost = calculate.ll(current_mortality, (current_mortality+level))
                    total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))

                    text += f"Ваш текущий уровень летальности: `{current_mortality}` 🛡\n"
                    text += f"Улучшение на _+{level}_ будет стоить: "
                    text += f"`{total_cost}` 🧬\n\n"
                    text += f"*Чтобы подвердить улучшение напишите:* `++летал {level}`"

                    await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  
        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return

    elif message.text.lower().startswith("++летал ") or message.text.lower().startswith("++летальность "):
        if lab.has_lab:  
            msg = message.text.lower().split(" ")
            text = "🔬 _Меню прокачки уровней_\n\n"
            current_mortality = lab.infectiousness

            if len(msg) == 2:
                if msg[1].isdigit():
                    level = int(msg[1])

                    if level <= 0:
                        await message.reply("Чувак)")
                        return

                    if level > 5:
                        await message.reply("Максимальное допустимое значение: `5`", parse_mode="Markdown")
                        return

                    current_balance = lab.bio_res
                    total_cost = calculate.ll(current_mortality, (current_mortality+level))
                    if current_balance < total_cost:
                        await message.reply("*У вас недостаточно био-ресурсов!*", parse_mode="Markdown")

                    else:
                        lab.bio_res -= total_cost
                        lab.immunity += level
                        lab.save()
                        total_cost = str('{0:,}'.format(total_cost).replace(',', ' '))
                        text += f"Вы успешно добавили `{level}` летальности!\n"
                        text += f"С баланса снято `{total_cost}` био-ресурсов 🧬"
                        await message.reply(text=text, parse_mode="Markdown")
                
                else:
                    await message.reply("Неправильный формат команды.")
                    return 

            else:
                await message.reply("Неправильный формат команды.")
                return  

        else:
            await message.reply(text=f"{message.from_user.first_name}, " \
                                f"у вас не создана лаборотория!\n\n"\
                                f"Напишите команду `биолаб` чтобы создать её",
                                parse_mode="Markdown")
            
            return


print("improvements init")