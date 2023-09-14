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

def impr_price(start, end, power):
    price = 0
    for i in range(int(end) - int(start)):
        price += floor((int(start) + i + 1) ** power)
    return price

@dp.message_handler(content_types=['text'])
async def improve(message: types.Message):
    
    if message.text.startswith("+"):
    
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab: # проверка существует ли лаба, если лабы нет, то пусть вообще не отвечает
        
            imps={}
            imps["патоген"] =      re.fullmatch(r"\+(патоген|пат)(\s\d+)?", message.text.lower())
            imps["квалификация"] = re.fullmatch(r"\+(разработка|квала|квалификация)(\s\d+)?", message.text.lower())
            imps["заразность"] =   re.fullmatch(r"\+(зз|заразность)(\s\d+)?", message.text.lower())
            imps["иммунитет"] =    re.fullmatch(r"\+(иммун|иммунитет)(\s\d+)?", message.text.lower())
            imps["летальность"] =  re.fullmatch(r"\+(летал|летальность)(\s\d+)?", message.text.lower())
            imps["безопасность"] = re.fullmatch(r"\+(сб|безопасность)(\s\d+)?", message.text.lower())
            imps["попыток"] =      re.fullmatch(r"\+([а-я]+)(\s\d+)?", message.text.lower())

            atts = int(imps["попыток"].group(2)) if imps["попыток"].group(2) != None else 1
            text = None

            if atts <= 100:

                if imps["патоген"] != None:
                    price = strconv.format_nums(impr_price(lab.all_patogens, lab.all_patogens + atts, 2.0))
                    text = f"Прокачка патоегна с _{lab.all_patogens} ур._ до _{lab.all_patogens + atts} ур._ обойдется вам в _{price} био_"

                elif imps["квалификация"] != None:
                    price = strconv.format_nums(impr_price(lab.qualification, lab.qualification + atts, 2.0))
                    text = f"Прокачка квалификации с _{lab.qualification} ур._ до _{lab.qualification + atts} ур._ обойдется вам в _{price} био_"

                elif imps["заразность"] != None:
                    price = strconv.format_nums(impr_price(lab.infectiousness, lab.infectiousness + atts, 2.0))
                    text = f"Прокачка заразности с _{lab.infectiousness} ур._ до _{lab.infectiousness + atts} ур._ обойдется вам в _{price} био_"

                elif imps["иммунитет"] != None:
                    price = strconv.format_nums(impr_price(lab.immunity, lab.immunity + atts, 2.0))
                    text = f"Прокачка иммунитета с _{lab.immunity} ур._ до _{lab.immunity + atts} ур._ обойдется вам в _{price} био_"

                elif imps["летальность"] != None:
                    price = strconv.format_nums(impr_price(lab.mortality, lab.mortality + atts, 2.0))
                    text = f"Прокачка летальности с _{lab.mortality} ур._ до _{lab.mortality + atts} ур._ обойдется вам в _{price} био_"

                elif imps["безопасность"] != None:
                    price = strconv.format_nums(impr_price(lab.security, lab.security + atts, 2.0))
                    text = f"Прокачка безопасности с _{lab.security} ур._ до _{lab.security + atts} ур._ обойдется вам в _{price} био_"

            else: text = f"Вы не можете прокачать более _100 уровней_ за раз!"

            if text != None: await message.reply(text=text, parse_mode="Markdown")