from typing import Any
from app import query
import json

    
class UserLab:
    def __init__(self, user_id):
        self.user_id = user_id
        self.__convert_lab()

    def __convert_lab(self):
        
        result = query(f"SELECT * FROM `bio_attacker`.`labs` LEFT JOIN `telegram_data`.`tg_users` ON bio_attacker.labs.user_id = telegram_data.tg_users.user_id WHERE `bio_attacker`.`labs`.`user_id` = {self.user_id} LIMIT 1;")
        if len(result) == 1: 
            result[0].pop("patogen_names")
            result[0].pop("iris_name")
            result[0].pop("tg_users.id")
            result[0].pop("tg_users.user_id")
            self.__dict__ = dict(result[0])
            self.__start_data = dict(result[0])
        else: return None

    def __getitem__(self, item):
        return self.__dict__[item]
    def __repr__(self):
        return str(json.dumps(self.__dict__, indent=4))
    
    def save(self):
        result = []
        for i in self.__start_data:
            if self.__start_data[i] != self.__dict__[i]: result.append(f"`{i}` = '{self.__dict__[i]}'") 
        if len(result) != 0: query(f"UPDATE `bio_attacker`.`labs` SET {', '.join(result)} WHERE `labs`.`user_id` = {self.user_id}")

