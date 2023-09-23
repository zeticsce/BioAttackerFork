from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

work_path = __file__.split("\\")
work_path.pop(-1)
work_path = '\\'.join(work_path)

import sys
import asyncio
import time
import datetime

from config import BOT_TOKEN, OWNER_ID, MYSQL_HOST

from libs.mysql_connect import query
from libs.handlers import *
from libs.StringConverters import StringConv
from libs.ChatHistory import save_message

sys.path.append(os.path.abspath(os.curdir) + "/libs")

strconv = StringConv()
bot = Bot(
    token = BOT_TOKEN
)

snd_msg_base = bot.send_message

async def new_send_message(chat_id, text, parse_mode = None, entities = None, disable_web_page_preview = None, message_thread_id = None, disable_notification = None, protect_content = None, reply_to_message_id = None, allow_sending_without_reply = None, reply_markup = None):
    msg = await snd_msg_base(chat_id, text, parse_mode, entities, disable_web_page_preview, message_thread_id, disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup)
    save_message(msg)

bot.send_message = new_send_message


dp = Dispatcher(bot)
dp.message_handlers.once = False

is_host = requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST

async def on_startup(dp):
    await dp.bot.send_message(OWNER_ID, f"*Вход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

if __name__ == '__main__':
    from libs.handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



