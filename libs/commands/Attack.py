'''

Модуль для заражения юзеров

'''

import os
import re
import time
import math
import random

from app import dp, bot, query, strconv, save_message, is_host
from config import MYSQL_HOST
from libs.handlers import labs

from aiogram import types, utils
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.callback_data import CallbackData

def skloneniye(num):
    names = ['день', 'дня', 'дней']
    n = num % 100
    if n >= 5 and n <= 20: return names[2]
    n = num % 10
    if n == 1: return names[0]
    if n >= 2 and n <= 4: return names[1]
    return names[2]


@dp.message_handler(content_types=['text'])
async def show_lab(message: types.Message):
    bio_infect = re.fullmatch(r"(биоеб)( \d{1,2})?( \S+)?", message.text.lower()) # регулярка на заражения
    if bio_infect != None:
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab:  #проверка на наличие лабы

            """Задание стартовых параметров колво попыток/тег"""
            attempts = int(bio_infect.group(2)) if bio_infect.group(2) != None else 1 # колво попыток
            victim_tag = bio_infect.group(3).strip().replace("tg://openmessage?user_id=", "").replace("https://t.me/", "").replace("@", "") if bio_infect.group(3) != None else None # тег жертвы из сообщения, None если его небыло
            victim = None #обьект жертвы содержит user_id, name, username
            """Проверка валидности стартовых параметров"""
            if lab.patogens <= 0: # проверка на паты
                await bot.send_message(message.chat.id, text=f"👺 Жди новых патогенов!",  parse_mode="Markdown")
                return
            if attempts > 10: # ограничивает колво попыток до 10
                await bot.send_message(message.chat.id, text=f"👺 За раз максимум 10 попыток!",  parse_mode="Markdown")
                return
            if attempts > lab.patogens: # следит, чтобы в итоге колво патов не стало меньше 0
                attempts = lab.patogens # клво попыток равное колву оставшихся патогенов

            if victim_tag != None: # если в сообщении был тег
                db_user = labs.get_user(victim_tag)
                if db_user == None:
                    await bot.send_message(message.chat.id, text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                    return # прерывает функцию в случае не нахождения юзера
                else: 
                    if is_host: # на хосте проверяет кд до следующего удара по юзеру
                        victim_in_list = lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{db_user['user_id']}'")
                        if len(victim_in_list) != 0:
                            victim_in_list = victim_in_list[0]
                            if victim_in_list['from_infect'] > (int(time.time())-3600):
                                untill = math.floor((victim_in_list['from_infect'] - (int(time.time())-3600)) / 60) # колво минут
                                declination = "" # склонение минуту/минуты/минут
                                if untill <= 20:
                                    if untill == 1: declination = "минута"
                                    elif untill <= 4: declination = "минуты"
                                    else: declination = "минут"
                                else: 
                                    if untill%10 == 1: declination = "минута"
                                    elif untill%10 <= 4: declination = "минуты"
                                    else: declination = "минут"

                                await bot.send_message(message.chat.id, text=f"👺 Ты сможешь заразить его повторно через {untill} {declination}!",  parse_mode="Markdown")
                                return 
                    victim = db_user

            """Генерация жертвы, если victim_tag == None"""
            if victim == None:
                if message.reply_to_message:
                    if message.reply_to_message["from"]["is_bot"] == True: # фильтр на ботов
                        await bot.send_message(message.chat.id, "👺 Нельзя заразить бота!")
                        return
                    victim = labs.get_user(message.reply_to_message["from"]["id"]) # обьект жертвы user_id, user_name, name
                    if is_host: # на хосте проверяет кд до следующего удара по юзеру
                        victim_in_list = lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{victim['user_id']}'")
                        if len(victim_in_list) != 0:
                            victim_in_list = victim_in_list[0]
                            if victim_in_list['from_infect'] > (int(time.time())-3600):
                                untill = math.floor((victim_in_list['from_infect'] - (int(time.time())-3600)) / 60) # колво минут
                                declination = "" # склонение минуту/минуты/минут
                                if untill <= 20:
                                    if untill == 1: declination = "минута"
                                    elif untill <= 4: declination = "минуты"
                                    else: declination = "минут"
                                else: 
                                    if untill%10 == 1: declination = "минута"
                                    elif untill%10 <= 4: declination = "минуты"
                                    else: declination = "минут"

                                await bot.send_message(message.chat.id, text=f"👺 Ты сможешь заразить его повторно через {untill} {declination}!",  parse_mode="Markdown")
                                return 
                else:
                    chance = int(random.random() * 100)

                    if chance < 20:
                        """Рандом юзер из бд с профитом 1-100 с шансом 20%"""
                        victim = labs.get_random_victum()
                    elif chance < 65:
                        """Рандом юзер с лабой с шансом 35%"""
                        victim = query("SELECT * FROM `bio_attacker`.`labs` INNER JOIN `telegram_data`.`tg_users` ON `telegram_data`.`tg_users`.`user_id`=`bio_attacker`.`labs`.`user_id` ORDER BY RAND() LIMIT 1;")[0] # 10% жертва из уже созданных лаб

                        """Штука снизу отвечает за исключение повторных заражений, но мне дико не нравится, что теперь постоянно пишет, что жертва не найдена (это пишется потому, что очень мало игроков)"""
                        # victim = victim if len(lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{victim['user_id']}' AND `victums{lab.user_id}`.`from_infect` <= {int(time.time()) - (60*60)}")) != 0 else None # проверка кд
                    
                    elif chance < 95:
                        """Рандом юзер из своих жертв с шансом 30%"""
                        victims = lab.get_victums(params="ORDER BY RAND() LIMIT 4")
                        for i in victims:
                            if i["from_infect"] <= int(time.time()) - (60*60): # проверка на кд
                                victim = i
                                break
                    else:
                        """Провал в поиске с шансом 5%"""
                        victim = None

            if victim == None:
                await bot.send_message(message.chat.id, text=f"👺 Жертва не найдена!",  parse_mode="Markdown")
                return
            if victim['user_id'] == lab.user_id:
                """Действия при заражении самого себя"""
                profit = int(lab.bio_exp / 10)

                lab.save_victum(victim['user_id'], profit)
                lab.patogens -= 1
                lab.save()
                patogen_name =  f"патогеном «{lab.patogen_name}»" if lab.patogen_name != None else "неизветным патогеном"

                rslt_text = f"😎 Вы подвергли заражению [{strconv.escape_markdown(victim['name'])}](tg://openmessage?user_id={victim['user_id']}) {patogen_name}\n\n🧪 Затрачено патогенов: _{1}_\n☣️ Жертва приности _{strconv.format_nums(profit)} био-ресурса_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
                await bot.send_message(message.chat.id, rslt_text,  parse_mode="Markdown")
            else:
                VictimLab = labs.get_lab(victim['user_id'])
                if VictimLab.has_lab: 
                    """алгоритм заражения, когда у юзера есть лаба"""

                    if VictimLab.immunity > lab.infectiousness: # просчет успеха удара, если имун жертвы больше заразности атакующего
                        atts = 0
                        for i in range(attempts):
                            atts += 1
                            if random.random() < 1/(VictimLab.immunity-lab.infectiousness):
                                suc = True
                                break
                        else:
                            suc = False
                    else:
                        suc = True
                        atts = 1 #затрачено патогенов
                    if suc:
                        profit = int(VictimLab.bio_exp / 10) # 10% профита юзера
                        profit = 1 if profit < 1 else profit # мин профит 1

                        lab.bio_exp += (profit*1.01) # рост био на 1% при заражении
                        VictimLab.bio_exp -= profit
                        VictimLab.bio_exp = 1 if VictimLab.bio_exp <= 0 else VictimLab.bio_exp #минимальный био у юзера 

                        VictimLab.prevented_issue += atts - 1
                        VictimLab.all_issue += atts
                        lab.all_operations += atts
                        lab.suc_operations += 1
                        lab.patogens -= atts

                        lab.save_victum(VictimLab.user_id, profit)
                        
                        patogen_name =  f"патогеном «{lab.patogen_name}»" if lab.patogen_name != None else "неизветным патогеном"

                        rslt_text = f"😎 Вы подвергли заражению [{strconv.escape_markdown(VictimLab.name)}](tg://openmessage?user_id={VictimLab.user_id}) {patogen_name}\n\n🧪 Затрачено патогенов: _{atts}_\n☣️ Получено _{strconv.format_nums(profit)} био-опыта_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
                        await bot.send_message(message.chat.id, rslt_text,  parse_mode="Markdown")

                        if VictimLab.security >= lab.security: # отправка сообщения о заражении, если сб жертвы больше сб атакующего
                            sb_text = f"👨🏻‍🔬 Была проведена операция вашего заражения! Организатор: [{strconv.escape_markdown(lab.name)}](tg://openmessage?user_id={lab.user_id})\n🧪 Совершено минимум {atts} попыток!\n☣️ Вы потряли {profit} био."
                            try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                            except utils.exceptions.ChatNotFound: pass
                        else:
                            patogen_name =  f"патогеном `{lab.patogen_name}`" if lab.patogen_name != None else "неизветным патогеном"
                            sb_text = f"👨🏻‍🔬 Вас подвергли заражению {patogen_name}\n☣️ Вы потряли _{profit} био._"
                            try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                            except utils.exceptions.ChatNotFound: pass

                    else: # действия при нуедаче заражения

                        VictimLab.prevented_issue += atts
                        VictimLab.all_issue += atts
                        lab.all_operations += atts
                        lab.patogens -= atts
                    
                        infct_text = f"👺 Операция заражения [{strconv.escape_markdown(VictimLab.name)}](tg://openmessage?user_id={VictimLab.user_id}) провалилась!"
                        await bot.send_message(message.chat.id, text=infct_text,  parse_mode="Markdown")
                        
                        """В случае провала, сб всегда попадает к жертве"""
                        sb_text = f"👺 Попытка вашего заражения провалилась! Организатор: [{strconv.escape_markdown(lab.name)}](tg://openmessage?user_id={lab.user_id})\nСовершено минимум {atts} попыток!"
                        try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                        except utils.exceptions.ChatNotFound: pass

                    lab.save()
                    VictimLab.save()

                else: 
                    """Рандом профит"""
                    profit = random.randint(0, 100)
                    lab.bio_exp += profit

                    atts = 0
                    for i in range(attempts):
                        atts += 1
                        if random.random() < 90/100:
                            suc = True
                            break
                    else:
                        suc = False

                    lab.all_operations += atts
                    lab.suc_operations += 1
                    lab.patogens -= atts

                    lab.save_victum(victim['user_id'], profit)
                    
                    patogen_name =  f"патогеном «{lab.patogen_name}»" if lab.patogen_name != None else "неизветным патогеном"

                    rslt_text = f"😎 Вы подвергли заражению [{strconv.escape_markdown(victim['name'])}](tg://openmessage?user_id={victim['user_id']}) {patogen_name}\n\n🧪 Затрачено патогенов: _{atts}_\n☣️ Получено _{strconv.format_nums(profit)} био-опыта_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
                    await bot.send_message(message.chat.id, rslt_text,  parse_mode="Markdown")

                    lab.save()