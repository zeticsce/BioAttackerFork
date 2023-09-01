

# BioAttacker
[![Lines of code](https://hitsofcode.com/github/kawasaji/BioAttacker?branch=main)](https://hitsofcode.com/github/kawasaji/BioAttacker/view?branch=main) <img alt="GitHub commit activity (branch)" src="https://img.shields.io/github/commit-activity/m/kawasaji/BioAttacker"> <a href="https://www.behance.net/jimmykawasaji" target="blank"> <img alt="Static Badge" src="https://img.shields.io/badge/telegram-387D7A"> </a>

Бот-игра для телеграм работающий на `pymysql`

## Оглавление

- [Установка](#Установка)
- []()
- []()

## Установка

Для начала скопируйте репозиторий на свой компьютер
```bash
git commit https://github.com/kawasaji/BioAttacker
```
Далее перейдите в папку проекта `BioAttacker` и установите зависимости
```bash
pip install -r requirements.txt
```

Теперь нужно создать файл в  `BioAttacker\config.py`
И ввести туда
``` python
BOT_TOKEN = "BOT_TOKEN"
OWNER_ID = 1234

MYSQL_USER = "MYSQL_USER"
MYSQL_PASSWORD = "MYSQL_PASSWORD"
MYSQL_DB = "MYSQL_DB"
MYSQL_HOST = "MYSQL_HOST"
```
