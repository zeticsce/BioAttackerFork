from typing import Any
from app import query
import json
import time
import math

    
class UserLab:
    """
        Класс создан для взаимодействия с лабой пользователя

        изменить значения в лабе пользователя можно при помощи 
        lab.<название параметра> += <необходимое значение>
        далее для того, чтобы закрепить значение в бд используем lab.save()
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.has_lab = False 
        self.__convert_lab()
        if self.has_lab and self.virus_chat == None: self.virus_chat = str(self.user_id)

    def format_dir(self, _item, indent=4, base_indent=None):

        if base_indent == None: 
            base_indent = indent
        result = "{\n"
        count = 0
        for i in _item:
            comma = "" if len(_item) - 1 == count else ","
            if type(_item[i]) == str: result += " "*indent + f'"{i}": "{_item[i]}"{comma}\n'
            elif type(_item[i]) == dict: result += " "*indent + f'"{i}": ' + self.format_dir(_item[i], indent=base_indent + indent, base_indent=base_indent) + comma
            else: result += " "*indent + f'"{i}": {_item[i]}{comma}\n'
            count += 1
        result += " "*(indent - base_indent) + "}\n"
        return result
    
    def __convert_lab(self):

        """
            Выбирает лабу из бд, чистит ее от лишнего
        """
        
        result = query(f"SELECT * FROM `bio_attacker`.`labs` LEFT JOIN `telegram_data`.`tg_users` ON bio_attacker.labs.user_id = telegram_data.tg_users.user_id WHERE `bio_attacker`.`labs`.`user_id` = {self.user_id} LIMIT 1;")
        if len(result) != 0: 
            result[0].pop("patogen_names")
            result[0].pop("iris_name")
            result[0].pop("tg_users.id")
            result[0].pop("tg_users.user_id")
            # print(result[0]['last_patogen_time'])
            self.__dict__ = dict(result[0])
            self.__start_data = dict(result[0])
            self.has_lab = True

            delta = int(time.time()) - self.last_patogen_time
            qual_time = ((61 - self.qualification)* 60)
            delta = delta / qual_time
            self.last_patogen_time = int(time.time()) - ((delta % 1) * qual_time)
            self.patogens += math.floor(delta)
            if self.patogens + math.floor(delta) <= self.all_patogens:
                self.patogens += math.floor(delta)
            else: 
                self.patogens = int(self.all_patogens)
                self.last_patogen_time = int(time.time())



    def __getitem__(self, item):
        return self.__dict__[item]
    def __repr__(self):
        data = dict(self.__dict__)
        data.pop("_UserLab__start_data")
        data.pop("has_lab")
        return self.format_dir(data)
    
    
    def get_victums(self, params = None):
        """
            Выводит список жертв у юзера
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None: 
            return query(f"SELECT bio_attacker_data.victums{self.user_id}.id, bio_attacker_data.victums{self.user_id}.user_id, telegram_data.tg_users.user_name, telegram_data.tg_users.name, bio_attacker_data.victums{self.user_id}.profit, bio_attacker_data.victums{self.user_id}.from_infect, bio_attacker_data.victums{self.user_id}.until_infect  FROM `bio_attacker_data`.`victums{self.user_id}` INNER JOIN `telegram_data`.`tg_users` ON bio_attacker_data.victums{self.user_id}.user_id = telegram_data.tg_users.user_id;")
        else: 
            return query(f"SELECT bio_attacker_data.victums{self.user_id}.id, bio_attacker_data.victums{self.user_id}.user_id, telegram_data.tg_users.user_name, telegram_data.tg_users.name, bio_attacker_data.victums{self.user_id}.profit, bio_attacker_data.victums{self.user_id}.from_infect, bio_attacker_data.victums{self.user_id}.until_infect  FROM `bio_attacker_data`.`victums{self.user_id}` INNER JOIN `telegram_data`.`tg_users` ON bio_attacker_data.victums{self.user_id}.user_id = telegram_data.tg_users.user_id {params};")
    
    def get_issues(self, params = None):
        """
            Выводит список болезней у юзера
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None: return query(f"SELECT * FROM `bio_attacker_data`.`issues{self.user_id}`;")
        else: return query(f"SELECT * FROM `bio_attacker_data`.`issues{self.user_id}` WHERE {params};")

        
    def save_victum(self, victum_id, profit):
        """
            Функция записывает жертву в базу и обновляет число заражений у юзера

            victum_id   юзер айди жертвы
            profit      профит, который получил юзер
        """
        victums = query(f"SELECT * FROM `bio_attacker_data`.`victums{self.user_id}` WHERE `user_id` = {victum_id} LIMIT 1")
        if len(victums) == 0:
            query(f"INSERT INTO `bio_attacker_data`.`victums{self.user_id}` (`id`, `user_id`, `profit`, `from_infect`, `until_infect`) VALUES (NULL, '{victum_id}', '{profit}', '{int(time.time())}', '{int(time.time()) + (self.mortality * 24 * 60 * 60)}')")
        else:
            query(f"DELETE FROM `bio_attacker_data`.`victums{self.user_id}` WHERE `victums{self.user_id}`.`id` = {victums[0]['id']}")
            query(f"INSERT INTO `bio_attacker_data`.`victums{self.user_id}` (`id`, `user_id`, `profit`, `from_infect`, `until_infect`) VALUES (NULL, '{victum_id}', '{profit}', '{int(time.time())}', '{int(time.time()) + (self.mortality * 24 * 60 * 60)}')")
        q = query(f"SELECT count(victums{self.user_id}.id) FROM `bio_attacker_data`.`victums{self.user_id}` WHERE `until_infect` >= {int(time.time())}")
        self.victums = q[0][list(q[0].keys())[0]]
        self.suc_operations += 1
        self.bio_exp += profit
        self.last_patogen_time = int(time.time())
    

    def save(self):
        """Сохраняет значение лабы, если никакие значения не были изменены, то ничего не делает"""
        result = []
        for i in self.__start_data:
            if self.__start_data[i] != self.__dict__[i]: result.append(f"`{i}` = '{self.__dict__[i]}'") 
        if len(result) != 0: query(f"UPDATE `bio_attacker`.`labs` SET {', '.join(result)} WHERE `labs`.`user_id` = {self.user_id}")

    

