import time

from app import dp, bot
from libs.handlers import labs, statistics
from config import USER_ID
from commands.messages import *


from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils import exceptions

vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')
buylg = CallbackData('vote', 'action', 'theme_name', 'id', 'chat_id')

@dp.message_handler(content_types=["text"]) 
async def handler(message: types.message):
    if message.text.lower().replace(". ", ".") in ("market", "маркет", "тема", "theme" ".m", ".м", ".т"):
        lab = labs.get_lab(message.from_user.id)
        if lab.has_lab:

            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

            if 'themes' not in lab.modules:
                lab.modules['themes'] = []
                lab.save()

            text = "Доступные вам темы:\n\n"

            if len(lab.modules['themes']) == 0:
                text += "У вас нету ни одной приобретенной темы."
            else:
                count = 0
                for i in range(len(lab.modules['themes'])):
                    theme_name = lab.modules['themes'][i]
                    text += f"{count + 1}. " + f"{theme[theme_name]['theme_name']}\n"
                    count += 1
                
            keyboard_markup.row(
                types.InlineKeyboardButton(text="Темы", callback_data=vote_cb.new(action='themes', id=message.from_user.id, chat_id=message.chat.id)),
            )

            await message.reply(text, reply_markup=keyboard_markup)
        
        else:
            return

@dp.callback_query_handler(vote_cb.filter(action='themes'))
async def open_themes(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]

    if from_user_id == str(query.from_user.id):
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

        keyboard_markup.row(
            types.InlineKeyboardButton(text="Языковые", callback_data=vote_cb.new(action='languages', id=from_user_id, chat_id=chat_id)),
            types.InlineKeyboardButton(text="Аркадные", callback_data=vote_cb.new(action='aracdes', id=from_user_id, chat_id=chat_id)),
        )

        keyboard_markup.add(
            types.InlineKeyboardButton(text='Установить тему', callback_data=vote_cb.new(action=f'install_theme', id=from_user_id, chat_id=chat_id)),
        )

        text = f"Языковые - темы с использованием иностранных языков\n\n"
        text += f"Аркадные - темы с использованием разных тематик"

        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=query.message.message_id, reply_markup=keyboard_markup)
        
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='languages'))
async def buy_language(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]

    if from_user_id == str(query.from_user.id):
        text = "🌊 Маркет тем\n\n"

        lab = labs.get_lab(from_user_id)
        purchased = lab.modules
        
        keys = list(theme.keys())
        count = 0

        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

        for i in range(len(keys)):
            if theme[keys[i]]["type"] == "language":
                if keys[i] in lab.modules['themes']:
                    continue
                
                theme_name = theme[keys[i]]["theme_name"]
                theme_price = theme[keys[i]]["price"]
                
                text += f"{count + 1}. " + f'{theme_name} | {theme_price} 💰\n'
                count += 1
                

                keyboard_markup.add(
                    types.InlineKeyboardButton(text=f'{theme_name}', callback_data=buylg.new(action=f'buy_theme', theme_name=keys[i], id=from_user_id, chat_id=chat_id)),
                )
        
        if count == 0:
            text += "Походу вы купили все темы :)"
        
        keyboard_markup.add(
            types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action='themes', id=from_user_id, chat_id=chat_id)),
        )

        await bot.edit_message_text(text, message_id=query.message.message_id, chat_id=chat_id, reply_markup=keyboard_markup)
    
    else:
        await query.answer("Эта кнопка не для тебя :)")


@dp.callback_query_handler(vote_cb.filter(action='aracdes'))
async def buy_language(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]

    if from_user_id == str(query.from_user.id):
        text = "🌊 Маркет тем\n\n"

        lab = labs.get_lab(from_user_id)
        purchased = lab.modules
        
        keys = list(theme.keys())
        count = 0

        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

        for i in range(len(keys)):
            if theme[keys[i]]["type"] == "arcade":
                if keys[i] in lab.modules['themes']:
                    continue

                theme_name = theme[keys[i]]["theme_name"]
                theme_price = theme[keys[i]]["price"]
                
                text += f"{count + 1}. " + f'{theme_name} | {theme_price} 💰\n'
                count += 1
                

                keyboard_markup.add(
                    types.InlineKeyboardButton(text=f'{theme_name}', callback_data=buylg.new(action=f'buy_theme', theme_name=keys[i], id=from_user_id, chat_id=chat_id)),
                )
        
        if count == 0:
            text += "Походу вы купили все темы :)"

        keyboard_markup.add(
            types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action='themes', id=from_user_id, chat_id=chat_id)),
        )

        await bot.edit_message_text(text, message_id=query.message.message_id, chat_id=chat_id, reply_markup=keyboard_markup)
    
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(buylg.filter(action='buy_theme'))
async def buy_language(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    theme_name = callback_data["theme_name"]

    if from_user_id == str(query.from_user.id):
        lab = labs.get_lab(from_user_id)
        if lab.has_lab:

            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

            if 'themes' not in lab.modules:
                lab.modules['themes'] = []
                lab.save()
            
            if lab.coins < int(theme[theme_name]["price"]):
                await bot.edit_message_text(text="У вас недостаточно коинов!", message_id=query.message.message_id, chat_id=chat_id)
                return
            else:
                creator_lab = None
                if theme_name == "zombie":
                    creator_lab = labs.get_lab(1731537016) # Окультизм
 
                elif theme_name in ("cookies", "mafia"):
                    creator_lab = labs.get_lab(1202336740) # Кнопка

                elif theme_name == "dream":
                    creator_lab = labs.get_lab(5892568878) # David95gT
                
                elif theme_name == "scammer":
                    creator_lab = labs.get_lab(6112156332) # Геля
                
                elif theme_name == "school":
                    creator_lab = labs.get_lab(1468359713) # Донатик
                
                elif theme_name == "pornohub":
                    creator_lab = labs.get_lab(5022122512) # Дино

                if creator_lab != None:
                    creator_lab.coins += 500
                    statistics.save_transaction(sender_id=USER_ID, getter_id=creator_lab.user_id, coins=500)
                    creator_lab.save()
                    try:
                        await bot.send_message(creator_lab.user_id, "Вашу тему купили, вам начислено 500 комнов!")
                    except exceptions.ChatNotFound:
                        pass

                statistics.themes.append({
                    "descr": f"Куплена тема {theme_name} за {int(theme[theme_name]['price'])}",
                    "prise": int(theme[theme_name]['price']),
                    "theme_name": theme_name,
                    "time": time.time(),
                    "buyer": lab.user_id,
                    "creator": creator_lab.user_id if creator_lab != None else None
                })

                lab.coins -= int(theme[theme_name]["price"])
                statistics.save_transaction(sender_id=lab.user_id, getter_id=USER_ID, coins=int(theme[theme_name]["price"]))
                lab.modules['themes'].append(theme_name)
                lab.save()

            
            keyboard_markup.add(
                    types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action=f'themes', id=from_user_id, chat_id=chat_id)),
            )

            await bot.edit_message_text(text=f"{theme[theme_name]['theme_name']} приобретена\n\nВы потратили {theme[theme_name]['price']} коинов!", message_id=query.message.message_id, chat_id=chat_id, reply_markup=keyboard_markup)
    
    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(vote_cb.filter(action='install_theme'))
async def buy_language(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    lab = labs.get_lab(from_user_id)
    if from_user_id == str(query.from_user.id):
        text = "🌪 Ваши темы\n\n"

        if len(lab.modules['themes']) == 0:
            text += "У вас нету ни одной приобретенной темы."
        else:

            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

            text += "Кликните на кнопку чтобы установить тему."
            for i in range(len(lab.modules['themes'])):
                theme_name = lab.modules['themes'][i]

                keyboard_markup.add(
                    types.InlineKeyboardButton(text=f'{theme[theme_name]["theme_name"]}', callback_data=buylg.new(action=f'install_theme', theme_name=theme_name, id=from_user_id, chat_id=chat_id)),
                )
        
        keyboard_markup.add(
                    types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action=f'themes', id=from_user_id, chat_id=chat_id)),
        )
        
        await bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=chat_id, reply_markup=keyboard_markup)

    else:
        await query.answer("Эта кнопка не для тебя :)")

@dp.callback_query_handler(buylg.filter(action='install_theme'))
async def buy_language(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    theme_name = callback_data["theme_name"]

    if from_user_id == str(query.from_user.id):
        lab = labs.get_lab(from_user_id)
        if lab.has_lab:
            
            keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

            lab.theme = theme_name
            lab.save()

            text = f"{theme[theme_name]['theme_name']} установлена!"

            keyboard_markup.add(
                    types.InlineKeyboardButton(text='◀️ Назад', callback_data=vote_cb.new(action=f'themes', id=from_user_id, chat_id=chat_id)),
            )
            
            await bot.edit_message_text(text=text, message_id=query.message.message_id, chat_id=chat_id, reply_markup=keyboard_markup)
    
    else:
        await query.answer("Эта кнопка не для тебя :)")