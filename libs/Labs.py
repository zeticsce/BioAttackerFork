from app import query

class Labs:
    def __init__(self) -> None:
        self.has_lab_users = [i['user_id'] for i in query("SELECT * FROM `bio_attacker`.`labs`")]

    def create_lab(self, user_id):
        
        "INSERT INTO `bio_attacker_data`.`victums780882761` (`id`, `user_id`, `name`, `profit`, `from_infect`, `untill_infect`) VALUES (NULL, '567', 'ополо', '657', '6584', '56765')"

        "INSERT INTO `bio_attacker_data`.`issues780882761` (`id`, `user_id`, `pat_name`, `hidden`, `from_infect`, `until_infect`) VALUES (NULL, '7800121', NULL, '1', '6584', '75648')"
        

        query(f"INSERT INTO `bio_attacker`.`labs` (`id`, `user_id`, `corp`, `patogen_name`, `all_patogens`, `patogens`, `last_patogen_time`, `qualification`, `infectiousness`, `immunity`, `mortality`, `security`, `bio_exp`, `bio_res`, `all_operations`, `suc_operations`, `all_issue`, `prevented_issue`, `victims`, `disease`, `coins`, `bio_valuta`) VALUES (NULL, '{user_id}', NULL, NULL, '10', '10', '0', '1', '1', '1', '5', '1', '1', '100', '0', '0', '0', '0', '0', '0', '0', '0')")
        query(f"CREATE TABLE `bio_attacker_data`.`victums{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` VARCHAR(255) NULL , `name` VARCHAR(255) NULL , `profit` INT(11) NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")
        query(f"CREATE TABLE `bio_attacker_data`.`issues{user_id}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `user_id` BIGINT NOT NULL , `pat_name` VARCHAR(255) NULL , `hidden` BOOLEAN NULL , `from_infect` BIGINT NULL , `until_infect` BIGINT NULL , PRIMARY KEY (`id`), INDEX `user id` (`user_id`)) ENGINE = InnoDB;")

        result = query(f"SELECT * FROM `bio_attacker`.`labs` LEFT JOIN `telegram_data`.`tg_users` ON bio_attacker.labs.user_id = telegram_data.tg_users.user_id WHERE `bio_attacker`.`labs`.`user_id` = {user_id} LIMIT 1;")

        result[0].pop("patogen_names")
        result[0].pop("iris_name")
        result[0].pop("tg_users.id")
        result[0].pop("tg_users.user_id")
        return result[0]
    
    def get_lab(self, user_id):
        result = query(f"SELECT * FROM `bio_attacker`.`labs` LEFT JOIN `telegram_data`.`tg_users` ON bio_attacker.labs.user_id = telegram_data.tg_users.user_id WHERE `bio_attacker`.`labs`.`user_id` = {user_id} LIMIT 1;")
        if len(result) == 1: 
            result[0].pop("patogen_names")
            result[0].pop("iris_name")
            result[0].pop("tg_users.id")
            result[0].pop("tg_users.user_id")
            return result[0]
        else: return None