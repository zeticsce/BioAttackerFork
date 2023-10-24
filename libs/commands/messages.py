from typing import Any
from app import strconv

def skloneniye(num):
    names = ['день', 'дня', 'дней']
    n = num % 100
    if n >= 5 and n <= 20: return names[2]
    n = num % 10
    if n == 1: return names[0]
    if n >= 2 and n <= 4: return names[1]
    return names[2]

start_text = (
    "🧪 Вступи в смертельную игру биовойн!\n\n",
    "🌡️ Готов поиграть с жизнями?\n\n",
    "💣 Завоевывай мир своим вирусом!\n\n",
    "🧬 Готов к биологическому хаосу?\n\n",
    "🦠 Создай собственный патоген!\n\n",
    "🔬 Добро пожаловать в биолабораторию!\n\n",
    "💉 Погрузись в мир вирусов!\n\n"
)

''' Стандартная тема '''
theme = {
    "standard" : {
        "theme_name" : "Стандартная тема",
        "theme_desc" : "Дефолтная тема для олдов био-войн",

        "biolab" : {
            "info" : "🦠 Информация о вирусе",
            "owner" : "👺 Владелец",
            "corp" : "🏛 Корпорация",
            "pats" : "🧪 Патогенов",
            "new" : "⏱ До нового патогена",
            "quala" : "👨🏻‍🔬 Разработка",
            "zz" : "🦠 Заразность",
            "im" : "🛡 Иммунитет",
            "ll" : "☠️ Летальность",
            "bp" : "🕵️‍♂️ Безопасность",
            "exp" : "☣️ Био-опыт",
            "res" : "🧬 Био-ресурс",
            "operate" : "😷 Спецопераций",
            "issue" : "🥽 Предотвращены",
            "skills" : "НАВЫКИ",
            "data" : "ДАННЫЕ"

        },

        "errors" : {
            "wait" : "👺 Жди новых патогенов!",
            "10" : "👺 За раз максимум 10 попыток!",
            "404" : "👺 Юзер не найден!",
            "again" : "👺 Ты сможешь заразить его повторно через",
            "bot" : "👺 Нельзя заразить бота!",
            "victim" : "👺 Жертва не найдена!"
        }
    },

    "hell" : {
        "theme_name" : "Хеллоуинская тема",
        "theme_desc" : "Тема в честь Хеллоуина",

        "biolab" : {
            "info" : "👻 Название розыгрыша",
            "owner" : "👺 Владелец",
            "corp" : "🏛 Корпорация",
            "pats" : "🪄 ужастиков",
            "new" : "⏱ Новый ужастик",
            "quala" : "🧛 Квалификация колдунов",
            "zz" : "🌘 Ужасность",
            "im" : "🌕 Стойкость",
            "ll" : "🦇 Кровожадность",
            "bp" : "🕵️‍♂️ Ночная служба",
            "exp" : "🩸 Адреналин",
            "res" : "🧬 Био-ресурс",
            "operate" : "😷 Розыгрышей",
            "issue" : "🥽 Предотвращены",
            "skills" : "НАВЫКИ",
            "data" : "ДАННЫЕ"

        },

        "errors" : {
            "wait" : "👺 Жди новых розыгрышей!",
            "10" : "👺 За раз максимум 10 розыгрышей!",
            "404" : "👺 Юзер не найден!",
            "again" : "👺 Ты сможешь напугать его повторно через",
            "bot" : "👺 Нельзя напугать бота!",
            "victim" : "👺 Жертва не найдена!"
        }
    },

    "ukraine" : {
        "theme_name" : "Украинская тема",
        "theme_desc" : "Стандартна тема але українською мовою",

        "biolab" : {
            "info" : "🦠Інформація про вірус",
            "owner" : "👺 Власник",
            "corp" : "🏛 Ватага",
            "pats" : "🧪 Патогенів",
            "new" : "⏱ До нового патогена",
            "quala" : "👨🏻‍🔬 Розробка",
            "zz" : "🦠 Токсичність",
            "im" : "🛡 Стійкість",
            "ll" : "☠️ Час гепертонії",
            "bp" : "🕵️‍♂️ Антивірус",
            "exp" : "☣️ Біо-досвід",
            "res" : "🧬 Біо-ресурс",
            "operate" : "😷 Спецоперація",
            "issue" : "🥽 Соснули пипку",
            "skills" : "НАВИКИ",
            "data" : "ДАНІ"

        },

        "errors" : {
            "wait" : "👺 Чекай нових патогенів!",
            "10" : "👺 За раз не більше 10 патів!",
            "404" : "👺 Юзер не знайдений!",
            "again" : "👺 Можна йобнути знову через ",
            "bot" : "👺 Не можна йобнути бота!",
            "victim" : "👺 Йолоп не знайдений!"
        }
    },

    "azeri" : {
        "theme_name" : "Азербайджанская тема",
        "theme_desc" : "Тема для Азербайджанцев. ВНИМАНИЕ! СОДЕРЖИТ НЕЦЕНЗУРНУЮ ЛЕКСИКУ 18+!!1!",

        "biolab" : {
            "info" : "🦠 баздыгын сохбети",
            "owner" : "👺 Хан",
            "corp" : "🏛 Азерчай",
            "pats" : "🧪 Баздыглар",
            "new" : "⏱ До нового баздыга",
            "quala" : "👨🏻‍🔬 Пейсярляр",
            "zz" : "🦠 Дашагын бойу",
            "im" : "🛡 Готунун бойу",
            "ll" : "☠️ Агзынын бойу",
            "bp" : "🕵️‍♂️ Атонлар",
            "exp" : "☣️ Био-манатлар",
            "res" : "🧬 Био-гяпийляр",
            "operate" : "😷 Спецопераций",
            "issue" : "🥽 Предотвращены",
            "skills" : "ГЕХПЕЕЕЕ",
            "data" : "ГИЖДЫЛЛАААХ"

        },

        "errors" : {
            "wait" : "👺 гиждыллах, патогенляр йохду бле!",
            "10" : "👺 пейсяр, максимум 10 дяфя!",
            "404" : "👺 сикимин башы бля!",
            "again" : "👺 Ону йеня сикмяк олар сонра",
            "bot" : "👺 Боту сикмяк гадагандыр!",
            "victim" : "👺 Гяхпяни тампадын!"
        }
    },
    "mafia" : {
        "theme_name" : "Тема Мафия",
        "theme_desc" : "💰 Деньги и власть – основные ценности мафии, ты поднимешься к вершине преступного мира, либо станешь жертвой своей собственной доверчивости",

        "biolab" : {
            "info" : "🗂 Приём вербовки",
            "owner" : "🕵🏻‍♂️ Мафиози",
            "corp" : "🏛 В составе картеля",
            "pats" : "🚬 Придумано заманух",
            "new" : "⏳ Новая замануха",
            "quala" : "🥷 Квалификация вербовщиков",
            "zz" : "🔪 Убойность",
            "im" : "🔒 Защищенность",
            "ll" : "☠️ Смертоносность",
            "bp" : "🚓 Безнаказанность",
            "exp" : "💰 Добыча",
            "res" : "🏦 Криминальные доходы",
            "operate" : "😎 Выполнено заказов",
            "issue" : "🥽 Пресечено",
            "skills" : "НАВЫКИ",
            "data" : "ДАННЫЕ"

        },

        "errors" : {
            "wait" : "🚬 Жди новых идей для заманух!",
            "10" : "🔫 За раз только 10 попыток, брад!",
            "404" : "🔫 404! Нацелился не на того!",
            "again" : "🔫 Повторно вербовать можно только через",
            "bot" : "🤖 Забудь про бота, они не поддаются вербовке!",
            "victim" : "🔫 Цель не найдена, браток свинтил!"
        }
    },
}
def illness_check(lab):
    text = f""
    if lab.patogen_name is not None:
        text = f"🥴 У вас горячка вызванная патогеном «`{lab.illness['patogen']}`»\n\n"
    else:
        text = f"🥴 У вас горячка вызванная неизвестным патогеном \n\n"
    return text

def patogenName(lab, theme=""):
    if theme == "":
        if lab.theme == "azeri":
            howfuck = "баздыгом"
        elif lab.theme == "mafia":
            howfuck = "приемом"
        elif lab.theme == "hell":
            howfuck = "розыгрышем"
        else:
            howfuck = "патогеном"
    else:
        if theme == "azeri":
            howfuck = "баздыгом"
        elif theme == "mafia":
            howfuck = "приемом"
        elif theme == "hell":
            howfuck = "розыгрышем"
        else:
            howfuck = "патогеном"

    return f"{howfuck} «<code>{lab.patogen_name}</code>»" if lab.patogen_name is not None else f"неизвестным {howfuck}"


def sbService(suc, hidden, equal, theme, first_id, first_name, second_id, second_name, atts, patogen_name="", profit=0):

    hide_victim_link = f'<a href="tg://user?id={second_id}">\xad</a>'
    hide_attacker_link = f'<a href="tg://user?id={first_id}">\xad</a>'
    if suc == 1:

        if theme is None:
            organizer = "Организатор"
            full_attempt = "👨🏻‍🔬 Была проведена операция вашего заражения"
            short_attempt = "👨🏻‍🔬 Была проведена операция заражения"
            lost = "🧪 Совершено минимум"
            you_lost = "☣️ Вы потеряли"
            bio = "био"

            alternative = "👨🏻‍🔬 Вас подвергли заражению"
            alter_lost = "☣️ Потерял"
            alter_attempt = "был подвергнут заражению"

        elif theme == "azeri":
            organizer = "Пейсяр"
            full_attempt = "👨🏻‍🔬 Сын пейсяр чыхдын"
            short_attempt = "👨🏻‍🔬 Сяни сикди"
            lost = "🧪 Патогенляр сычды"
            you_lost = "☣️ мантлары сычдын"
            bio = "манат"

            alternative = "👨🏻‍🔬 Сяни сиктиляр"
            alter_lost = "☣️ Сычдын"
            alter_attempt = "ону сиктиляр"

        elif theme == "ukraine":
            organizer = "Злочинець"
            full_attempt = "👨🏻‍🔬 Була спроба вашого вбивства "
            short_attempt = "👨🏻‍🔬 Була проведена операція вбивства"
            lost = "🧪 Здійснено мінімум "
            you_lost = "☣️ Ви проєбали "
            bio = "біо"

            alternative = "👨🏻‍🔬 Вас йобнули"
            alter_lost = "☣️ Проєбав "
            alter_attempt = "був йобнутий"

        elif theme == "hell":
            organizer = "Организатор розыгрыша"
            full_attempt = "👨🏻‍🔬 Только что вас напугали"
            short_attempt = "👨🏻‍🔬 Только что напугали"
            lost = "👻 Совершено минимум"
            you_lost = "🩸 Вы потеряли"
            bio = "адреналина"

            alternative = "👨🏻‍🔬 Вас напугали"
            alter_lost = "🩸 Потерял"
            alter_attempt = "напугали"

        if hidden:
            if equal:
                sb_text = f'{full_attempt} {patogen_name}.\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n\n'\
                        f'{lost} {atts} попыток!\n'\
                        f'{you_lost} <code>{profit}</code> {bio}.'
            else:
                sb_text = f'{short_attempt} '\
                        f'<a href="tg://openmessage?user_id={second_id}">{second_name}</a> {patogen_name}.\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n\n'\
                        f'{lost} {atts} попыток!\n'\
                        f'{you_lost} <code>{profit}</code> {bio}.'\
                        f'{hide_victim_link}'
        else:
            if equal:
                sb_text = f"{alternative} {patogen_name}\n\n"\
                        f"{you_lost} <code>{strconv.format_nums(profit)}</code> {bio}."
            else:
                sb_text = f'👨🏻‍🔬 <a href="tg://openmessage?user_id={second_id}">{second_name}</a> '\
                        f'{alter_attempt} {patogen_name}\n\n'\
                        f'{alter_lost} <code>{strconv.format_nums(profit)}</code> {bio}.'

        sb_text += f"{hide_victim_link}"            


    else:
        if theme is None:
            organizer = "Организатор"
            full_attempt = "👺 Попытка вашего заражения провалилась!"
            short_attempt = "👺 Попытка заразить"

        elif theme == "azeri":
            organizer = "Пейсяр"
            full_attempt = "👺 Сяни вуранда озю пейсяр чыхды!"
            short_attempt = "👺 Сяни сикмяк"

        elif theme == "hell":
            organizer = "Организатор розыгрыша"
            full_attempt = "👺 Вас пытались напугать, но вы и бровью не пошевелили!"
            short_attempt = "👺 Попытка напугать"

        elif theme == "ukraine":
            organizer = "Злочинець"
            full_attempt = "👺 Спроба вашого вбивства провалилася!"
            short_attempt = "👺 Спроба вбивства"

        if hidden:
            if equal:
                sb_text = f'{full_attempt}\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n'\
                        f'Совершено минимум <i>{atts}</i> попыток!'
            else:
                sb_text = f'{short_attempt} '\
                        f'<a href="tg://openmessage?user_id={second_id}">{second_name}</a> провалилась!'\
                        f'\n\{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n'\
                        f'Совершено минимум <i>{atts}</i> попыток!'\
                        f'{hide_victim_link}'
        else:
            if equal:
                sb_text = f'{full_attempt}\n\n'\
                    f'Совершено минимум <i>{atts}</i> попыток!'
            else:
                sb_text = f'{short_attempt} '\
                    f'<a href="tg://user?id={second_id}">{second_name}</a> провалилась!\n\n'\
                    f'Совершено минимум <i>{atts}</i> попыток!'

    return sb_text


def attackText(theme, new, first_name, second_name, first_id, second_id, patogen_name, atts, profit, mortality):
    rslt_text = f""

    if theme == "azeri":
        ''' Азербайджанская тема '''
        fucked = "сикди"
        spend = "🧪 патогенляр гетди"
        gain = "☣️ Бу гяхпя верир"
        bio_res = "био-манатлар"
        infect = "☠️ Заражение на"
        lol = "👨‍🔬 Бу гехпе сенин деильди!!! Амма инди сяниндир)"

    elif theme == "mafia":
        ''' Мафиозная тема '''
        fucked = "успешно завербовал"
        spend = "💉 Использовано энергии"
        gain = "💰 Отобрано"
        bio_res = "манат"
        infect = "⏳ Останется на поводке клана в течение"
        lol = "🥷 Вы пополнили список своих шестерок новым осведомителем"

    elif theme == "hell":
        ''' Хеллоуин '''
        fucked = "напугал"
        spend = "👻 Потрачено ужастиков"
        gain = "🩸 Получено"
        bio_res = "адреналина"
        infect = "🌙 Пугающий эффект продлится"
        lol = "🎃 Жертва впервые встретилась с вашей шалостью и будет в шоке"

    elif theme == "ukraine":
        ''' Украинская тема '''
        fucked = "йобнув"
        spend = "🧪 Затрачено патогенів"
        gain = "☣️ Йолоп приносить"
        bio_res = "біо-ресурса"
        infect = "☠️ Гіпертонія на"
        lol = "👨‍🔬 Йолоп ще не був йобнутий вашим патогеном"

    else:
        ''' Стандартная тема '''
        fucked = "подверг заражению"
        spend = "🧪 Затрачено патогенов"
        gain = "☣️ Жертва приносит"
        bio_res = "био-ресурса"
        infect = "☠️ Заражение на"
        lol = "👨‍🔬 Объект ещё не подвергался заражению вашим патогеном"

    hide_victim_link = f'<a href="tg://user?id={second_id}">\xad</a>'
    hide_attacker_link = f'<a href="tg://user?id={first_id}">\xad</a>'

    rslt_text = f"😎 <a href='tg://openmessage?user_id={first_id}'>{first_name}</a>" \
                f" {fucked} " \
                f"<a href='tg://openmessage?user_id={second_id}'>{strconv.normalaze(second_name, replace=str(second_id))}</a>"\
                f" {patogen_name}\n\n"\
                f"{spend}: <i>{atts}</i>\n"\
                f"{gain} <i>{strconv.format_nums(profit)}{bio_res}</i>\n"\
                f"{infect} <i>{mortality} {skloneniye(mortality)}</i>"

    if new:
        rslt_text += f"\n\n<i>{lol}</i>"

    rslt_text += f"{hide_victim_link}"

    return rslt_text

heal_text = (
    "💊 Купить Обезболивающее",
    "💊 Купить Аптечку",
    "☕️ Выпить малиновый чай",
    "🍵 Выпить зеленый чай",
    "👨🏼‍⚕️ Пойти к врачу",
    "💉 Вколоть Антидот"
)

fuck_against = {
    "standard" : "Заразить в ответ",
    "azeri" : "Выебать",
    "hell" : "Напугать в ответ",
    "ukraine" : "Йобнути у відповідь "
}
