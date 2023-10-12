'''

Модуль для заражения юзеров

'''

import os
import re
import time
import math
import random
from typing import Any

from app import dp, bot, query, strconv, save_message, is_host, IsAdmin
from config import MYSQL_HOST
from libs.handlers import labs
from commands.messages import *
from math import floor

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

vote_cb = CallbackData('vote', 'action', 'id', 'chat_id')
attack_against = CallbackData('vote', 'action', 'id', 'chat_id', 'id_of_organizator')

class Waiting:
    def __init__(self):
        self.users = {}
        self.last_clean = time.time()
    def clean(self):
        if self.last_clean + 240 < time.time(): self.users = {} # очищает стек юзеров раз в 20 минут

waiting = Waiting()


def get_keyboard_first(message: types.Message):
    text = random.choice(heal_text)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.row(
        types.InlineKeyboardButton(text=text, callback_data=vote_cb.new(action='buy', id=message.from_user.id, chat_id=message.chat.id)),
    )


    return keyboard_markup


def against( message: types.Message, id_of_organizator, id_id, chat_id):

    text = "Заразить в ответ"
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.row(
        types.InlineKeyboardButton(text="Заразить в ответ", callback_data=attack_against.new(action='against', id=id_id, chat_id=chat_id, id_of_organizator=id_of_organizator)),
    )


    return keyboard_markup


@dp.message_handler(content_types=["text"])
async def show_lab(message: types.Message):
    bio_infect = re.fullmatch(r"(биоеб)( \d{1,2})?( \S+)?", message.text.lower()) # регулярка на заражения
    if bio_infect != None:

        time_start = time.time()
        try: 
            if waiting.users[str(message.from_id)] + 0.75 > time_start: return # прерывает выполнение, если кд не прошло
        except KeyError: waiting.users[str(message.from_id)] = time_start # сохраняет время исполнения команды
        finally:  waiting.users[str(message.from_id)] = time_start # время отработки команды для юзера записывается сюда
        waiting.clean()
        
        lab = labs.get_lab(message['from']['id'])
        if lab.has_lab:  #проверка на наличие лабы

            """ Проверка на горячку"""
            if lab.illness != None:
                text = f""
                if lab.patogen_name != None:
                    text = f"🥴 У вас горячка вызванная патогеном «`{lab.illness['patogen']}`»\n\n"
                else:
                    text = f"🥴 У вас горячка вызванная неизвестным патогеном \n\n"

                declination = "" # склонение минуту/минуты/минут
                untill = floor(lab.illness['illness'] / 60)
                if untill <= 20:
                    if untill == 1: declination = "минута"
                    elif untill <= 4: declination = "минуты"
                    else: declination = "минут"
                else: 
                    if untill%10 == 1: declination = "минута"
                    elif untill%10 <= 4: declination = "минуты"
                    else: declination = "минут"
                text += f"Осталось времени `{untill}` {declination}."
                await bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_keyboard_first(message), reply_to_message_id=message.message_id)
                return


            """Задание стартовых параметров колво попыток/тег"""
            attempts = int(bio_infect.group(2)) if bio_infect.group(2) != None else 1 # колво попыток
            victim_tag = bio_infect.group(3).strip().replace("tg://user?id=", "").replace("tg://openmessage?user_id=", "").replace("https://t.me/", "").replace("@", "") if bio_infect.group(3) != None else None # тег жертвы из сообщения, None если его небыло
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
                profit = 1 if profit < 1 else profit

                lab.save_victum(victim['user_id'], profit)
                lab.save_issue(lab.user_id, lab.patogen_name, int(time.time()) + (lab.mortality * 24 * 60 * 60))
                lab.patogens -= 1
                lab.last_issue = int(time.time())
                lab.save()
                patogen_name =  f"патогеном «{lab.patogen_name}»" if lab.patogen_name != None else "неизветным патогеном"

                rslt_text = f"😎 [{message.from_user.first_name}](tg://user?id={message.from_user.id}) подверг заражению [{strconv.escape_markdown(victim['name'])}](tg://user?id={victim['user_id']}) {patogen_name}\n\n🧪 Затрачено патогенов: _{1}_\n☣️ Жертва приности _{strconv.format_nums(profit)} био-ресурса_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
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

                        lab.bio_exp += profit 
                        VictimLab.bio_exp -= profit
                        VictimLab.bio_exp = 1 if VictimLab.bio_exp <= 0 else VictimLab.bio_exp #минимальный био у юзера 

                        VictimLab.prevented_issue += atts - 1
                        VictimLab.all_issue += atts
                        VictimLab.last_issue = int(time.time())
                        lab.all_operations += atts
                        lab.suc_operations += 1
                        lab.patogens -= atts

                        lab.save_victum(VictimLab.user_id, profit)
                        # если у жертвы VictimLab.security сб больше, чем у атакующего lab.security, жертва получает сообщение о болезни
                        VictimLab.save_issue(lab.user_id, lab.patogen_name, int(time.time()) + (lab.mortality * 24 * 60 * 60), lab.security > VictimLab.security)
                        
                        patogen_name =  f"патогеном «<code>{lab.patogen_name}</code>»" if lab.patogen_name != None else "неизветным патогеном"

                        rslt_text = f'😎 <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> подверг заражению <a href="tg://user?id={VictimLab.user_id}">{strconv.escape_markdown(VictimLab.name)}</a> {patogen_name}\n\n🧪 Затрачено патогенов <i>{atts}</i>\n☣️ Получено <i>{strconv.format_nums(profit)} био-опыта</i>\n☠️ Заражение на <i>{lab.mortality} {skloneniye(lab.mortality)}</i>'
                        await bot.send_message(message.chat.id, rslt_text,  parse_mode="HTML")

                        if int(VictimLab.virus_chat) != message.chat.id:
                            if VictimLab.security >= lab.security: # отправка сообщения о заражении, если сб жертвы больше сб атакующего
                                patogen_name =  f"патогеном <code>{lab.patogen_name}</code>" if lab.patogen_name != None else "неизветным патогеном"
                                if int(VictimLab.virus_chat) == VictimLab.user_id: sb_text = f'👨🏻‍🔬 Была проведена операция вашего заражения {patogen_name}. \n\nОрганизатор <a href="tg://openmessage?user_id={lab.user_id}">{strconv.escape_markdown(lab.name)}</a>\n\n🧪 Совершено минимум {atts} попыток!\n☣️ Вы потеряли {profit} био.'
                                else: sb_text = f'👨🏻‍🔬 Была проведена операция заражения <a href="tg://user?id={VictimLab.user_id}">{VictimLab.name}</a> {patogen_name}. \n\nОрганизатор: <a href="tg://openmessage?user_id={lab.user_id}">{strconv.escape_markdown(lab.name)}</a>\n\n🧪 Совершено минимум {atts} попыток!\n☣️ Вы потеряли {profit} био.'
                                # try: 
                                await bot.send_message(chat_id=VictimLab.virus_chat, text=sb_text,  parse_mode="HTML", reply_markup=against(message, id_id=VictimLab.user_id, chat_id=VictimLab.virus_chat,id_of_organizator=lab.user_id))
                                # except Exception as e:
                                #     print(e) 
                            else:
                                patogen_name =  f"патогеном <code>{lab.patogen_name}</code>" if lab.patogen_name != None else "неизветным патогеном"
                                if int(VictimLab.virus_chat) == VictimLab.user_id: sb_text = f"👨🏻‍🔬 Вас подвергли заражению {patogen_name}\n\n☣️ Вы потеряли <i>{strconv.format_nums(profit)} био.</i>"
                                else: sb_text = f'👨🏻‍🔬 <a href="tg://user?id={VictimLab.user_id}">{VictimLab.name}</a> был подвергнут заражению {patogen_name}\n\n☣️ Потерял <i>{strconv.format_nums(profit)} био.</i>'
                                try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="HTML")
                                except: pass

                    else: # действия при нуедаче заражения

                        VictimLab.prevented_issue += atts
                        VictimLab.all_issue += atts
                        lab.all_operations += atts
                        lab.patogens -= atts
                    
                        infct_text = f"👺 Операция заражения [{strconv.escape_markdown(VictimLab.name)}](tg://user?id={VictimLab.user_id}) провалилась!"
                        await bot.send_message(message.chat.id, text=infct_text,  parse_mode="Markdown")
                        
                        if int(VictimLab.virus_chat) != message.chat.id:
                            """В случае провала, сб всегда попадает к жертве"""
                            if int(VictimLab.virus_chat) == VictimLab.user_id:
                                sb_text = f"👺 Попытка вашего заражения провалилась! Организатор [{strconv.escape_markdown(lab.name)}](tg://user?id={lab.user_id})\nСовершено минимум {atts} попыток!"
                            else:
                                sb_text = f"👺 Попытка заразить [{VictimLab.name}](tg://user?id={VictimLab.user_id}) провалилась! Организатор [{strconv.escape_markdown(lab.name)}](tg://user?id={lab.user_id})\nСовершено минимум {atts} попыток!"
                            try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                            except: pass

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

                    rslt_text = f"😎 [{message.from_user.first_name}](tg://user?id={message.from_user.id}) подверг заражению [{strconv.escape_markdown(victim['name'])}](tg://user?id={victim['user_id']}) {patogen_name}\n\n🧪 Затрачено патогенов _{atts}_\n☣️ Получено _{strconv.format_nums(profit)} био-опыта_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
                    await bot.send_message(message.chat.id, rslt_text,  parse_mode="Markdown")

                    lab.save()
    
    if message.text.lower() in ("хил", "биохил", "биохилл"):
        lab = labs.get_lab(message.from_user.id)
        if lab.has_lab:  #проверка на наличие лабы
            if lab.illness != None:
                if lab.bio_res - 10 >= 0:
                    lab.last_issue = 0
                    lab.bio_res -= 10
                    lab.save()

                    text = "🤓Вы успешно исцелились!\n\n"
                    text += "Потрачено `10` био-ресурсов 🧬" 
                    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_to_message_id=message.message_id)
                elif lab.bio_res - 10 <= 0 and lab.bio_res + lab.coins >= 0:
                    text = "🤓Вы успешно исцелились!\n\n"
                    text += f"Потрачено {lab.bio_res} 🧬 и {(10 - lab.bio_res)} 💰"
                    lab.last_issue = 0
                    lab.coins -= (10 - lab.bio_res)
                    lab.bio_res -= lab.bio_res
                    lab.save()
                    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_to_message_id=message.message_id)

                else:
                    await message.reply("Недостаточно био-ресурса!")

            else:
                await message.reply("😃 У вас нету горячки!")

""" Код для хилки """
@dp.callback_query_handler(vote_cb.filter(action='buy'))
async def treat(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    if from_user_id == str(query.from_user.id):
        lab = labs.get_lab(from_user_id)
        if lab.has_lab:  #проверка на наличие лабы
                    
            if lab.bio_res - 10 >= 0:
                lab.last_issue = 0
                lab.bio_res -= 10
                lab.save()

                text = "🤓Вы успешно исцелились!\n\n"
                text += "Потрачено `10` био-ресурсов 🧬" 
                await bot.edit_message_text(
                    chat_id=query.message.chat.id, 
                    text=text, 
                    parse_mode="Markdown", 
                    message_id=query.message.message_id,
                )
            elif lab.bio_res - 10 <= 0 and lab.bio_res + lab.coins >= 0:
                text = "🤓Вы успешно исцелились!\n\n"
                text += f"Потрачено {lab.bio_res} 🧬 и {(10 - lab.bio_res)} 💰"
                lab.last_issue = 0
                lab.coins -= (10 - lab.bio_res)
                lab.bio_res -= lab.bio_res
                lab.save()
                await bot.edit_message_text(
                    chat_id=query.message.chat.id, 
                    text=text, 
                    parse_mode="Markdown", 
                    message_id=query.message.message_id,
                )
            else:
                await query.answer("Кажется тебе био-реса не хватает :)")
    else:
        await query.answer("Эта кнопка не для тебя :)")

''' Код для ответки '''
@dp.callback_query_handler(attack_against.filter(action='against'))
async def attack_youknow(query: types.CallbackQuery, callback_data: dict):
    from_user_id = callback_data["id"]
    message_name = query.from_user.first_name
    chat_id = callback_data["chat_id"]
    victim = callback_data["id_of_organizator"]
    lab = labs.get_lab(from_user_id)
    VictimLab = labs.get_lab(victim)
    if from_user_id == str(query.from_user.id):
        # await bot.delete_message(query.message.chat.id, query.message.message_id)
        text_message = query.message.text.split("\n")
        patogen_name =  f"патогеном «<code>{VictimLab.patogen_name}</code>»" if VictimLab.patogen_name != None else "неизветным патогеном"
        text = f'👨🏻‍🔬 Была проведена операция заражения <a href="tg://openmessage?user_id={lab.user_id}">{lab.name}</a> {patogen_name}\n\n'
        text += f'Организатор: <a href="tg://openmessage?user_id={VictimLab.user_id}"></a>{VictimLab.name}\n\n'
        text += text_message[4] + "\n"
        text += text_message[5]
        await bot.edit_message_text(
                    chat_id=query.message.chat.id, 
                    text=text, 
                    parse_mode="HTML", 
                    message_id=query.message.message_id,
                    disable_web_page_preview=True
                )

        if lab.illness != None:
            text = f""
            if lab.patogen_name != None:
                text = f"🥴 У вас горячка вызванная патогеном «`{lab.illness['patogen']}`»\n\n"
            else:
                text = f"🥴 У вас горячка вызванная неизвестным патогеном \n\n"

            declination = "" # склонение минуту/минуты/минут
            untill = floor(lab.illness['illness'] / 60)
            if untill <= 20:
                if untill == 1: declination = "минута"
                elif untill <= 4: declination = "минуты"
                else: declination = "минут"
            else: 
                if untill%10 == 1: declination = "минута"
                elif untill%10 <= 4: declination = "минуты"
                else: declination = "минут"
            text += f"Осталось времени `{untill}` {declination}."
            await bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_keyboard_first(message), reply_to_message_id=message.message_id)
            return

        if lab.patogens <= 0: # проверка на паты
            await bot.send_message(query.message.chat.id, text=f"👺 Жди новых патогенов!",  parse_mode="Markdown")
            return

        
        if is_host: # на хосте проверяет кд до следующего удара по юзеру
            victim_in_list = lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{VictimLab['user_id']}'")
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

        atts = 0
        suc = False
        if VictimLab.immunity > lab.infectiousness: # просчет успеха удара, если имун жертвы больше заразности атакующего
            
            if random.random() < 1/(VictimLab.immunity-lab.infectiousness):
                atts = 1
                suc = True
        else:
            suc = True
            atts = 1 #затрачено патогенов
        if suc:
            profit = int(VictimLab.bio_exp / 10) # 10% профита юзера
            profit = 1 if profit < 1 else profit # мин профит 1

            lab.bio_exp += profit 
            VictimLab.bio_exp -= profit
            VictimLab.bio_exp = 1 if VictimLab.bio_exp <= 0 else VictimLab.bio_exp #минимальный био у юзера 

            VictimLab.prevented_issue += atts - 1
            VictimLab.all_issue += atts
            VictimLab.last_issue = int(time.time())
            lab.all_operations += atts
            lab.suc_operations += 1
            lab.patogens -= atts

            lab.save_victum(VictimLab.user_id, profit)
            # если у жертвы VictimLab.security сб больше, чем у атакующего lab.security, жертва получает сообщение о болезни
            VictimLab.save_issue(lab.user_id, lab.patogen_name, int(time.time()) + (lab.mortality * 24 * 60 * 60), lab.security > VictimLab.security)
            
            patogen_name =  f"патогеном «{lab.patogen_name}»" if lab.patogen_name != None else "неизветным патогеном"

            rslt_text = f"😎 [{lab.name}](tg://user?id={lab.user_id}) подверг заражению [{strconv.escape_markdown(VictimLab.name)}](tg://user?id={VictimLab.user_id}) {patogen_name}\n\n🧪 Затрачено патогенов _{atts}_\n☣️ Получено _{strconv.format_nums(profit)} био-опыта_\n☠️ Заражение на _{lab.mortality} {skloneniye(lab.mortality)}_"
            await bot.send_message(query.message.chat.id, rslt_text,  parse_mode="Markdown")

            if int(VictimLab.virus_chat) != query.message.chat.id:
                if VictimLab.security >= lab.security: # отправка сообщения о заражении, если сб жертвы больше сб атакующего
                    patogen_name =  f"патогеном <code>{lab.patogen_name}</code>" if lab.patogen_name != None else "неизветным патогеном"
                    if int(VictimLab.virus_chat) == VictimLab.user_id: sb_text = f'👨🏻‍🔬 Была проведена операция вашего заражения {patogen_name}. \n\nОрганизатор <a href="tg://openmessage?user_id={lab.user_id}">{strconv.escape_markdown(lab.name)}</a>\n\n🧪 Совершено минимум {atts} попыток!\n☣️ Вы потеряли {profit} био.'
                    else: sb_text = f'👨🏻‍🔬 Была проведена операция заражения <a href="tg://user?id={VictimLab.user_id}">{VictimLab.name}</a> {patogen_name}. \n\nОрганизатор: <a href="tg://openmessage?user_id={lab.user_id}">{strconv.escape_markdown(lab.name)}</a>\n\n🧪 Совершено минимум {atts} попыток!\n☣️ Вы потеряли {profit} био.'
                    # try: 
                    await bot.send_message(chat_id=VictimLab.virus_chat, text=sb_text,  parse_mode="HTML", reply_markup=against(query.message, id_id=VictimLab.user_id, chat_id=VictimLab.virus_chat,id_of_organizator=lab.user_id))
                    # except Exception as e:
                    #     print(e) 
                else:
                    patogen_name =  f"патогеном <code>{lab.patogen_name}</code>" if lab.patogen_name != None else "неизветным патогеном"
                    if int(VictimLab.virus_chat) == VictimLab.user_id: sb_text = f"👨🏻‍🔬 Вас подвергли заражению {patogen_name}\n\n☣️ Вы потеряли <i>{strconv.format_nums(profit)} био.</i>"
                    else: sb_text = f'👨🏻‍🔬 <a href="tg://user?id={VictimLab.user_id}">{VictimLab.name}</a> был подвергнут заражению {patogen_name}\n\n☣️ Потерял <i>{strconv.format_nums(profit)} био.</i>'
                    try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="HTML")
                    except: pass

        else: # действия при нуедаче заражения

            VictimLab.prevented_issue += atts
            VictimLab.all_issue += atts
            lab.all_operations += atts
            lab.patogens -= atts
        
            infct_text = f"👺 Операция заражения [{strconv.escape_markdown(VictimLab.name)}](tg://user?id={VictimLab.user_id}) провалилась!"
            await bot.send_message(query.message.chat.id, text=infct_text,  parse_mode="Markdown")
            
            if int(VictimLab.virus_chat) != query.message.chat.id:
                """В случае провала, сб всегда попадает к жертве"""
                if int(VictimLab.virus_chat) == VictimLab.user_id:
                    sb_text = f"👺 Попытка вашего заражения провалилась! Организатор [{strconv.escape_markdown(lab.name)}](tg://user?id={lab.user_id})\nСовершено минимум {atts} попыток!"
                else:
                    sb_text = f"👺 Попытка заразить [{VictimLab.name}](tg://user?id={VictimLab.user_id}) провалилась! Организатор [{strconv.escape_markdown(lab.name)}](tg://user?id={lab.user_id})\nСовершено минимум {atts} попыток!"
                try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                except: pass

        lab.save()
        VictimLab.save()
        

    else:
        await query.answer("Эта кнопка не для тебя :)")
