from typing import Any
from app import query
import json

    
class UserLab:
    """
        Класс создан для взаимодействия с лабой пользователя

        изменить значения в лабе пользователя можно при помощи 
        lab.<название параметра> += <необходимое значение>
        далее для того, чтобы закрепить значение в бд используем lab.save()
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.__convert_lab()

    def __convert_lab(self):

        """
            Выбирает лабу из бд, чистит ее от лишнего
        """
        
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
    
    
    def get_victums(self, params = None):
        """
            Выводит список жертв у юзера
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None: return query(f"SELECT * FROM `bio_attacker_data`.`victums{self.user_id}`;")
        else: return query(f"SELECT * FROM `bio_attacker_data`.`victums{self.user_id}` WHERE {params};")
    
    def get_issues(self, params = None):
        """
            Выводит список болезней у юзера
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None: return query(f"SELECT * FROM `bio_attacker_data`.`issues{self.user_id}`;")
        else: return query(f"SELECT * FROM `bio_attacker_data`.`issues{self.user_id}` WHERE {params};")
    

    def save(self):
        """Сохраняет значение лабы, если никакие значения не были изменены, то ничего не делает"""
        result = []
        for i in self.__start_data:
            if self.__start_data[i] != self.__dict__[i]: result.append(f"`{i}` = '{self.__dict__[i]}'") 
        if len(result) != 0: query(f"UPDATE `bio_attacker`.`labs` SET {', '.join(result)} WHERE `labs`.`user_id` = {self.user_id}")

    

