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
            if victim['user_id'] == str(lab.user_id):
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
                            sb_text = f"Была проведена операция вашего заражения!\nСовершено минимум {atts} попыток!\nОрганизатор: [{strconv.escape_markdown(lab.name)}](tg://openmessage?user_id={lab.user_id})\nВы потряли {profit} био."
                            try: await bot.send_message(VictimLab.virus_chat, text=sb_text,  parse_mode="Markdown")
                            except utils.exceptions.ChatNotFound: pass
                        else:
                            patogen_name =  f"патогеном {lab.patogen_name}" if lab.patogen_name != None else "неизветным патогеном"
                            sb_text = f"Вас подвергли заражению {patogen_name}\nВы потряли {profit} био."
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
                        sb_text = f"👺 Попытка вашего заражения провалилась!\nСовершено минимум {atts} попыток!\nОрганизатор: [{strconv.escape_markdown(lab.name)}](tg://openmessage?user_id={lab.user_id})"
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

            return
            attempts = int(bio_infect.group(2)) if bio_infect.group(2) != None else None # колво попыток

            if attempts == None: attempts = 1 # если колво попыток не определено, задавать 1

            if lab.patogens <= 0: # проверка на паты
                await bot.send_message(message.chat.id, text=f"👺 Жди новых патогенов!",  parse_mode="Markdown")
                return
            if attempts > 10: # ограничивает колво попыток до 10
                await bot.send_message(message.chat.id, text=f"👺 За раз максимум 10 попыток!",  parse_mode="Markdown")
                return

            victim_tag = bio_infect.group(3).strip().replace("tg://openmessage?user_id=", "").replace("https://t.me/", "").replace("@", "") if bio_infect.group(3) != None else None # тег жертвы из сообщения, None если его небыло

            victim = None # жертва (пиздец я всегда victum использовал)
            chance = random.random() # рандомыш от 0 до 1

            profit = 0
            pats = 0

            if message.reply_to_message: # нахождение айди жертвы при реплае
                if message.reply_to_message["from"]["is_bot"] == True: # фильтр на ботов
                    await bot.send_message(message.chat.id, "Нельзя заразить бота")
                    return
                victim = labs.get_user(message.reply_to_message["from"]["id"]) # обьект жертвы user_id, user_name, name


            if victim_tag != None: # если все хорошо, у нас останется victim_user, которая содержит айди юзера
                # в приоретете victim_tag, если будет реплай, то он сначала чекнет victim_tag, если он присутсвует, то будет бить его
                if re.fullmatch(r"[\w]+", victim_tag) == None: # проверка на валидность тега, нет ли там русских букв, спец символов и тд
                    await bot.send_message(message.chat.id, text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                    return
                else:
                    victim = labs.get_user(victim_tag) # проверка есть ли он в базе
                    if victim == None:
                        await bot.send_message(message.chat.id, text=f"👺 Юзер не найден!",  parse_mode="Markdown")
                        return
                    elif is_host: # на хосте проверяет кд до следующего удара по юзеру
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

            if victim == None: # тут происходит рандомный выбор жертвы
                if chance < 0.30: victim = labs.get_random_victum() # 30% абсолютно рандомный чел из бд
                elif chance < 0.60: # 30% перебив случайной жертвы
                    victims = lab.get_victums(params="ORDER BY RAND() LIMIT 4")
                    for i in victims:
                        if i["from_infect"] <= int(time.time()) - (60*60): # проверка на кд
                            victim = i
                            break
                elif chance < 0.90: #30% ктото с лабой
                    victim = query("SELECT * FROM `bio_attacker`.`labs` INNER JOIN `telegram_data`.`tg_users` ON `telegram_data`.`tg_users`.`user_id`=`bio_attacker`.`labs`.`user_id` ORDER BY RAND() LIMIT 1;")[0] # 10% жертва из уже созданных лаб
                    
                    """Штука снизу отвечает за исключение повторных заражений, но мне дико не нравится, что теперь постоянно пишет, что жертва не найдена (это пишется потому, что очень мало игроков)"""
                    # victim = victim if len(lab.get_victums(f"WHERE `victums{lab.user_id}`.`user_id` LIKE '{victim['user_id']}' AND `victums{lab.user_id}`.`from_infect` <= {int(time.time()) - (60*60)}")) != 0 else None # проверка кд
                    
                else: victim = None # 10% неудачный поиск

            if victim == None: #при неудачном поиске пишет, что жертва не найдена
                lab.save()
                del lab
                await bot.send_message(message.chat.id, text=f"👺 Жертва не найдена!",  parse_mode="Markdown")
            else:

                attack_chance = random.random() # рандом от 0 до 1
                success = False
                    
                labOfVictim = labs.get_lab(victim['user_id']) # лаба жертвы

                if labOfVictim.has_lab: # если у жертвы есть лаба, то по другому пересчитывать шансы

                    delta = labOfVictim.immunity - lab.infectiousness # разница заразности и иммунитета

                    if delta <= 0: #если иммун жертвы меньше/равно заразности атакующего, то успех 100%
                        success = True
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1

                    # elif attempts > 1: # если применяет несколько попыток заражения, считается по экспоненте 1/(x^2)
                    #     pats = 0
                    #     for i in range(attempts):
                    #         if lab.patogens <= 0: break
                    #         lab.all_operations += 1
                    #         lab.patogens -= 1
                    #         pats += 1
                    #         success = random.random()
                    #         if success: break

                else:
                    if attempts > 1: # если попыток задано больше 1, то он увеличивает шанс на поражение :)
                        pats = 0
                        for i in range(attempts):
                            if lab.patogens <= 0: break
                            lab.all_operations += 1
                            lab.patogens -= 1
                            pats += 1
                            success = random.random() > 0.3
                            if success: break

                    elif attack_chance < 0.2: # 20% шанс на неудачу при атаке, success остается False по умолчанию
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1
                    else: # если все другие иф не сработали, то значит успешно пробил 
                        success = True
                        lab.all_operations += 1
                        lab.patogens -= 1
                        pats = 1
                if success: # если по всем шансам прошло успешно, то идет дальше отрабатывать жертву 
                    if labOfVictim.has_lab:

                        labOfVictim.all_issue += 1

                        profit = int(labOfVictim.bio_exp / 10)
                        profit = 1 if profit < 1 else profit # мин профит 1

                        labOfVictim.bio_exp -= int(labOfVictim.bio_exp / 10)
                        labOfVictim.bio_exp = 1 if labOfVictim.bio_exp < 1 else labOfVictim.bio_exp # чтобы не ушло в 0 или -

                        labOfVictim.save()

                    else: profit = random.randint(1, 100)

                    lab.save_victum(victim['user_id'], profit)
                    lab.save()

                    text = f"😎 Вы подвергли заражению пользователя "
                    text += f"[{victim['name']}](tg://openmessage?user_id={victim['user_id']})\n\n"
                    text += f"🧪 Затрачено патогенов `{pats}`.\n"
                    text += f"☠️ Заражение на `{lab.mortality}` "      
                    text += await skloneniye(lab.mortality)
                    text += ".\n"
                    text += f"☣️ `{profit}` био-опыта."

                    await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
                        
                    ''' Отправка уведомления '''

                    if labOfVictim.has_lab:
                        chat = labOfVictim["virus_chat"]
                        text = ""
                        chance = random.randint(1, 100)

                        if lab.security < labOfVictim.security:

                            if pats > 1:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\nБыло произведено {pats} попыток вашего заражения\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            else:
                                text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            await bot.send_message(chat_id=chat, text=text, parse_mode="Markdown")
                            return

                        if lab.security > labOfVictim.security :
                            
                            sp = (lab.infectiousness - labOfVictim.security)**2

                            if chance > sp:
                                
                                if pats > 1:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\nБыло произведено {pats} попыток вашего заражения\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                                else:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\n[{lab["name"]}](tg://openmessage?user_id={lab["user_id"]}) подверг вас заражению.\n\nНазвание патогена: `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            else:
                                
                                if pats > 1:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\nБыло произведено {pats} попыток вашего заражения\n\n_Вы потеряли ☣️ {profit} опыта_'
                                else:
                                    text += f'👨🏻‍🔬 Корпорация докладывает: \n\nВас пытались заразить вирусом под названием `{lab["patogen_name"] if lab["patogen_name"] != None else "Неизвестно"}`\n\n_Вы потеряли ☣️ {profit} опыта_'
                            
                            
                            await bot.send_message(chat_id=chat, text=text, parse_mode="Markdown")

                else:
                    await bot.send_message(message.chat.id, text=f"👺 Попытка заразить [{victim['name']}](tg://openmessage?user_id={victim['user_id']}) провалилась!\nВероятно у вашего вируса слабая заразность.",  parse_mode="Markdown")
                    
                    labOfVictim = labs.get_lab(victim['user_id'])
                    if labOfVictim.has_lab:
                        labOfVictim.all_issue += 1
                        labOfVictim.save()
