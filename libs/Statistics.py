import json
from config import BOT_TOKEN, ECHO_CHAT
import requests
import shutil
import time
import datetime
import os
import sys

work_path = __file__.replace("\\", "/").split("/")
work_path.pop(-1)
work_path.pop(-1)
work_path = '/'.join(work_path)

class Statistics:
    def __init__(self) -> None:
        self.last_update = time.time()
        if not os.path.isfile(work_path + f'/chats/statistics.json'):
            stat = {
                "themes": [],
                "transactions": [],
                "users": {}
            }
            with open(work_path + f'/chats/statistics.json', 'w+', encoding="utf8") as f: json.dump(stat, f)

        try:
            with open(work_path + f'/chats/statistics.json', encoding='utf-8') as f: stat = json.load(f)
        except Exception as e:
            file_id = str(int(time.time()*1000))[::-1][:6]
            shutil.copyfile(work_path + f'/chats/statistics.json', work_path + f'/chats/invalidStatistics{file_id}.json')
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/', {
                'method': 'sendMessage', 
                'chat_id': ECHO_CHAT, 
                'text': f"*🪛 Ошибка чтения файла статистики*\n_(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_\n*Создан дамб файла* `chats/invalidStatistics{file_id}.json`",
                'parse_mode': "Markdown"
            })
            stat = {
                "themes": [],
                "transactions": [],
                "users": {}
            }
            with open(work_path + f'/chats/statistics.json', 'w+', encoding="utf8") as f: json.dump(stat, f)
        self.stat = stat
        self.users = stat["users"]
        self.themes: list = stat["themes"]
        self.transactions: list = stat['transactions']

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self.save()
    def save_transaction(self, sender_id: int, getter_id: int, coins: int): # транзакции только на коины!
        "tr_type это received (получил) или gave (отдал)"
        self.transactions.append({
            "sender_id": sender_id,
            "getter_id": getter_id,
            "coins": coins,
            "time": time.time()
        })
        self.save()
    def save(self):
        if self.last_update + 30 < time.time(): # сохранение в файл раз в тридцать секунд
            result = {
                "themes": self.themes,
                "transactions": self.transactions,
                "users": {}
            }
            with open(work_path + f'/chats/statistics.json', 'w', encoding="utf8") as f: json.dump(result, f)
            self.last_update = time.time()