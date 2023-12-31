

# BioAttacker
[![Lines of code](https://hitsofcode.com/github/kawasaji/BioAttacker?branch=main)](https://hitsofcode.com/github/kawasaji/BioAttacker/view?branch=main) ![GitHub](https://img.shields.io/github/license/kawasaji/BioAttacker)
 ![GitHub contributors](https://img.shields.io/github/contributors/kawasaji/BioAttacker) <img alt="GitHub commit activity (branch)" src="https://img.shields.io/github/commit-activity/m/kawasaji/BioAttacker"> <a href="https://t.me/avocado_systems" target="blank"> <img alt="Static Badge" src="https://img.shields.io/badge/telegram-387D7A"> </a>

[![DeepSource](https://app.deepsource.com/gh/kawasaji/BioAttacker.svg/?label=active+issues&show_trend=false&token=j1x1arJZRozTgUJ-OX7PiREv)](https://app.deepsource.com/gh/kawasaji/BioAttacker/)
[![DeepSource](https://app.deepsource.com/gh/kawasaji/BioAttacker.svg/?label=resolved+issues&show_trend=false&token=j1x1arJZRozTgUJ-OX7PiREv)](https://app.deepsource.com/gh/kawasaji/BioAttacker/)

Бот-игра для телеграм работающий на `pymysql` и `aiogram`

## Оглавление

- [Установка](#Установка)
- [Запуск](#Запуск)
- [Команды](#Команды)

## Установка

Для начала скопируйте репозиторий на свой компьютер
```console
git clone https://github.com/kawasaji/BioAttacker
```
Далее перейдите в папку проекта `BioAttacker` и установите зависимости
```console
pip install -r requirements.txt
```

Теперь нужно создать файл в  `BioAttacker\config.py`
И ввести туда
``` python
BOT_TOKEN = "BOT_TOKEN"
OWNER_ID = 1234

MYSQL_USER = "MYSQL_USER"
MYSQL_PASSWORD = "MYSQL_PASSWORD"
MYSQL_HOST = "MYSQL_HOST"
```

## Запуск
Для запуска перейдите в папку проекта и напишите данную команду
```console
python -m app
```

## Команды

Для начала начнем с команды `биолаб`

Данная команда показывает всю вашу статистику, уровни, кол-во доступных патогенов

> <img alt="биолаб" src="https://github.com/kawasaji/BioAttacker/blob/main/photos/1.png?raw=true">
