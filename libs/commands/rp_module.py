'''

Модуль с рп командами

'''

import os
import re

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

rp = {
    "пнуть":             ["{op} пнул(а) {to}", "{op} пнул(а) {to} с репликой {repl}"],
    "погладить":         ["{op} погладил(а) {to}", "{op} погладил(а) {to} с репликой {repl}"],
    "бан":               ["{op} забанил(а) {to}", "{op} забанил(а) {to} с вердиктом {repl}"],
    "мут":               ["{op} замутил(а) {to}", "{op} замутил(а) {to} по причине {repl}"],
    "варн":              ["{op} кинул(а) варн {to}", "{op} кинул(а) варн {to} с репликой {repl}"],
    "расстрелять":       ["{op} расстрелял(а) {to}", "{op} расстрелял(а) {to} с репликой {repl}"],
    "убить":             ["{op} убил(а) {to}", "{op} убил(а) {to} с фразой {repl}"],
    "повесить":          ["{op} повесил(а) {to}", "{op} повесил(а) {to} по причине {repl}"],
    "принудить":         ["{op} принудил(а) {to}", "{op} принудил(а) {to} {repl}"],
    "приклеить":         ["{op} приклеил(а) {to}", "{op} приклеил(а) {to} с репликой {repl}"],
    "где":               ["{op} поинтересовался(лась) у {to}", "{op} поинтересовался(лась) у {to} с репликой {repl}"],
    "ударить":           ["{op} ударил(а) {to}", "{op} ударил(а) {to} с репликой {repl}"],
    "дать пять":         ["{op} дал(а) пять {to}", "{op} дал(а) пять {to} с репликой {repl}"],
    "обнять":            ["{op} обнял(а) {to}", "{op} обнял(а) {to} с репликой {repl}"],
    "извинить":          ["{op} извинил(а) {to}", "{op} извинил(а) {to} с репликой {repl}"],
    "простить":          ["{op} простил(а) {to}", "{op} простил(а) {to} с репликой {repl}"],
    "испугать":          ["{op} испугал(а) {to}", "{op} испугал(а) {to} с репликой {repl}"],
    "поздравить":        ["{op} поздравил(а) {to}", "{op} поздравил(а) {to} с репликой {repl}"],
    "пожать руку":       ["{op} пожал(а) руку{to}", "{op} пожал(а) руку {to} с репликой {repl}"],
    "похвалить":         ["{op} похвалил(а) {to}", "{op} похвалил(а) {to} с репликой {repl}"],
    "ущимить":           ["{op} ущимил(а) {to}", "{op} ущимил(а) {to} с репликой {repl}"],
    "ущипнуть":          ["{op} ущипнул(а) {to}", "{op} ущипнул(а) {to} с репликой {repl}"],
    "пригласить на чай": ["{op} пригласил(а) на чай {to}", "{op} пригласил(а) на чай {to} с репликой {repl}"],
    "лизнуть":           ["{op} лизнул(а) у {to}", "{op} лизнул(а) у {to} с репликой {repl}"],
    "лизь":              ["{op} подлизнул(а) {to}", "{op} подлизнул(а) {to} с репликой {repl}"],
    "облизать":          ["{op} облизал(а) ухо {to}", "{op} облизал(а) ухо {to} с репликой {repl}"],
    "прижать":           ["{op} прижал(а) {to}", "{op} прижал(а) {to} с репликой {repl}"],
    "потрогать":         ["{op} потрогал(а) {to}", "{op} потрогал(а){to} с репликой {repl}"],
    "понюхать":          ["{op} понюзал(а) {to}", "{op} понюзал(а) {to} с репликой {repl}"],
    "покормить":         ["{op} покормил(а) {to}", "{op} покормил(а) {to} с репликой {repl}"],
    "куснуть":           ["{op} куснул(а) {to}", "{op} куснул(а) {to} с репликой {repl}"],
    "кусь":              ["{op} сделал(а) микрокусь {to}", "{op} сделал(а) микрокусь {to} с репликой {repl}"],
    "поцеловать":        ["{op} поцеловал(а) {to}", "{op} поцеловал(а) {to} с репликой {repl}"],
    "шлепнуть":          ["{op} шлепнул(а) {to}", "{op} шлепнул(а) {to} с репликой {repl}"],
    "изнасиловать":      ["{op} принудил(а) к сексу {to}", "{op} принудил(а) {to} с репликой {repl}"],
    "отдаться":          ["{op} отдался(ась) полностью {to}", "{op} отдался(ась) {to} с репликой {repl}"],
    "трахнуть":          ["{op} принудил(а) к сексу {to}", "{op} принудил(а) к сексу {to} с репликой {repl}"],
    "делать секс":       ["{op} сделал(а) детей с {to}", "{op} сделал(а) детей с {to} с репликой {repl}"],
    "выебать":           ["{op} принудил(а) к сексу с особой жестокостью {to}", "{op} принудил(а) к сексу с особой жестокостью {to} с репликой {repl}"],
    "кастрировать":      ["{op} кастрировал(а) {to}", "{op} кастрировал(а) {to} с репликой {repl}"],
    "отравить":          ["{op} отравил(а) {to}", "{op} отравил(а) {to} с репликой {repl}"],
    "послать нахуй":     ["{op} послал(а) нахуй {to}", "{op} послал(а) нахуй {to} с репликой {repl}"],
    "расстрелять":       ["{op} расстрелял(а) {to}", "{op} расстрелял(а) {to} с репликой {repl}"],
    "сжечь":             ["{op} сжег {to}", "{op} сжег {to} с репликой {repl}"],
    "уебать":            ["{op} уебал(а) {to}", "{op} уебал(а) {to} с репликой {repl}"],
    "ударить":           ["{op} ударил(а) {to}", "{op} ударил(а) {to} с репликой {repl}"],
    "укусить":           ["{op} откусил(а) {to}", "{op} откусил(а) {to} с репликой {repl}"],
    "убить":             ["{op} убил(а) {to}", "{op} убил(а) {to} с репликой {repl}"],
    "связать":           ["{op} связал(а) {to}", "{op} связал(а) {to} с репликой {repl}"],
    "заставить":         ["{op} заставить(а) {to}", "{op} заставить(а) {to} с репликой {repl}"],
    "повесить":          ["{op} повесил(а) {to}", "{op} повесил(а) {to} с репликой {repl}"],
    "уничтожить":        ["{op} уничтожил(а) {to}", "{op} уничтожил(а) {to} с репликой {repl}"],
    "продать":           ["{op} продал(а) {to}", "{op} продал(а) {to} с репликой {repl}"],
    "пощекотать":        ["{op} пощекотал(а) {to}", "{op} пощекотал(а) {to} с репликой {repl}"],
    "взорвать":          ["{op} взорвал(а) {to}", "{op} взорвал(а) {to} с репликой {repl}"],
    "засосать":          ["{op} засосал(а) {to}", "{op} засосал(а) {to} с репликой {repl}"],
    "унизить":           ["{op} унизил(а) {to}", "{op} унизил(а) {to} с репликой {repl}"],
    "ушатать":           ["{op} ушатал(а) {to}", "{op} ушатал(а) {to} с репликой {repl}"],
    "порвать":           ["{op} порвал(а) {to}", "{op} порвал(а) {to} с репликой {repl}"],
    "отрубить":          ["{op} отрубил(а) {to}", "{op} отрубил(а) {to} с репликой {repl}"],
    "выкопать":          ["{op} выкопал(а) {to}", "{op} выкопал(а) {to} с репликой {repl}"],
    "наказать":          ["{op} наказал(а) {to}", "{op} наказал(а) {to} с репликой {repl}"]
}

@dp.message_handler(content_types=["text"])
async def improve(message: types.Message):
    split_msg = message.text.split("\n")
    reg = re.fullmatch(r"([a-zA-Zа-яА-Я0-9\s]+)(\s@([0-9a-zA-Z]+))?", split_msg[0])
    if reg != None:
        text = None
        command = reg.group(1).strip()
        to = reg.group(3)
        if to == None:
            if message.reply_to_message: 
                to = f'<a href="tg://openmessage?user_id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'
                to_hide = f'<a href="tg://user?id={message.reply_to_message.from_user.id}">\xad</a>'
        else:
            user = labs.get_user(to)
            if user != None:
                to = f'<a href="tg://openmessage?user_id={user["user_id"]}">{user["name"]}</a>'
                to_hide = f'<a href="tg://user?id={user["user_id"]}">\xad</a>'

        op = f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a>'
        repl = '\n'.join(split_msg[1::]) if len(split_msg) != 1 else None
        if command.lower() in rp:
            if op != None and to != None:
                if repl == None:
                    text = rp[command.lower()][0].replace("{op}", op).replace("{to}", to)
                else:
                    text = rp[command.lower()][1].replace("{op}", op).replace("{to}", to).replace("{repl}", repl)

            if text != None: await bot.send_message(message.chat.id, text=text+to_hide, parse_mode="HTML", disable_web_page_preview=True)