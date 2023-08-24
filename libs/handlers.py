
from app import dp

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

@dp.message_handler(content_types=['text']) 
async def handler(message: types.message):
    await message.reply(message.text)

print("handlers init")