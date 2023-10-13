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
        return result

    def escape_markdown(self, text):
        """функция для экранирования символов sql"""
        return re.sub(r"([`_'*\[\]])", r"\\\1", str(text))

    def delinkify(self, text):
        """ функция для удаления ссылок"""
        # return re.sub(r'^https?:\/\/.*[\r\n]*', '', str(text))
        return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str(text))
    
    def deEmojify(self, text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)
    def format_nums(self, num):
        num = ''.join(reversed(str(num)))
        result = ''
        count = 0
        for i in num:
            if count%3 == 0: result += ' '
            result += i
            count += 1
        return ''.join(reversed(str(result)))
    

keys = "А – Ꭿ ₳ Ǻ ǻ α ά Ǡ ẫ Ắ ắ Ằ ằ ẳ Ẵ ẵ Ä ª ä Å À Á Â å ã â à á Ã ᗩ @ Ⱥ Ǟ; Б – Ҕ ҕ Ϭ ϭ   ƃ ɓ; В – ℬ Ᏸ β ฿ ß ᗷ ᗽ ᗾ ᗿ Ɓ Ᏸ ᗸ ᗹ; Г – ୮ ┍ ℾ; Д – ℊ ∂; Е – ℰ ℯ ໂ Ē ℮ ē Ė ė Ę ě Ě ę Έ ê Ê È € É Ế Ề Ể Ễ é è عЄ є έ ε Ҿ ҿ; Ж – ♅ Җ җ Ӝ ӝ Ӂ ӂ; З – Յ ℨ ჳ; И – น ự Ӥ ӥ Ũ ũ Ū ū Ŭ ŭ Ù ú Ú ù Ҋ ҋ; К – ₭ Ꮶ Ќ k ќ ķ Ķ Ҝ ҝ ᶄ Ҡ ҡ; Л – ለ ሉ ሊ ሌ ል ሎ Ꮧ Ꮑ; М – ጠ ᛖ ℳ ʍ ᶆ Ḿ ḿ ᗰ ᙢ 爪 ₥; Н – ਮ ዘ ዙ ዚ ዛ ዜ ዝ ዞ ዟ ℍ ℋ ℎ ℌ ℏ ዙ Ꮵ Ĥ Ħ Ή Ḩ ӈ; О – ტ ó ό σ ǿ Ǿ Θ ò Ó Ò Ô ô Ö ö Õ õ ờ ớ ọ Ọ ợ Ợ ø Ø Ό Ở Ờ Ớ Ổ Ợ Ō ō Ő; П – Ո ກ ⋒ Ҧ ҧ; Р – թ ℙ ℘ ρ Ꭾ Ꮅ 尸 Ҏ ҏ ᶈ ₱ ☧ ᖘ ק ₽ Ƿ Ҏ ҏ; С – Ⴚ ☾ ℭ ℂ Ç ¢ ç Č ċ Ċ ĉ ς Ĉ ć Ć č Ḉ ḉ ⊂ Ꮸ ₡ ¢; Т – ⍑ ⍡ T t τ Ţ Ť Ŧ Ṫ ₮; У – ע ɣ Ꭹ Ꮍ Ẏ ẏ ϒ ɤ ￥ ௶ Ⴘ; Ф – Փ փ Ⴔ ቁ ቂ ቃ ቄ ቅ ቆ ቇ ቈ; Х -א χ × ✗ ✘ ᙭ ჯ Ẍ ẍ ᶍ; Ц – Ա ų; Ч – Կ կ ੫ Ⴁ Ӵ ӵ Ҹ ҹ; Ш – ש ᗯ ᙡ ω; Щ – պ ખ; Ъ – Ѣ ѣ ; Ы – Ӹ ӹ; Ь – Ѣ ѣ ; Э – ∋ ∌ ∍ ヨ Ӭ ӭ ℈; Ю – ਠ;"
keys += "A – Ꭿ 凡 Ꮨ ∀ ₳ Ǻ ǻ α ά Ά ẫ Ắ ắ Ằ ằ ẳ Ẵ ẵ Ä ª ä Å À Á Â å ã â à á Ã ᵰ B – ℬ Ᏸ β ฿ ß Ђ Ɓ ƀ ხ 方 ␢ Ꮄ C – ℭ ℂ Ç ¢ ç Č ċ Ċ ĉ ς Ĉ ć Ć č Ḉ ḉ ⊂ Ꮸ ₡ ¢ D – Ɗ Ď ď Đ đ ð ∂ ₫ ȡ E – ℯ £ Ē ℮ ē Ė ė Ę ě Ě ę Έ ê ξ Ê È € É ∑ Ế Ề Ể Ễ é è ع Є є έ ε F – ℱ ₣ ƒ ∮ Ḟ ḟ ჶ ᶂ φ╒ G – Ꮹ Ꮆ ℊ Ǥ ǥ Ĝ ĝ Ğ ğ Ġ ġ Ģ ģ פ ᶃ ₲ H – ℍ ℋ ℎ ℌ ℏ ዙ Ꮵ Ĥ Ħ ħ Ή 廾 Ћ ђ Ḩ Һ ḩ I – ℐ ℑ ί ι Ï Ί Î ì Ì í Í î ϊ ΐ Ĩ ĩ Ī ī Ĭ ĭ İ į Į Ꭵ J – ჟ Ĵ ĵ ᶖ ɉ K – ₭ Ꮶ Ќ k ќ ķ Ķ Ҝ ҝ ﻸ ᶄ L – ℒ ℓ Ŀ ŀ £ Ĺ ĺ Ļ ļ λ ₤ Ł ł ľ Ľ Ḽ ḽ ȴ Ꮭ ￡ Ꮑ M – ℳ ʍ ᶆ Ḿ ḿ 爪 ₥ N – ℕ η ñ ח Ñ ή ŋ Ŋ Ń ń Ņ ņ Ň ň ŉ ȵ ℵ ₦ O – ℴ ტ ٥ Ό ó ό σ ǿ Ǿ Θ ò Ó Ò Ô ô Ö ö Õ õ ờ ớ ọ Ọ ợ Ợ ø Ø Ό Ở Ờ Ớ Ổ ổ Ợ Ō ō P – ℙ ℘ þ Þ ρ Ꭾ Ꮅ 尸 Ҏ ҏ ᶈ ₱ ק ァ Q – ℚ q Q ᶐ Ǭ ǭ ჹ R – ℝ ℜ ℛ ℟ ჩ ř Ř ŗ Ŗ ŕ Ŕ ᶉ Ꮢ 尺 S – Ꮥ Ṧ ṧ ȿ ى § Ś ś š Š ş Ş ŝ Ŝ ₰ ∫ $ ֆ T – ₸ † T t τ ΐ Ţ ţ Ť ť ŧ Ŧ ィ 干 Ṫ ṫ ナ Ꮏ Ꮖ テ ₮ U – ∪ Ũ ⋒ Ủ Ừ Ử Ữ Ự ύ ϋ Ù ú Ú ΰ ù Û û Ü ử ữ ự Џ ü ừ Ũ ũ Ū ū Ŭ ŭ ų Ų ű Ű ů Ů V – ∨ √ Ꮙ Ṽ ṽ ᶌ \/ ℣ ʋ W – ₩ ẃ Ẃ ẁ Ẁ ẅ ώ ω ŵ Ŵ Ꮤ Ꮃ ฬ Ẅ ѡ Ꮚ Ꮗ ผ ฝ พ ฟ X – χ × ჯ Ẍ ẍ ᶍ Y – ɣ Ꭹ Ꮍ Ẏ ẏ ϒ ɤ ￥ り Z – ℤ ℨ ჳ 乙 Ẑ ẑ ɀ Ꮓ;"