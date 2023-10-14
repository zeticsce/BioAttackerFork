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
    "пнуть":        ["{op} пнул(а) {to}",                 "{op} пнул(а) {to} с репликой {repl}"],
    "погладить":    ["{op} погладил(а) {to}",             "{op} погладил(а) {to} с репликой {repl}"],
    "бан":          ["{op} забанил(а) {to}",              "{op} забанил(а) {to} с вердиктом {repl}"],
    "мут":          ["{op} замутил(а) {to}",              "{op} замутил(а) {to} по причине {repl}"],
    "варн":         ["{op} кинул(а) варн {to}",           "{op} кинул(а) варн {to} с репликой {repl}"],
    "расстрелять":  ["{op} расстрелял(а) {to}",           "{op} расстрелял(а) {to} с репликой {repl}"],
    "убить":        ["{op} убил(а) {to}",                 "{op} убил(а) {to} с фразой {repl}"],
    "повесить":     ["{op} повесил(а) {to}",              "{op} повесил(а) {to} по причине {repl}"],
    "принудить":    ["{op} принудил(а) {to}",             "{op} принудил(а) {to} {repl}"],
    "приклеить":    ["{op} приклеил(а) {to}",             "{op} приклеил(а) {to} с репликой {repl}"],
    "где":          ["{op} поинтересовался(лась) у {to}", "{op} поинтересовался(лась) у {to} с репликой {repl}"],
    "ударить":      ["{op} ударил(а) {to}",               "{op} ударил(а) {to} с репликой {repl}"]
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