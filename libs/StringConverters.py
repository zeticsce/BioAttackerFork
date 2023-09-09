import re

class StringConv:
    def __init__(self):
        pass
    def num_to_str(self, num):
        """
            Конвертирует число в строку 
            1000 1к
            1300 1,3к
            100300 100,3к
            10000300 1 000,3к
        """
        if num >= 1000:
            count = 1
            result = ""
            for i in reversed(str(num)):
                if count % 3 == 0: result += i + " "
                else: result += i
                count += 1
            result = list(reversed(result))
            if result[-3] != "0": 
                result = result[0:-2]
                result[-2] = ","
            else: result = result[0:-3]
            return ''.join(result).strip() + "k"
        else: return str(num)
        
    def escape_sql(self, text):
        """функция для экранирования символов sql"""
        result = re.sub(r"([\'\`\\])", r"\\\1", str(text))
        print(result)
        return result
