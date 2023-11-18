from typing import Any
from app import strconv

def skloneniye(num, theme):
    if theme == "english":
        names = ['day', 'days', 'days']
    elif theme == "ukraine":
        names = ['день', 'дня', 'днів']
    else:
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
        "theme_name" : "🇷🇺 Стандартная тема",
        "theme_desc" : "Дефолтная тема для олдов био-войн",
        "type" : "language",
        "price" : 0,

        "minilab": {
            "lab": """
👺 Владелец: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Патогенов: {pats} из {all_pats}
☣️ Био-опыт: {bio_exp}
🧬 Био-ресурс: {bio_res}{fever}""",
            "no lab name": "им. {name}",
            "corp": '\n🏛 Корпорация «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас горячка вызванная патогеном «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас горячка вызванная неизвестным патогеном ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🦠 Информация о вирусе: <code>{patogen_name}</code>

👺 Владелец: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Патогенов: {pats} из {all_pats} (<code>+{pats_calk}</code>)
👨🏻‍🔬 Разработка: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🔬 НАВЫКИ:</b>
🦠 Заразность: {infect} ур. (<code>+{infect_calk}</code>)
🛡 Иммунитет: {immunity} ур. (<code>+{immunity_calk}</code>)
☠️ Летальность: {mortality} ур. (<code>+{mortality_calk}</code>)
🕵️‍♂️ Безопасность: {security} ур. (<code>+{security_calk}</code>)

<b>⛩ ДАННЫЕ:</b>
☣️ Био-опыт: {bio_exp}
🧬 Био-ресурс: {bio_res}
😷 Спецопераций: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🥽 Предотвращены: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏛 Корпорация «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас горячка вызванная патогеном «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас горячка вызванная неизвестным патогеном ещё <code>{fever_time} мин.</code>",
            "no fever": "",
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

     "dream" : {
        "theme_name" : "🌙 Спокойной ночи",
        "theme_desc" : "Тема чтобы попытатся уснуть",
        "type" : "arcade",
        "price" : 5000,

         "minilab": {
            "lab": """
👨‍⚕️ Профессор: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

💊 Таблеток: {pats} из {all_pats}
🌌 Сон-опыт: {bio_exp}
✨ Сон-ресурс: {bio_res}{fever}""",
            "no lab name": "им. {name}",
            "corp": '\n🕍 Дворец Снов «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До новой таблетки: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До новой таблетки: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥱 У вас сонливость вызванная таблеткой «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥱 У вас сонливость вызванная неизвестной таблеткой ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """💤 Информация о снотворном: <code>{patogen_name}</code>

👨‍⚕️ Профессор: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

💊 Таблеток: {pats} из {all_pats} (<code>+{pats_calk}</code>)
🧑‍🔬 Изготовление: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🔬 НАВЫКИ:</b>
💤 Сонливость: {infect} ур. (<code>+{infect_calk}</code>)
🛡 Устойчивость: {immunity} ур. (<code>+{immunity_calk}</code>)
⏱ Время сна: {mortality} ур. (<code>+{mortality_calk}</code>)
🧚 Информация от Феи: {security} ур. (<code>+{security_calk}</code>)

<b>⛩ ДАННЫЕ:</b>
🌌 Сон-опыт: {bio_exp}
✨ Сон-ресурс: {bio_res}
😴 Подвержены: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
👌 Предотвращены: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🕍 Дворец Снов «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До новой таблетки: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До новой таблетки: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥱 У вас сонливость вызванная таблеткой «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥱 У вас сонливость вызванная неизвестной таблеткой ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "errors" : {
            "wait" : "⛔️ Жди новых таблеток!",
            "10" : "⛔️ За раз максимум 10 попыток!",
            "404" : "⛔️ Юзер не найден!",
            "again" : "⛔️ Ты сможешь подвергнуть сонливостью его повторно через",
            "bot" : "⛔️ Нельзя подвергнуть сонливостью бота!",
            "victim" : "⛔️ Человек не найден!"
        }
    },


    "hell" : {
        "theme_name" : "🩸 Хеллоуинская тема",
        "theme_desc" : "Тема в честь Хеллоуина",
        "type" : "arcade",
        "price" : 1000,

        "minilab": {
            "lab": """
👺 Владелец: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🪄 ужастиков: {pats} из {all_pats}
🩸 Адреналин: {bio_exp}
🧬 Сладостей: {bio_res}{fever}""",
            "no lab name": "им. {name}",
            "corp": '\n🏛 Корпорация «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ Новый ужастик: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ Новый ужастик: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 Вы в шоке с розыгрыша «<code>{fever_name}</code>» ещё {fever_time} мин!",
            "fever": "\n\n🥴 У вас шок от неизвестного розыгрыша ещё {fever_time} мин.",
            "no fever": "",
        },

        "biolab" : {
            "lab": """👻 Название розыгрыша: <code>{patogen_name}</code>

👺 Владелец: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🪄 ужастиков: {pats} из {all_pats} (<code>+{pats_calk}</code>)
🧛 Квалификация колдунов: {qual} (<code>{qualification_calk}</code>){new_patogen}

🔬 НАВЫКИ:
🌘 Ужасность: {infect} ур. (<code>+{infect_calk}</code>)
🌕 Стойкость: {immunity} ур. (<code>+{immunity_calk}</code>)
🦇 Кровожадность: {mortality} ур. (<code>+{mortality_calk}</code>)
🕵️‍♂️ Ночная служба: {security} ур. (<code>+{security_calk}</code>)

⛩ ДАННЫЕ:
🩸 Адреналин: {bio_exp}
🧬 Сладостей: {bio_res}
😷 Розыгрышей: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🥽 Предотвращены: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏛 Корпорация «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ Новый ужастик: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ Новый ужастик: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 Вы в шоке с розыгрыша «<code>{fever_name}</code>» ещё {fever_time} мин!",
            "fever": "\n\n🥴 У вас шок от неизвестного розыгрыша ещё {fever_time} мин.",
            "no fever": "",
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
        "theme_name" : "🇺🇦 Украинская тема",
        "theme_desc" : "Стандартна тема але українською мовою",
        "type" : "language",
        "price" : 100,

        "minilab": {
            "lab": """
👺 Власник: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Патогенів: {pats} из {all_pats}
☣️ Біо-досвід: {bio_exp}
🧬 Біо-ресурси: {bio_res}{fever}""",

            "no lab name": "им. {name}",
            "corp": '\n🏛 Хата «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> хв.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас лихоманка через вірус «<code>{fever_name}</code>» ще <code>{fever_time} хв.</code>",
            "fever": "\n\n🥴 У вас лихоманка через невідомий вірус ще <code>{fever_time} хв.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🦠 Інформація про вірус: <code>{patogen_name}</code>

👺 Власник: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Патогенів: {pats} з {all_pats} (<code>+{pats_calk}</code>)
👨🏻‍🔬 Розробка: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🔬 НАВИЧКИ:</b>
🦠 Заразність: {infect} рів. (<code>+{infect_calk}</code>)
🛡 Імунітет: {immunity} рів. (<code>+{immunity_calk}</code>)
☠️ Летальність: {mortality} рів. (<code>+{mortality_calk}</code>)
🕵️‍♂️ Служба безпеки: {security} рів. (<code>+{security_calk}</code>)

<b>⛩ ІНФОРМАЦІЯ:</b>
☣️ Біо-досвід: {bio_exp}
🧬 Біо-ресурси: {bio_res}
😷 Спецоперацій: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🥽 Соснули пуцку: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} хв. | +{qual_calk}",
            "qualification calk 60": "{qual_time} хв.",
            "corp": '\n🏛 Хата «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> хв.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас лихоманка через вірус «<code>{fever_name}</code>» ще <code>{fever_time} хв.</code>",
            "fever": "\n\n🥴 У вас лихоманка через невідомий вірус ще <code>{fever_time} хв.</code>",
            "no fever": "",
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
        "theme_name" : "🇦🇿 Азербайджанская тема",
        "theme_desc" : "Тема для Азербайджанцев. ВНИМАНИЕ! СОДЕРЖИТ НЕЦЕНЗУРНУЮ ЛЕКСИКУ 18+!!1!",
        "type" : "language",
        "price" : 100,

        "minilab": {
            "lab": """
💩 Хан: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🥒 Хыярлар: {pats} из {all_pats}
☣️ Био-манатлар: {bio_exp}
🧬 Био-гяпийляр: {bio_res}{fever}""",

            "no lab name": "им. {name}",
            "corp": '\n🏛 Азерчай «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового огурца: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового огурца: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас горячка вызванная огурцом «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас горячка вызванная неизвестным огурцом ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🦠 Хыярын сохбети: <code>{patogen_name}</code>

💩 Хан: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🥒 Хыярлар: {pats} из {all_pats} (<code>+{pats_calk}</code>){new_patogen}
👨🏻‍🔬 Хякимляр: {qual} (<code>{qualification_calk}</code>)

<b>🍆 Баклажаны:</b>
🦠 Сикимин бойу: {infect} ур. (<code>+{infect_calk}</code>)
🛡 Готун размери: {immunity} ур. (<code>+{immunity_calk}</code>)
☠️ Няняляр: {mortality} ур. (<code>+{mortality_calk}</code>)
🕵️‍♂️ Анти-полисляр: {security} ур. (<code>+{security_calk}</code>)

<b>🍅 Помидоры:</b>
☣️ Био-манатлар: {bio_exp}
🧬 Био-гяпийляр: {bio_res}
😷 Вурулду: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🥽 Сикмяди: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏛 Азерчай «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового огурца: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового огурца: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас горячка вызванная огурцом «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас горячка вызванная неизвестным огурцом ещё <code>{fever_time} мин.</code>",
            "no fever": "",
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

    "zombie" : {
        "theme_name" : "🧟 Зомби-Апокалипсис",
        "theme_desc" : "Любительское оформление по теме «Зомби-Апокалипсис»",
        "type" : "arcade",
        "price" : 5000,

        "minilab": {
            "lab": """
🧯 Выживший: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Мутагенов: {pats} из {all_pats}
🔬 Инфекто-опыт: {bio_exp}
💶 Инфекто-ресурсы: {bio_res}{fever}""",

            "no lab name": "им. {name}",
            "corp": '\n🏭 Гильдия «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового мутагена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового мутагена: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🌡 У вас горячка вызванная инфекцией «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🌡 У вас горячка вызванная неизвестной инфекцией ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🧟‍♀️ Название инфекции: <code>{patogen_name}</code>

🧯 Выживший: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Мутагенов: {pats} из {all_pats} (<code>+{pats_calk}</code>)
👨🏻‍🔬 Эволюция инфекции: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🖲 ТВОИ НАВЫКИ:</b>
🧫 Инфекционная способность: {infect} ур. (<code>+{infect_calk}</code>)
💉 Антитела: {immunity} ур. (<code>+{immunity_calk}</code>)
💀 Тяжесть инфекции: {mortality} ур. (<code>+{mortality_calk}</code>)
🕵🏻‍♂️ Контроль безопасности: {security} ур. (<code>+{security_calk}</code>)

<b>📟 ТВОЯ СТАТИСТИКА:</b>
🔬 Инфекто-опыт: {bio_exp}
💶 Инфекто-ресурсы: {bio_res}
🚁 Успешных миссий: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🚑 Предотвращено: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏭 Гильдия «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового мутагена: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового мутагена: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🌡 У вас горячка вызванная инфекцией «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🌡 У вас горячка вызванная неизвестной инфекцией ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "errors" : {
            "wait" : "🚒 Жди новых мутагенов!",
            "10" : "🚓 За один раз можно использовать максимум 10 попыток инфицировать!",
            "404" : "🚑 Человек не найден!",
            "again" : "🚛 Ты сможешь его инфицировать повторно через",
            "bot" : "🛵 Нельзя инфицировать бота!",
            "victim" : "🚙 Жертва для инфицирования не найдена!"
        }
    },

    "cookies" : {
        "theme_name" : "🧑‍🍳 Кулинарная тема",
        "theme_desc" : "Готовьте ваши лучшие рецепты блюд и угощайте всех вокруг вкусняшками!",
        "type" : "arcade",
        "price" : 5000,

        "minilab": {
            "lab": """
🧑‍🍳 Шеф-повар: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧁 Приготовлено вкусняшек: {pats} из {all_pats}
🙏 Благодарности: {bio_exp}
💵 Касса: {bio_res}{fever}""",

            "no lab name": "им. {name}",
            "corp": '\n🏛 Сеть кондитерских «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏳ Новая вкусняшка: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏳ Новая вкусняшка: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🍰 Ваша попа слиплась от чрезмерной сладости десерта «<code>{fever_name}</code>» еще на <code>{fever_time} мин.</code>",
            "fever": "\n\n🍰 Ваша попа слиплась от чрезмерной сладости еще на <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🏷 Название рецепта <code>{patogen_name}</code>

🧑‍🍳 Шеф-повар: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧁 Приготовлено вкусняшек: {pats} из {all_pats} (<code>+{pats_calk}</code>)
🎂 Квалификация пекаря: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🔬 НАВЫКИ:</b>
🍰 Сладость: {infect} ур. (<code>+{infect_calk}</code>)
🍪 Искушение: {immunity} ур. (<code>+{immunity_calk}</code>)
🍭 Незабываемость: {mortality} ур. (<code>+{mortality_calk}</code>)
🤐 Секретность рецептов: {security} ур. (<code>+{security_calk}</code>)

<b>⛩ ДАННЫЕ:</b>
🙏 Благодарности: {bio_exp}
💵 Касса: {bio_res}
😋 Выполнено заказов: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🤒 Раскритиковано блюд: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏛 Сеть кондитерских «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏳ Новая вкусняшка: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏳ Новая вкусняшка: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🍰 Ваша попа слиплась от чрезмерной сладости десерта «<code>{fever_name}</code>» еще на <code>{fever_time} мин.</code>",
            "fever": "\n\n🍰 Ваша попа слиплась от чрезмерной сладости еще на <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "errors" : {
            "wait" : "🧁 Нет вкусняшек для угощения!",
            "10" : "🧁 Не более 10 подач вкусняшек за раз!",
            "404" : "🧑‍🍳 Юзер не найден!",
            "again" : "🧑‍🍳 Ты сможешь угостить его повторно через",
            "bot" : "🧑‍🍳 Нельзя угощать роботов!",
            "victim" : "🧑‍🍳 Посетитель не найден!"
        }
    },

    "school" : {
        "theme_name" : "🏅 Школьная тема", 
        "theme_desc" : "Тема для школьников. ", 
        "type" : "arcade", 
        "price" : 5000, 

        "minilab": {
            "lab": """
💀 Учитель: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

💀 Доступных двоек: {pats} из {all_pats}
⚡️ Зарплата: {bio_exp}
🎖 Премия: {bio_res}{fever}""",

            "no lab name": "им. {name}",
            "corp": '\n⚠️ Учительская «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До новой двойки: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До новой двойки: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n💥 У вас расстройство,вызванное потерей зарплаты, «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас расстройство,вызванное потерей зарплаты, ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """😈 Информация о причине: <code>{patogen_name}</code>

💀 Учитель: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

💀 Доступных двоек: {pats} из {all_pats} (<code>+{pats_calk}</code>)
🤓 Отличников: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>😵 НАВЫКИ:</b>
👹 Злость: {infect} ур. (<code>+{infect_calk}</code>)
😓 Аргументность: {immunity} ур. (<code>+{immunity_calk}</code>)
☠️ Смертность: {mortality} ур. (<code>+{mortality_calk}</code>)
🤐 Внимательность: {security} ур. (<code>+{security_calk}</code>)

<b>👑 Кошелек:</b>
⚡️ Зарплата: {bio_exp}
🎖 Премия: {bio_res}
🎉 Удачных двоек: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🎁 Предотвращено потерей зарплаты: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "неизвестно",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n⚠️ Учительская «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До новой двойки: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До новой двойки: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n💥 У вас расстройство,вызванное потерей зарплаты, «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴 У вас расстройство,вызванное потерей зарплаты, ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "errors" : {
            "wait" : "😶 Жди новой двойки,еще {next_patogen_time} мин!",
            "10" : "😶 За раз максимум 10 попыток!",
            "404" : "😶 Фамилия не найдена!",
            "again" : "😶 Ты сможешь поставить ему двойку повторно через",
            "bot" : "😶 Нельзя поставить двойку тому,кто выше тебя по званию!",
            "victim" : "😶 Двоечник не найден!"
        }
    },

#     "mafia" : { # недоделка
#         "theme_name" : "🕵🏻‍♂️ Мафия",
#         "theme_desc" : "💰 Деньги и власть – основные ценности мафии, ты поднимешься к вершине преступного мира, либо станешь жертвой своей собственной доверчивости",
#         "type" : "arcade",
#         "price" : 5000,
#         "biolab" : {
#             "lab": """🦠 Информация о вирусе: {patogen_name}

# 🕵🏻‍♂️ Мафиози: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

# 🚬 Придумано заманух: {pats} из {all_pats} (<code>+{pats_calk}</code>)
# ⏳ Новая замануха: {qual} (<code>{qualification_calk}</code>){new_patogen}

# <b>🔬 НАВЫКИ:</b>
# 🔪 Убойность: {infect} ур. (<code>+{infect_calk}</code>)
# 🔒 Защищенность: {immunity} ур. (<code>+{immunity_calk}</code>)
# ☠️ Смертоносность: {mortality} ур. (<code>+{mortality_calk}</code>)
# 🚓 Безнаказанность: {security} ур. (<code>+{security_calk}</code>)

# <b>⛩ ДАННЫЕ:</b>
# 💰 Добыча: {bio_exp}
# 🏦 Криминальные доходы": {bio_res}
# 😎 Выполнено заказов: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
# 🥽 Пресечено: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

#             "no pathogen name": "неизвестно",
#             "no lab name": "им. {name}",
#             "qualification calk": "{qual_time} мин. | +{qual_calk}",
#             "qualification calk 60": "{qual_time} мин.",
#             "corp": '\n🏛 В составе картеля «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
#             "no corp": "",
#             "next patogen sec": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> сек.",
#             "next patogen min": "\n⏱ До нового патогена: <code>{next_patogen_time}</code> мин.",
#             "full patogens": "",
#             "fever patogen": "\n\n🥴 У вас горячка вызванная патогеном «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
#             "fever": "\n\n🥴 У вас горячка вызванная неизвестным патогеном ещё <code>{fever_time} мин.</code>",
#             "no fever": "",
#         },

#         "errors" : {
#             "wait" : "🚬 Жди новых идей для заманух!",
#             "10" : "🔫 За раз только 10 попыток, брад!",
#             "404" : "🔫 404! Нацелился не на того!",
#             "again" : "🔫 Повторно вербовать можно только через",
#             "bot" : "🤖 Забудь про бота, они не поддаются вербовке!",
#             "victim" : "🔫 Цель не найдена, браток свинтил!"
#         }
#     },

    "pornohub" : {
        "theme_name" : "🔞 Сексуальная индустрия",
        "theme_desc" : "Тема сексуального характера",
        "type" : "arcade",
        "price" : 5000,

        "minilab": {
            "lab": """
🤵🏿‍♂ Порноактер: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🍆 Презервативы: {pats} из {all_pats}
🏆 Рейтинг в Порнхабе: {bio_exp}
🧬 Гармоны счастья: {bio_res}{fever}""",    

            "no lab name": "им. {name}",
            "corp": '\n🏛 Порностудия «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До нового полового акта: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До нового полового акта: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 У вас импотенция из за нарушения эрекции «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n🥴У вас импотенция из за нарушения эрекции ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """🪪 Информация о пенисе: <code>{patogen_name}</code>

🤵🏿‍♂ Порноактер: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🍆 Презервативы: {pats} из {all_pats} (<code>+{pats_calk}</code>)
👨🏻‍🔬 Сексуальная зависимость: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>🔬 НАВЫКИ УДОВЛЕТВОРЕНИЯ:</b>
🔞 Черный хуй: {infect} ур. (<code>+{infect_calk}</code>)
🛡 Вагина: {immunity} ур. (<code>+{immunity_calk}</code>)
🌚 Возбуждение: {mortality} ур. (<code>+{mortality_calk}</code>
🩸 Фемидом: {security} ур. (<code>+{security_calk}</code>)

<b>⛩ ДАННЫЕ ПОЛОВЫХ АКТОВ:</b>
🏆 Рейтинг в Порнхабе: {bio_exp}
🧬 Гармоны счастья: {bio_res}
🥳 Оргазмов: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🌭 Изнасиловали: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

        "no pathogen name": "неизвестно",
        "no lab name": "им. {name}",
        "qualification calk": "{qual_time} мин. | +{qual_calk}",
        "qualification calk 60": "{qual_time} мин.",
        "corp": '\n🏛 Порностудия «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
        "no corp": "",
        "next patogen sec": "\n⏱ До нового полового акта: <code>{next_patogen_time}</code> сек.",
        "next patogen min": "\n⏱ До нового полового акта: <code>{next_patogen_time}</code> мин.",
        "full patogens": "",
        "fever patogen": "\n\n🥴 У вас импотенция из за нарушения эрекции «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
        "fever": "\n\n🥴У вас импотенция из за нарушения эрекции ещё <code>{fever_time} мин.</code>",
        "no fever": "",
    },

    "errors" : {
        "wait" : "🔞 Жди новых презервативов!",
        "10" : "🔞 Хуй болеть не будет?",
        "404" : "🔞 Шлюха не найдена!",
        "again" : "🔞 Ты сможешь трахнуть его повторно через",
        "bot" : "🔞 Нельзя трахать животных!",
        "victim" : "🔞 Шлюха не найдена!"
    }
 },

 "scammer" : {
        "theme_name" : "🤵🏻 Аферисты в сетях",
        "theme_desc" : "Тема для тех кто хочет получать ресурсы с помощью своей хитрости",
        "type" : "arcade",
        "price" : 5000,

        "minilab": {
            "lab": """
👤 Вы представляетесь: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

📱 Ложных номеров: {pats} из {all_pats}
💵  Долларов: {bio_exp}
💎 Общих запасов: {bio_res}{fever}""",    

            "no lab name": "им. {name}",
            "corp": '\n🏦 Сеть аферистов «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🖥 Вы слишком доверяли посторонним и были заскамлены «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n❓Вы повелись на фейковые данные ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab" : {
            "lab": """👥 Информация об организации: <code>{patogen_name}</code>

👤 Вы представляетесь: <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

📱 Ложных номеров: {pats} из {all_pats} (<code>+{pats_calk}</code>)
📞 Время подготовки шантажа: {qual} (<code>{qualification_calk}</code>){new_patogen}

<b>📊 ВАШИ НАВЫКИ:</b>
🗣 Убедительность: {infect} ур. (<code>+{infect_calk}</code>)
👀 Проинформированность : {immunity} ур. (<code>+{immunity_calk}</code>)
💰 Запасливость: {mortality} ур. (<code>+{mortality_calk}</code>)
🕵‍♂ Информация о других организациях: {security} ур. (<code>+{security_calk}</code>)

<b>🤫 СЕКРЕТНЫЕ ДАННЫЕ:</b>
💵  Долларов: {bio_exp}
💎 Общих запасов: {bio_res}
🪙 Получено ресурсов с игроков: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
👨‍✈️ Разоблачено мошенников: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",

            "no pathogen name": "фейковые данные",
            "no lab name": "им. {name}",
            "qualification calk": "{qual_time} мин. | +{qual_calk}",
            "qualification calk 60": "{qual_time} мин.",
            "corp": '\n🏦 Сеть аферистов «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🖥 Вы слишком доверяли посторонним и были заскамлены «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n❓Вы повелись на фейковые данные ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "errors" : {
            "wait" : "👺 Жди готовности шантажа",
            "10" : "👺 Можно попытаться обмануть только 10 раз!",
            "404" : "👺 Личность не найдена!",
            "again" : "👺 Ты сможешь получить доллары с доверчивых клиентов повторно через",
            "bot" : "👺 Искусственный интеллект не ведётся на уловки!",
            "victim" : "👺 Возможно данная личность скрывается от вас!"
        }
    },

    "english" : {
        "theme_name" : (
            "🇬🇧 Английская тема"
        ),
        "theme_desc" : (
            "Дефолтная тема для англоязычных (нет)"
        ),
        "type" : "language",
        "price" : 100,

        "minilab": {
            "lab": """
✨ <b>Owner:</b> <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Pathogens: {pats} из {all_pats}
☣️ Bio-exp: {bio_exp}
🧬 Bio-resource: {bio_res}{fever}""",    

            "no lab name": "им. {name}",
            "corp": '\n🏦 Сеть аферистов «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> сек.",
            "next patogen min": "\n⏱ До готовности шантажа: <code>{next_patogen_time}</code> мин.",
            "full patogens": "",
            "fever patogen": "\n\n🖥 Вы слишком доверяли посторонним и были заскамлены «<code>{fever_name}</code>» ещё <code>{fever_time} мин.</code>",
            "fever": "\n\n❓Вы повелись на фейковые данные ещё <code>{fever_time} мин.</code>",
            "no fever": "",
        },

        "biolab": {
            "lab": """🦠 Virus information: <code>{patogen_name}</code>

✨ <b>Owner:</b> <a href="tg://openmessage?user_id={user_id}">{lab_name}</a>{corp}

🧪 Pathogens: {pats} of {all_pats} (<code>+{pats_calk}</code>)
👨🏻‍🔬 Qualification: {qual} (<code>{qualification_calk}</code>){new_patogen}

🔬 <b>SKILLS:</b>
🦠 Infectiousness: {infect} lvl (<code>+{infect_calk}</code>)
🛡 Immunity: {immunity} lvl (<code>+{immunity_calk}</code>)
☠️ Lethality: {mortality} lvl (<code>+{mortality_calk}</code>)
🕵️‍♂️ Security Service: {security} lvl (<code>+{security_calk}</code>)

⛩ <b>DATA</b>:
☣️ Bio-exp: {bio_exp}
🧬 Bio-resource: {bio_res}
😷 Special Operations: {suc_operations}/{all_operations} (<code>{operations_percent}%</code>)
🥽 Prevented: {prevented_issue}/{all_issue} (<code>{issues_percent}%</code>){fever}""",
            "no pathogen name": "unknown",
            "no lab name": "of {name}",
            "qualification calk": "{qual_time} min. | +{qual_calk}",
            "qualification calk 60": "{qual_time} min.",
            "corp": '\n🏛 Corporation «<a href="tg://openmessage?user_id={corp_owner_id}">{corp_name}</a>»',
            "no corp": "",
            "next patogen sec": "\n⏱ Before a new pathogen: <code>{next_patogen_time}</code> sec.",
            "next patogen min": "\n⏱ Before a new pathogen: <code>{next_patogen_time}</code> min.",
            "full patogens": "",
            "fever patogen": "\n\n🥴 You have fever caused by pathogen «<code>{fever_name}</code>», <code>{fever_time} more min.</code>",
            "fever": "\n\n🥴 You have fever caused by an unknown pathogen, <code>{fever_time} more min.</code>",
            "no fever": ""
        },
        "errors" : {
            "wait" : "⏱ Wait for new pathogens!",
            "10" : "🧪 Maximum of 10 pathogens at a time!",
            "404" : "🧟‍♀️ User not found!",
            "again" : "🕐 You can re-infect him in",
            "bot" : "🙄 You can't infect a bot!",
            "victim" : "👺 Victim not found!"
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
            howfuck = "хыяром"
        elif lab.theme == "mafia":
            howfuck = "приемом"
        elif lab.theme == "hell":
            howfuck = "розыгрышем"
        elif lab.theme == "english":
            howfuck = "with the pathogen"
        elif lab.theme == "cookies":
            howfuck = "десертом"
        elif lab.theme == "zombie":
            howfuck = "мутагеном"
        elif lab.theme == "school":
            howfuck = "двойкой"
        elif lab.theme == "dream":
            howfuck = "таблеткой"
        elif lab.theme == "scammer":
            howfuck = "приёмом"
        elif lab.theme == "pornohub":
            howfuck = "твердым хуем"


        else:
            howfuck = "патогеном"

    else:
        if theme == "azeri":
            howfuck = "хыяром"
        elif theme == "mafia":
            howfuck = "приемом"
        elif theme == "hell":
            howfuck = "розыгрышем"
        elif theme == "english":
            howfuck = "with the pathogen"
        elif theme == "cookies":
            howfuck = "десертом"
        elif theme == "zombie":
            howfuck = "мутагеном"
        elif theme == "school":
            howfuck = "двойкой"
        elif theme == "dream":
            howfuck = "таблеткой"
        elif theme == "scammer":
            howfuck = "приёмом"
        elif theme == "pornohub":
            howfuck = "твердым хуем"

        else:
            howfuck = "патогеном"

    if lab.theme != "english" or theme != "english":
        return f"{howfuck} «<code>{lab.patogen_name}</code>»" if lab.patogen_name is not None else f"неизвестным {howfuck}"
    else:
        return f"{howfuck} «<code>{lab.patogen_name}</code>»" if lab.patogen_name is not None else f"unknown {howfuck}"


def sbService(suc, hidden, equal, theme, first_id, first_name, second_id, second_name, atts, patogen_name="", profit=0):

    hide_victim_link = f'<a href="tg://user?id={second_id}">\xad</a>'
    hide_attacker_link = f'<a href="tg://user?id={first_id}">\xad</a>'
    if suc == 1:

        attempt = "попыток"

        if theme == "azeri":
            organizer = "Пейсяр"
            full_attempt = "👨🏻‍🔬 Сын пейсяр чыхдын"
            short_attempt = "👨🏻‍🔬 Сяни сикди"
            lost = "🥒 Хыярлар сычды"
            you_lost = "☣️ мантлары сычды"
            bio = "манат"
            attempt = "дяня"

            alternative = "👨🏻‍🔬 Сяни сиктиляр"
            alter_lost = "☣️ Сычды"
            alter_attempt = "сиктиляр"

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
            attempt = "спроб"

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

        elif theme == "english":
            organizer = "Organizer"
            full_attempt = "👨🏻‍🔬 Your infection operation has been performed"
            short_attempt = "👨🏻‍🔬 An infection operation was performed"
            lost = "🧪 Minimum completed"
            you_lost = "☣️ You lost"
            bio = "bio-exp"
            attempt = "attempts"

            alternative = "👨🏻‍🔬 You have been infected"
            alter_lost = "☣️ Lost"
            alter_attempt = "was infected"

        elif theme == "zombie":
            organizer = "Распостранитель инфекции"
            full_attempt = "🖲 Была проведена операция вашего инфицирования"
            short_attempt = "🖲 Была проведена операция инфицирования"
            lost = "🧫 Совершено минимум"
            you_lost = "🔬 Вы потеряли"
            bio = "инфекто-опыта"

            alternative = "🖲 Вас подвергли инфекции"
            alter_lost = "🔬 Потерял"
            alter_attempt = "был подвергнут инфицированию"

        elif theme == "cookies":
            organizer = "Шеф-повар"
            full_attempt = "🧑‍🍳 Вас угостили десертом"
            short_attempt = "🧑‍🍳 Угостили "
            lost = "🧁 Совершено минимум"
            you_lost = "🙏 Вы оставили"
            bio = "благодарности"


            alternative = "🧑‍🍳 Вас угостили десертом"
            alter_lost = "🙏 Оставил"
            alter_attempt = "был угощен десертом"

        elif theme == "dream":
            organizer = "Организатор"
            full_attempt = "🧑‍🔬 Была проведена операция подвергнуть вас сонливостью"
            short_attempt = "🧑‍🔬 Была проведена операция подвергнуть вас сонливостью"
            lost = "💊 Совершено минимум"
            you_lost = "🌌 Вы потеряли"
            bio = "сон"


            alternative = "🧑‍🔬 Вас подвергли сонливостью"
            alter_lost = "🌌 Потерял"
            alter_attempt = "был подвергнут сонливостью"

        elif theme == "scammer":
            organizer = "Аферист"
            full_attempt = "🤥 Была совершена попытка обмануть вас"
            short_attempt = "🤥 Совершена попытка обмануть"
            lost = "📱 Совершено минимум"
            you_lost = "💵 Вы потеряли"
            bio = "доллары"

            alternative = "🤥 Вы оказались очень доверчивы и вас обманули"
            alter_lost = "💵 Потерял"
            alter_attempt = "был обманут"

        elif theme == "pornohub":
            organizer = "Порноактер"
            full_attempt = "🔞 Вас выебали жестко в попочку"
            short_attempt = "🔞 Была проведена попытка отсоса"
            lost = "🍆 Проведено минимум"
            you_lost = "🔞 В вас всунули"
            bio = "см члена"


            alternative = "👨🏿‍🔬 Вас жестко выебали"
            alter_lost = "🔞 Потерял"
            alter_attempt = "был изнасилован"


        elif theme == "school":
            organizer = "Шестерка"
            full_attempt = "👀 Была проведена операция уменьшения вашей зарплаты"
            short_attempt = "👀 Была проведена операция уменьшения вашей зарплаты"
            lost = "💩 Совершено минимум"
            you_lost = "⚡️ Вы потеряли"
            bio = "зарплаты"


            alternative = "👨🏻‍🔬 Вас сдали директору!"
            alter_lost = "⚡️ Вы потеряли"
            alter_attempt = "Он был раскрыт директору"

        else:
            organizer = "Организатор"
            full_attempt = "👨🏻‍🔬 Была проведена операция вашего заражения"
            short_attempt = "👨🏻‍🔬 Была проведена операция заражения"
            lost = "🧪 Совершено минимум"
            you_lost = "☣️ Вы потеряли"
            bio = "био"

            alternative = "👨🏻‍🔬 Вас подвергли заражению"
            alter_lost = "☣️ Потерял"
            alter_attempt = "был подвергнут заражению"

        if hidden:
            if equal:
                sb_text = f'{full_attempt} {patogen_name}.\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n\n'\
                        f'{lost} {atts} {attempt}!\n'\
                        f'{you_lost} <code>{profit}</code> {bio}.'
            else:
                sb_text = f'{short_attempt} '\
                        f'<a href="tg://openmessage?user_id={second_id}">{second_name}</a> {patogen_name}.\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n\n'\
                        f'{lost} {atts} {attempt}!\n'\
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

        attempt = "попыток"

        if theme == "azeri":
            organizer = "Баклажан"
            full_attempt = "👺 Сяни вуранда озю пейсяр чыхды!"
            short_attempt = "👺 Сяни сикмяк"
            attempt = "дяня"

        elif theme == "hell":
            organizer = "Организатор розыгрыша"
            full_attempt = "👺 Вас пытались напугать, но вы и бровью не пошевелили!"
            short_attempt = "👺 Попытка напугать"

        elif theme == "ukraine":
            organizer = "Злочинець"
            full_attempt = "👺 Спроба вашого вбивства провалилася!"
            short_attempt = "👺 Спроба вбивства"
            attempt = "спроб"

        elif theme == "english":
            organizer = "Organizer"
            full_attempt = "👺 Your infection attempt failed!"
            short_attempt = "👺 Attempt to infect"
            attempt = "attempts"

        elif theme == "zombie":
            organizer = "Распостранитель инфекции"
            full_attempt = "🚜 Инфицирование провалилось!"
            short_attempt = "🚚 Попытка инфицировать"

        elif theme == "cookies":
            organizer = "Шеф-повар"
            full_attempt = "🧑‍🍳 Вас пытались угостить, но вы искушенный гурман и раскритиковали подачу!"
            short_attempt = "🧑‍🍳 Попытка угостить кулинарного критика"

        elif theme == "school":
            organizer = "Организатор"
            full_attempt = "🤯 Попытка вашего раскрытия провалилась!"
            short_attempt = "🤯 Попытка сдать"

        elif theme == "dream":
            organizer = "Организатор"
            full_attempt = "⛔️ Попытка подвергнуть вас сонливостью провалилась!"
            short_attempt = "⛔️ Попытка подвергнуть сонливостью"

        elif theme == "scammer":
            organizer = "Аферист"
            full_attempt = "🤓 Вы обладаете достаточной информацией и не были обмануты!"
            short_attempt = "🤓 Попытка обмануть"

        elif theme == "pornohub":
            organizer = "Порноактер"
            full_attempt = "🔞 Попытка лишения вашей девственности провалилась!"
            short_attempt = "🔞 Попытка выебать"

        else:
            organizer = "Организатор"
            full_attempt = "👺 Попытка вашего заражения провалилась!"
            short_attempt = "👺 Попытка заразить"

        if hidden:
            if equal:
                sb_text = f'{full_attempt}\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n'\
                        f'Совершено минимум <i>{atts}</i> {attempt}!'
            else:
                sb_text = f'{short_attempt} '\
                        f'<a href="tg://openmessage?user_id={second_id}">{second_name}</a> провалилась!\n\n'\
                        f'{organizer}: '\
                        f'<a href="tg://openmessage?user_id={first_id}">{first_name}</a>\n'\
                        f'Совершено минимум <i>{atts}</i> {attempt}!'\
                        f'{hide_victim_link}'
        else:
            if equal:
                sb_text = f'{full_attempt}\n\n'\
                    f'Совершено минимум <i>{atts}</i> {attempt}!'
            else:
                sb_text = f'{short_attempt} '\
                    f'<a href="tg://user?id={second_id}">{second_name}</a> провалилась!\n\n'\
                    f'Совершено минимум <i>{atts}</i> {attempt}!'

    return sb_text


def attackText(theme, new, first_name, second_name, first_id, second_id, patogen_name, atts, profit, mortality):
    rslt_text = f""

    if theme == "azeri":
        ''' Азербайджанская тема '''
        fucked = "сикди"
        spend = "🥒 хыярлар гетди"
        gain = "☣️ Бу баклажан верир"
        bio_res = "био-манатлар"
        infect = "☠️ Заражение на"
        lol = "👨‍🔬 Бу баклажан сенин деильди!!! Амма инди сяниндир)"

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

    elif theme == "english":
        ''' Английская тема '''
        fucked = "infected"
        spend = "🧪 Pathogens Spent"
        gain = "☣️ The sacrifice brings"
        bio_res = "bio-resources"
        infect = "☠️ Infection for"
        lol = "👨‍🔬 The object has not yet been infected with your pathogen"

    elif theme == "zombie":
        ''' Зомби тема '''
        fucked = "подверг инфицированию"
        spend = "🧫 Затрачено мутагенов"
        gain = "🔬 Жертва приносит"
        bio_res = "инфекто-ресурса"
        infect = "☠️ Инфицирование на"
        lol = "🧟‍♀ Объект ещё не подвергался инфицированию вашим мутагеном"

    elif theme == "cookies":
        fucked = "угостил(а)"
        spend = "🧁 Использовано вкусняшек"
        gain = "🙏 Получено"
        bio_res = "благодарности"
        infect = "🍭 Десерт запомнится на"
        lol = "😋 Посетитель впервые пробует ваш рецепт и в восторге от блюда"

    elif theme == "school":
        fucked = "поставил на место"
        spend = "😔 Затрачено попыток"
        gain = "💘 Жертва принесет вам"
        bio_res = "зарплаты"
        infect = "☠️ Двойка на"
        lol = "😎 Вы еще не ставили этому человеку двойку!"

    elif theme == "dream":
        fucked = "подверг сонливостью"
        spend = "💊 Затрачено таблеток"
        gain = "🌌 Человек приносит"
        bio_res = "сон-ресурса"
        infect = "⏱ Сонливость на"
        lol = "🧑‍🔬 Человек ещё не подвергался сонливостью вашей таблеткой"

    elif theme == "scammer":
        fucked = "обманул"
        spend = "📱 Затрачено ложных номеров"
        gain = "💵 Жертва приносит"
        bio_res = "долларов"
        infect = "🪙 Ресурсы получены на"
        lol = "🥸 Вы ещё не получали долларов с данного игрока, колличество ваших запасов увеличено"

    elif theme == "pornohub":
        fucked = "сладко выебал"
        spend = "🍆 Затрачено презервативов"
        gain = "🥰 Жертва кончила"
        bio_res = "раз"
        infect = "🥶 Будет дрожать в конвульсиях"
        lol = "🔞 Вы ранее не проникали во влагалище данного человека"


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
                f"{infect} <i>{mortality} {skloneniye(mortality, theme)}</i>"

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
    "azeri" : "Хыяры салмаг?",
    "hell" : "Напугать в ответ",
    "ukraine" : "Йобнути у відповідь ",
    "english": "Infect back",
    "zombie" : "Инфицировать в ответ",
    "cookies" : "Угостить в ответ",
    "school" : "Поставить двойку в ответ!",
    "dream" : "Усыпить в ответ",
    "scammer" : "Обмануть в ответ",
    "pornohub" : "Попросить минет",
    "mafia" : "Завербовать в ответ"


}