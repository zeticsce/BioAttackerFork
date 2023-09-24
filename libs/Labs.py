from app import query, bot, OWNER_ID, BOT_TOKEN
import time
import random
import asyncio
import requests

class Labs:
    def __init__(self) -> None:
        self.has_lab_users = [i['user_id'] for i in query("SELECT * FROM `bio_attacker`.`labs`")]
        self.bio_top = query("SELECT * FROM bio_attacker.labs INNER JOIN telegram_data.tg_users ON bio_attacker.labs.user_id = telegram_data.tg_users.user_id ORDER BY bio_attacker.labs.bio_exp DESC LIMIT 25;")

    def create_lab(self, user_id):
        if len(query(f"SELECT * FROM `bio_attacker`.`labs` WHERE `user_id` = {user_id}")) == 0:        
            "INSERT INTO `bio_attacker_data`.`victums780882761` (`id`, `user_id`, `name`, `profit`, `from_infect`, `untill_infect`) VALUES (NULL, '567', 'ополо', '657', '6584', '56765')"
            "INSERT INTO `bio_attacker_data`.`issues780882761` (`id`, `user_id`, `pat_name`, `hidden`, `from_infect`, `until_infect`) VALUES (NULL, '7800121', NULL, '1', '6584', '75648')"


            query(f"INSERT INTO `bio_attacker`.`labs` (`id`, `user_id`, `corp`, `patogen_name`, `all_patogens`, `patogens`, `last_patogen_time`, `qualification`, `infectiousness`, `immunity`, `mortality`, `security`, `bio_exp`, `bio_res`, `all_operations`, `suc_operations`, `all_issue`, `prevented_issue`, `victims`, `disease`, `coins`, `bio_valuta`, `last_issue`, `last_farma`, `last_daily`, `virus_chat`) VALUES (NULL, '{user_id}', NULL, NULL, '10', '10', '0', '1', '1', '1', '5', '1', '1', '100', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '{int(time.time())}', '{user_id}')")
            query(f"CREATE TABLE `bio_attacker_data`.`victums{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` VARCHAR(255) NULL , `profit` INT(11) NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")
            query(f"CREATE TABLE `bio_attacker_data`.`issues{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` BIGINT NOT NULL , `pat_name` VARCHAR(255) NULL , `hidden` BOOLEAN NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")
            self.has_lab_users.append(user_id)
            user = self.get_user(user_id)
            labs_count = query("SELECT COUNT(*) as count FROM  `bio_attacker`.`labs`;")[0]['count']
            
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/', {
                'method': 'sendMessage', 
                'chat_id': OWNER_ID, 
                'text': f"🔬 Cоздана новая лаба {user['name']} / @{user_id}!\n🧮 Всего лаб {labs_count}"
            })
            
            from libs.UserLab import UserLab

        return UserLab(user_id)
    
    def get_lab(self, user_id): 
        from libs.UserLab import UserLab
        return UserLab(user_id)
    def get_user(self, tag):
        """
            Вернет юзера, если он существует, иначе будет None
        """
        if str(tag).isdigit(): 
            result = query(f"SELECT * FROM `telegram_data`.`tg_users` WHERE `user_id` = '{tag}'")
            result = None if len(result) == 0 else result[0] 
        else:
            result = query(f"SELECT * FROM `telegram_data`.`tg_users` WHERE `user_name` LIKE '{tag}'")
            result = None if len(result) == 0 else result[0]
        return result

    def save_victum(self, user_id, victum_id, profit):
        """
            user_id     юзер айди человека, который сделал заражение
            victum_id   юзер айди жертвы
            profit      профит, который получил юзер
        """
        victums = query(f"SELECT * FROM `bio_attacker_data`.`victums{user_id}` WHERE `user_id` = {victum_id} LIMIT 1")
        lab = self.get_lab(user_id)
        if len(victums) == 0:
            query(f"INSERT INTO `bio_attacker_data`.`victums{user_id}` (`id`, `user_id`, `profit`, `from_infect`, `until_infect`) VALUES (NULL, '{victum_id}', '{profit}', '{int(time.time())}', '{int(time.time()) + (lab.mortality * 24 * 60 * 60)}')")
        else:
            query(f"DELETE FROM `bio_attacker_data`.`victums{user_id}` WHERE `victums{user_id}`.`id` = {victums[0]['id']}")
            query(f"INSERT INTO `bio_attacker_data`.`victums{user_id}` (`id`, `user_id`, `profit`, `from_infect`, `until_infect`) VALUES (NULL, '{victum_id}', '{profit}', '{int(time.time())}', '{int(time.time()) + (lab.mortality * 24 * 60 * 60)}')")
    
    def get_victums(self, user_id, params = None):
        """
            user_id  юзер айди пользователя, у которого надо взять жертв
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None:
            return query(f"SELECT bio_attacker_data.victums{user_id}.id, bio_attacker_data.victums{user_id}.user_id, telegram_data.tg_users.user_name, telegram_data.tg_users.name, bio_attacker_data.victums{user_id}.profit, bio_attacker_data.victums{user_id}.from_infect, bio_attacker_data.victums{user_id}.until_infect  FROM `bio_attacker_data`.`victums{user_id}` INNER JOIN `telegram_data`.`tg_users` ON bio_attacker_data.victums{user_id}.user_id = telegram_data.tg_users.user_id;")
        else:
            return query(f"SELECT * FROM `bio_attacker_data`.`victums{user_id}` WHERE {params};")
        
    def get_issues(self, user_id, params = None):
        """
            user_id  юзер айди пользователя, у которого надо взять жертв
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None:
            return query(f"SELECT * FROM `bio_attacker_data`.`issues{user_id}`;")
        else:
            return query(f"SELECT * FROM `bio_attacker_data`.`issues{user_id}` WHERE {params};")
    def get_random_victum(self):
        count = query("SELECT MAX(`id`) as count FROM `telegram_data`.`tg_users`;")[0]['count']
        try: user = query(f"SELECT * FROM `telegram_data`.`tg_users` WHERE id = {random.randint(1, count)} LIMIT 1;")[0]
        except: user = query(f"SELECT * FROM `telegram_data`.`tg_users` WHERE id = {random.randint(1, count)} LIMIT 1;")[0]
        return user