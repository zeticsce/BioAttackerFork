'''

Модуль с прокачками лаб

'''

import os
import re

from app import dp, bot, strconv
from libs.handlers import labs

from aiogram import types

from math import floor

work_path = os.path.abspath(os.curdir)

def impr_price(start, end, power):
    price = 0
    for i in range(int(end) - int(start)):
        price += floor((int(start) + i + 1) ** power)
    return price

@dp.message_handler(content_types=["text"])
async def improve(message: types.Message):

    if message.text.startswith("+"):

        lab = labs.get_lab(message['from']['id'])

        imps={}
        imps["попыток"] = re.fullmatch(r"(\+\+|\+)([а-я]+)(\s\d+)?", message.text.lower()) # если imps["попыток"] будет None, то это невалидное сообщение

        if lab.has_lab and imps["попыток"] is not None: # проверка существует ли лаба, если лабы нет, то пусть вообще не отвечает

            imps["патоген"] =      re.fullmatch(r"(\+\+|\+)(патоген|пат)(\s\d+)?", message.text.lower())
            imps["квалификация"] = re.fullmatch(r"(\+\+|\+)(разработка|квала|квалификация)(\s\d+)?", message.text.lower())
            imps["заразность"] =   re.fullmatch(r"(\+\+|\+)(зз|заразность)(\s\d+)?", message.text.lower())
            imps["иммунитет"] =    re.fullmatch(r"(\+\+|\+)(иммун|иммунитет)(\s\d+)?", message.text.lower())
            imps["летальность"] =  re.fullmatch(r"(\+\+|\+)(летал|летальность)(\s\d+)?", message.text.lower())
            imps["безопасность"] = re.fullmatch(r"(\+\+|\+)(сб|безопасность)(\s\d+)?", message.text.lower())

            atts = int(imps["попыток"].group(3)) if imps["попыток"].group(3) is not None else 1
            text = None

            if atts <= 10000:
                if imps["попыток"].group(1) == "+": # тут проверяется колво плюсов, может быть только один или два

                    if imps["патоген"] is not None:
                        price = strconv.format_nums(impr_price(lab.all_patogens, lab.all_patogens + atts, 2.0))
                        text = f"Прокачка патоегна с _{lab.all_patogens} ур._ до _{lab.all_patogens + atts} ур._ обойдется вам в _{price} био_"

                    elif imps["квалификация"] is not None:
                        price = strconv.format_nums(impr_price(lab.qualification, lab.qualification + atts, 2.6))
                        text = f"Прокачка квалификации с _{lab.qualification} ур._ до _{lab.qualification + atts} ур._ обойдется вам в _{price} био_"
                        if lab.qualification < 60:
                            atts = atts if lab.qualification + atts <= 60 else 60 - lab.qualification
                            price = impr_price(lab.qualification, lab.qualification + atts, 2.6)
                            text = f"Прокачка квалификации с _{lab.qualification} ур._ до _{lab.qualification + atts} ур._ обойдется вам в _{price} био_"
                        else: text = f"У вас уже максимальный уровень!"

                    elif imps["заразность"] is not None:
                        price = strconv.format_nums(impr_price(lab.infectiousness, lab.infectiousness + atts, 2.5))
                        text = f"Прокачка заразности с _{lab.infectiousness} ур._ до _{lab.infectiousness + atts} ур._ обойдется вам в _{price} био_"

                    elif imps["иммунитет"] is not None:
                        price = strconv.format_nums(impr_price(lab.immunity, lab.immunity + atts, 2.5))
                        text = f"Прокачка иммунитета с _{lab.immunity} ур._ до _{lab.immunity + atts} ур._ обойдется вам в _{price} био_"

                    elif imps["летальность"] is not None:
                        price = strconv.format_nums(impr_price(lab.mortality, lab.mortality + atts, 1.95))
                        text = f"Прокачка летальности с _{lab.mortality} ур._ до _{lab.mortality + atts} ур._ обойдется вам в _{price} био_"

                    elif imps["безопасность"] is not None:
                        price = strconv.format_nums(impr_price(lab.security, lab.security + atts, 2.1))
                        text = f"Прокачка безопасности с _{lab.security} ур._ до _{lab.security + atts} ур._ обойдется вам в _{price} био_"

                else:

                    if imps["патоген"] is not None:
                        price = impr_price(lab.all_patogens, lab.all_patogens + atts, 2.0)
                        text = f"Вы успешно увеличили максимальное колличество патоегенов с _{lab.all_patogens}_ до _{lab.all_patogens + atts}_\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                        if lab.bio_res > price:
                            lab.all_patogens += atts
                            lab.patogens = lab.patogens + atts if lab.patogens + atts <= lab.all_patogens else lab.all_patogens
                            lab.bio_res -= price
                        elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                            text = f"Вы успешно увеличили максимальное колличество патоегенов с _{lab.all_patogens}_ до _{lab.all_patogens + atts}_."
                            text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                            lab.coins -= (price - lab.bio_res)
                            lab.bio_res -= lab.bio_res
                            lab.all_patogens += atts
                            lab.patogens = lab.patogens + atts if lab.patogens + atts <= lab.all_patogens else lab.all_patogens
                        else: text = f"Недостаточно био-ресурса!"

                    elif imps["квалификация"] is not None:
                        if lab.qualification < 60:
                            atts = atts if lab.qualification + atts <= 60 else 60 - lab.qualification
                            price = impr_price(lab.qualification, lab.qualification + atts, 2.6)
                            text = f"Вы успешно прокачали квалификацию с _{lab.qualification} ур._ до _{lab.qualification + atts} ур._\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                            if lab.bio_res > price:
                                lab.qualification += atts
                                lab.bio_res -= price
                            elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                                text = f"Вы успешно прокачали квалификацию с _{lab.qualification} ур._ до _{lab.qualification + atts} ур_."
                                text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                                lab.coins -= (price - lab.bio_res)
                                lab.bio_res -= lab.bio_res
                                lab.qualification += atts

                            else: text = f"Недостаточно био-ресурса!"
                        else: text = f"У вас уже максимальный уровень!"

                    elif imps["заразность"] is not None:
                        price = impr_price(lab.infectiousness, lab.infectiousness + atts, 2.5)
                        text = f"Вы успешно прокачали заразность с _{lab.infectiousness} ур._ до _{lab.infectiousness + atts} ур._\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                        if lab.bio_res > price:
                            lab.infectiousness += atts
                            lab.bio_res -= price
                        elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                            text = f"Вы успешно прокачали заразность с _{lab.infectiousness} ур._ до _{lab.infectiousness + atts} ур._"
                            text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                            lab.coins -= (price - lab.bio_res)
                            lab.bio_res -= lab.bio_res
                            lab.infectiousness += atts
                        else: text = f"Недостаточно био-ресурса!"

                    elif imps["иммунитет"] is not None:
                        price = impr_price(lab.immunity, lab.immunity + atts, 2.5)
                        text = f"Вы успешно прокачали иммунитет с _{lab.immunity} ур._ до _{lab.immunity + atts} ур._\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                        if lab.bio_res > price:
                            lab.immunity += atts
                            lab.bio_res -= price
                        elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                            text = f"Вы успешно прокачали иммунитет с _{lab.immunity} ур._ до _{lab.immunity + atts} ур._"
                            text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                            lab.coins -= (price - lab.bio_res)
                            lab.bio_res -= lab.bio_res
                            lab.immunity += atts
                        else: text = f"Недостаточно био-ресурса!"

                    elif imps["летальность"] is not None:
                        price = impr_price(lab.mortality, lab.mortality + atts, 1.95)
                        text = f"Вы успешно прокачали летальность с _{lab.mortality} ур._ до _{lab.mortality + atts} ур._\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                        if lab.bio_res > price:
                            lab.mortality += atts
                            lab.bio_res -= price
                        elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                            text = f"Вы успешно прокачали летальность с _{lab.mortality} ур._ до _{lab.mortality + atts} ур_."
                            text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                            lab.coins -= (price - lab.bio_res)
                            lab.bio_res -= lab.bio_res
                            lab.mortality += atts
                        else: text = f"Недостаточно био-ресурса!"

                    elif imps["безопасность"] is not None:
                        price = impr_price(lab.security, lab.security + atts, 2.1)
                        text = f"Вы успешно прокачали безопасность с _{lab.security} ур._ до _{lab.security + atts} ур._\n Это обошлось вам в _{strconv.format_nums(price)} 🧬_"
                        if lab.bio_res > price:
                            lab.security += atts
                            lab.bio_res -= price
                        elif lab.bio_res - price <= 0 and lab.bio_res + lab.coins >= price:
                            text = f"Вы успешно прокачали безопасность с _{lab.security} ур._ до _{lab.security + atts} ур._"
                            text += f"\nЭто обошлось вам в _{strconv.format_nums(lab.bio_res)}_ 🧬 и _{strconv.format_nums(price - lab.bio_res)}_ 💰" 
                            lab.coins -= (price - lab.bio_res)
                            lab.bio_res -= lab.bio_res
                            lab.security += atts
                        else: text = f"Недостаточно био-ресурса!"

                    lab.save()

            else: text = f"Вы не можете прокачать более _1000 уровней_ за раз!"

            if text is not None: await bot.send_message(message.chat.id, text=text, parse_mode="Markdown")
