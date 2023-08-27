from app import query
from libs.UserLab import UserLab

class Labs:
    def __init__(self) -> None:
        self.has_lab_users = [i['user_id'] for i in query("SELECT * FROM `bio_attacker`.`labs`")]

    def create_lab(self, user_id):
        
        "INSERT INTO `bio_attacker_data`.`victums780882761` (`id`, `user_id`, `name`, `profit`, `from_infect`, `untill_infect`) VALUES (NULL, '567', 'ополо', '657', '6584', '56765')"

        "INSERT INTO `bio_attacker_data`.`issues780882761` (`id`, `user_id`, `pat_name`, `hidden`, `from_infect`, `until_infect`) VALUES (NULL, '7800121', NULL, '1', '6584', '75648')"
        

        query(f"INSERT INTO `bio_attacker`.`labs` (`id`, `user_id`, `corp`, `patogen_name`, `all_patogens`, `patogens`, `last_patogen_time`, `qualification`, `infectiousness`, `immunity`, `mortality`, `security`, `bio_exp`, `bio_res`, `all_operations`, `suc_operations`, `all_issue`, `prevented_issue`, `victims`, `disease`, `coins`, `bio_valuta`) VALUES (NULL, '{user_id}', NULL, NULL, '10', '10', '0', '1', '1', '1', '5', '1', '1', '100', '0', '0', '0', '0', '0', '0', '0', '0')")
        query(f"CREATE TABLE `bio_attacker_data`.`victums{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` VARCHAR(255) NULL , `name` VARCHAR(255) NULL , `profit` INT(11) NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")
        query(f"CREATE TABLE `bio_attacker_data`.`issues{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` BIGINT NOT NULL , `pat_name` VARCHAR(255) NULL , `hidden` BOOLEAN NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")
        
        return UserLab(user_id)
    
    def get_lab(self, user_id): return UserLab(user_id)

    def get_victums(self, user_id, params = None):
        """
            user_id  юзер айди пользователя, у которого надо взять жертв
            params   условия для поиска жертв, если они не установлены, выдаст все возможные жертвы, условия писать согласно синтаксису sql
        """
        if params == None:
            return query(f"SELECT * FROM `bio_attacker_data`.`victums{user_id}`;")
        else:
            return query(f"SELECT * FROM `bio_attacker_data`.`victums{user_id}` WHERE {params};")