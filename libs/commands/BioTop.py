'''

Модуль с биотопом

'''

from app import dp, bot, query, strconv
from libs.handlers import labs

from aiogram import types


@dp.message_handler(content_types=["text"])
async def improve(message: types.Message):
    if message.text.lower() == "биоб":
        text = "Биотоп чмоней\n"
        count = 0
        all_bio_exp = query("SELECT SUM(bio_exp) as bio FROM `bio_attacker`.`labs`")[0]['bio']
        for lab in labs.bio_top:
            count += 1
            if lab["lab_name"] is not None:
                lab_name = lab["lab_name"]
            else:
                lab_name = "им. " + strconv.delinkify(strconv.normalaze(lab["name"], replace=str(lab['user_id'])))
            text += f'\n{count}. <a href="tg://openmessage?user_id={lab["user_id"]}">{lab_name}</a> | {strconv.num_to_str(lab["bio_exp"])} опыта'
            if count == 25: break

        text += f"\n\nБанк био-опыта в игре: {strconv.num_to_str(all_bio_exp)} ☣️"
        await bot.send_message(message.chat.id, text=text, parse_mode="HTML", disable_web_page_preview=True)
