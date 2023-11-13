from config import BOT_TOKEN, OWNER_ID, MYSQL_HOST, USERNAME, ECHO_CHAT
import datetime
import sys
import requests

class Out(object):
    def __init__(self, message_type) -> None:
        self.type = message_type
    def write(self, data):
        data = str(data)
        open('chats/errors.txt', 'a+').write(f"\n -- {datetime.datetime.now()}:\n" + data)
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/', {
            'method': 'sendMessage', 
            'chat_id': ECHO_CHAT, 
            'text': f'```{self.type}\n' + data + '```',
            'parse_mode': "Markdown"
        })
    def flush(self):
        pass

is_host = requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST
if is_host:
    sys.stdout = Out('Message')
    sys.stderr = Out('Warning')

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Filter

import asyncio
import time

class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        adms = [-1001864961488,-1001920018449, 1058211493, 5770061336, 780882761, 1202336740, 1495488713]
        return (message.chat.id in adms or message.from_user.id in adms) and message.text

import os

work_path = __file__.replace("\\", "/").split("/")
work_path.pop(-1)
work_path = '/'.join(work_path)

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
    return msg

bot.send_message = new_send_message


dp = Dispatcher(bot)
dp.message_handlers.once = False

async def on_startup(dp):
    await dp.bot.send_message(OWNER_ID, f"*Вход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")

if __name__ == '__main__':
    from libs.handlers import dp
    dp.bind_filter(IsAdmin)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



