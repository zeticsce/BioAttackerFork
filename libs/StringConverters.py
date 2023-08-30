class StringConv:
    def __init__(self):
        pass
    def num_to_str(self, num):
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
    
strconv = StringConv()

print(strconv.num_to_str(956))