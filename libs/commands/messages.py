import os
import re
import time
import math
import random
from typing import Any
from math import floor
from app import dp, bot, query, strconv, save_message, is_host, IsAdmin

def skloneniye(num):
    names = ['день', 'дня', 'дней']
    n = num % 100
    if n >= 5 and n <= 20: return names[2]
    n = num % 10
    if n == 1: return names[0]
    if n >= 2 and n <= 4: return names[1]
    return names[2]

start_text = (
    "🧪 Вступи в смертельную игру биовойн!\n\n",
    "🌡️ Готов поиграть с жизнями?\n\n",
    "💣 Завоевывай мир своим вирусом!\n\n",
    "🧬 Готов к биологическому хаосу?\n\n",
    "🦠 Создай собственный патоген!\n\n",
    "🔬 Добро пожаловать в биолабораторию!\n\n",
    "💉 Погрузись в мир вирусов!\n\n"
)

''' Стандартная тема '''
theme = {
    "standard" : {
        "theme_name" : "Стандартная тема",
        "theme_desc" : "Дефолтная тема для олдов био-войн",
        
        "biolab" : {
            "info" : "🦠 Информация о вирусе",
            "owner" : "👺 Владелец",
            "corp" : "🏛 Корпорация",
            "pats" : "🧪 Патогенов",
            "new" : "⏱ До нового патогена",
            "quala" : "👨🏻‍🔬 Разработка",
            "zz" : "🦠 Заразность",
            "im" : "🛡 Иммунитет",
            "ll" : "☠️ Летальность",
            "bp" : "🕵️‍♂️ Безопасность",
            "exp" : "☣️ Био-опыт",
            "res" : "🧬 Био-ресурс",
            "operate" : "😷 Спецопераций",
            "issue" : "🥽 Предотвращены"

        },

        "errors" : {
            "wait" : "👺 Жди новых патогенов!",
            "10" : "👺 За раз максимум 10 попыток!",
            "404" : "👺 Юзер не найден!",
            "again" : "👺 Ты сможешь заразить его повторно через",
            "bot" : "👺 Нельзя заразить бота!",
            "victim" : "👺 Жертва не найдена!"
        }
    },

    "hell" : {
        "theme_name" : "Хеллоуинская тема",
        "theme_desc" : "Тема в честь Хеллоуина",
        
        "biolab" : {
            "info" : "👻 Название розыгрыша",
            "owner" : "👺 Владелец",
            "corp" : "🏛 Корпорация",
            "pats" : "🪄 ужастиков",
            "new" : "⏱ Новый ужастик",
            "quala" : "🧛 Квалификация колдунов",
            "zz" : "🌘 Ужасность",
            "im" : "🌕 Стойкость",
            "ll" : "🦇 Кровожадность",
            "bp" : "🕵️‍♂️ Ночная служба",
            "exp" : "🩸 Адреналин",
            "res" : "🧬 Био-ресурс",
            "operate" : "😷 Розыгрышей",
            "issue" : "🥽 Предотвращены"

        },

        "errors" : {
            "wait" : "👺 Жди новых патогенов!",
            "10" : "👺 За раз максимум 10 попыток!",
            "404" : "👺 Юзер не найден!",
            "again" : "👺 Ты сможешь заразить его повторно через",
            "bot" : "👺 Нельзя заразить бота!",
            "victim" : "👺 Жертва не найдена!"
        }
    },

    "azeri" : {
        "theme_name" : "Азербайджанская тема",
        "theme_desc" : "Тема для Азербайджанцев. ВНИМАНИЕ! СОДЕРЖИТ НЕЦЕНЗУРНУЮ ЛЕКСИКУ 18+!!1!",

        "biolab" : {
            "info" : "🦠 баздыгын сохбети",
            "owner" : "👺 Хан",
            "corp" : "🏛 Азерчай",
            "pats" : "🧪 Баздыглар",
            "new" : "⏱ До нового баздыга",
            "quala" : "👨🏻‍🔬 Пейсярляр",
            "zz" : "🦠 Дашагын бойу",
            "im" : "🛡 Готунун бойу",
            "ll" : "☠️ Агзынын бойу",
            "bp" : "🕵️‍♂️ Атонлар",
            "exp" : "☣️ Био-манатлар",
            "res" : "🧬 Био-гяпийляр",
            "operate" : "😷 Спецопераций",
            "issue" : "🥽 Предотвращены"

        },

        "errors" : {
            "wait" : "👺 гиждыллах, патогенляр йохду бле!",
            "10" : "👺 пейсяр, максимум 10 дяфя!",
            "404" : "👺 сикимин башы бля!",
            "again" : "👺 Ону йеня сикмяк олар сонра",
            "bot" : "👺 Боту сикмяк гадагандыр!",
            "victim" : "👺 Гяхпяни тампадын!"
        }
    }
}
def illness_check(lab):
    text = f""
    if lab.patogen_name != None:
        text = f"🥴 У вас горячка вызванная патогеном «`{lab.illness['patogen']}`»\n\n"
    else:
        text = f"🥴 У вас горячка вызванная неизвестным патогеном \n\n"
    return text

def patogenName(lab):
    if lab.theme == "azeri":
        howfuck = "баздыгом"
    elif lab.theme == "mafia":
        howfuck = "приемом"
    elif lab.theme == "hell":
        howfuck = "розыгрышем"
    else:
        howfuck = "патогеном"
    return f"{howfuck} «<code>{lab.patogen_name}</code>»" if lab.patogen_name != None else f"неизветным {howfuck}"



def attackText(theme, new, first_name, second_name, first_id, second_id, patogen_name, atts, profit, mortality):
    rslt_text = f""
    
    if theme == "azeri":
        ''' Азербайджанская тема '''
        fucked = "сикди"
        spend = "🧪 патогенляр гетди"
        gain = "☣️ Бу гяхпя верир"
        bio_res = "био-манатлар"
        infect = "☠️ Заражение на"
        lol = "👨‍🔬 Бу гехпе сенин деильди!!! Амма инди сяниндир)"
    
    elif theme == "mafia":
        ''' Мафиозная тема '''
        fucked = "успешно завербовал"
        spend = "💉 Использовано энергии"
        gain = "💰 Отобрано"
        bio_res = "манат"
        infect = "⏳ Останется на поводке клана в течение"
        lol = "🥷 Вы пополнили список своих шестерок новым осведомителем"
    
    elif theme == "hell":
        ''' Хеллоуин '''
        fucked = "напугал"
        spend = "👻 Потрачено ужастиков"
        gain = "🩸 Получено"
        bio_res = "адреналина"
        infect = "🌙 Пугающий эффект продлится"
        lol = "🎃 Жертва впервые встретилась с вашей шалостью и будет в шоке"
    else:
        ''' Стандартная тема '''
        fucked = "подверг заражению"
        spend = "🧪 Затрачено патогенов"
        gain = "☣️ Жертва приносит"
        bio_res = "био-ресурса"
        infect = "☠️ Заражение на"
        lol = "👨‍🔬 Объект ещё не подвергался заражению вашим патогеном"

    hide_victim_link = f'<a href="tg://user?id={second_id}">\xad</a>'
    hide_attacker_link = f'<a href="tg://user?id={first_id}">\xad</a>'

    rslt_text = f"😎 <a href='tg://openmessage?user_id={first_id}'>{first_name}</a>" \
                f" {fucked} " \
                f"<a href='tg://openmessage?user_id={second_id}'>{strconv.normalaze(second_name, replace=str(second_id))}</a>"\
                f" {patogen_name}\n\n"\
                f"{spend}: <i>{atts}</i>\n"\
                f"{gain} <i>{strconv.format_nums(profit)}{bio_res}</i>\n"\
                f"{infect} <i>{mortality} {skloneniye(mortality)}</i>"

    if new:
        rslt_text += f"\n\n<i>{lol}</i>"

    rslt_text += f"{hide_victim_link}"

    return rslt_text

heal_text = (
    "💊 Купить Обезболивающее",
    "💊 Купить Аптечку",
    "☕️ Выпить малиновый чай",
    "🍵 Выпить зеленый чай",
    "👨🏼‍⚕️ Пойти к врачу",
    "💉 Вколоть Антидот"
)

fuck_against = {
    "standart" : "Заразить в ответ",
    "agro" : "Выебать"
}
