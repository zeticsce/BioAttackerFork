import re
import unicodedata
['ߛ', 'ໍ', 'ᛊ', 'ᜤ', '୧', '’', 'ට', '࿌', 'ϯ', '^', 'চ', 'ʜ', '࿇', 'ᙓ', 'ғ', 'ᛈ', '↼', 'ᚿ', 'ஜ', '๛', 'ð', 'ᐯ', 'ꮁ', '૦', 'ᴅ', '×', 'ϫ', '⁄', '℔', 'ȶ', 'ย', 'ր', 'ⱦ', '‧', '⃝', 'ʀ', 'მ', '୨', '›', 'ɩ', 'પ', '\u2063', 'ᴧ', 'ታ', 'দ', '∞', '๓', 'ᑎ', 'შ', 'ᥴ', '˖', 'ሀ', 'ᐟ', 'ઉ', '‹', '⃞', 'এ', 'ᴘ', '≛', 'ᖇ', 'ރ', 'ƨ', 'ᚱ', 'ஐ', '๖', '༼', 'զ', ':', 'ኸ', 'ꮋ', 'ᖚ', 'ܫ', '\U000e006c', 'ศ', 'æ', '«', 'ı', '֍', 'џ', 'ᱬ', 'ᡕ', 'ɠ', 'ፚ', 'ᡃ', 'ᚾ', 'ᘜ', 'ɧ', '℩', '༒', 'ᠵ', '>', 'ᘻ', 'ˎ', '[', '᠊', '⊘', 'ꮿ', 'ᥲ', 'է', 'ឪ', 'ᝨ', 'ꭸ', '᥊', 'י', '⃟', '֎', 'ꭰ', '⃣', '࿈', 'ա', '¿', 'ᴇ', 'ᄅ', '\U000e0062', 'ɕ', 'ᛟ', 'ᏺ', 'ᕈ', '\u200f', '᥎', '୭', '็', 'ᙁ', '⌑', '°', '"', 'ᘉ', '᯾', 'ʒ', 'ಠ', '˗', 'ʑ', 'ս', '\u200d', 'ꭷ', '\U000e0067', 'ᚤ', 'ષ', 'ᥣ', 'ᕼ', 'ჯ', 'ʙ', '∘', 'ƥ', 'ภ', 'ভ', 'ᥙ', 'დ', 'ᴠ', 'ᗪ', '᠌', 'ຮ', 'ᱢ', 'ɦ', 'վ', 'ᝀ', '↳', 'ક', 'γ', 'ᴓ', 'ᱴ', 'ᴩ', 'ƴ', 'ꮮ', 'ꮟ', 'ʬ', '๑', 'ց', '༏', 'ნ', 'ɞ', '‡', 'ᅟ', 'ދ', 'ऊ', 'ც', '*', 'វ', '<', 'ҭ', 'ɮ', 'ᚣ', 'ו', 'һ', 'ȼ', 'ކ', 'ፑ', 'ᛨ', 'ခ', 'ᥕ', 'ᴨ', 'ƚ', '»', 'ᥒ', 'ᛜ', 'ᗅ', '\U000e0073', 'ο', 'ᙅ', 'ʾ', 'ጀ', 'ᕐ', 'ß', 'ད', '⁐', '\U000e007f', 'ᴢ', 'ো', 'ᥬ', ')', '„', '༽', 'ω', 'ˏ', 'ב', '(', 'ꮯ', '\u2060', 'ᘛ', 'ꮼ', 'ᗑ', 'ᡶ', 'ᕗ', 'ৡ', 'ᚳ', ';', 'ᯓ', 'ઞ', '⊹', '¡', '!', 'ʏ', 'ι', '}', '=', 'ᴦ', 'ᥱ', '҂', 'μ', '϶', 'ᢗ', 'ব', 'ꮛ', 'ᛕ', '᠕', 'ཞ', 'ᚷ', 'ᛚ', 'ᡁ', '⇝', 'ᜣ', 'ⴝ', 'ɑ', '?', 'ཌ', 'ে', '\u206a', 'ด', "'", '¦', 'ᙖ', 'ꮒ', 'ɡ', '༓', 'ᗢ', 'ᚢ', 'ժ', 'թ', '༺', 'ת', 'በ', 'ღ', '᥉', '⌐', 'ɱ', '∆', 'ዐ', 'і', 'ѕ', 'ᕲ', 'ᬊ', 'ɾ', '”', '\U000e0065', '≼', 'ʌ', 'ᤋ', 'ʟ', '{', '࿖', 'ᕒ', 'ɭ', 'ᛁ', 'သ', 'ઽ', 'қ', 'ᒪ', 'ҵ', 'ᛉ', 'ᯤ', '-', 'ᐷ', 'ᄆ', '๔', 'ӄ', '᥅', 'א', 'ᠻ', 'ᵯ', 'ϝ', 'ƿ', 'ϟ', 'ᤂ', 'ጓ', 'ᦔ', 'ᱦ', 'ə', 'ν', 'ᛠ', 'ӻ', 'ᴡ', 'ঔ', 'հ', '͏', '&', '࿔', 'ᴀ', 'ƅ', '҉', 'ζ', '©', 'ː', 'ᙧ', '•', 'ު', 'ᛙ', 'ო', '≽', '/', '৮', 'ӌ', 'ᛏ', 'အ', 'ƙ', 'ɢ', '᧘', 'ᛌ', 'ɴ', '༢', 'ჿ', '᥆', 'ң', 'ᴗ', '®', 'ઇ', '᧒', 'ᴛ', 'ո', 'ρ', 'ি', '࿐', 'ߋ', '༻', '¤', 'ಭ', 'ᗝ', 'ᕙ', 'ᖆ', 'ᴍ', 'ᐠ', '~', '‽', 'ᚹ', 'ᴜ', '#', 'α', 'ל', 'ค', '—', 'ҽ', 'ᥫ', 'ৣ', 'ਡ', 'ร', 'ᑌ', '᭡', '\u200b', 'બ', '%', 'ᴄ', 'ᗣ', 'ᙐ', 'ᴊ', '᧐', 'ᝪ', '࿕', 'ᝯ', 'υ', 'ꭲ', 'ึ', 'λ', '↑', 'ץ', '⇨', 'ᱚ', 'ᛓ', 'ᓍ', 'ˊ', '์', 'ᦋ', 'ɪ', 'မ', '\U000e006e', 'ˋ', 'ߣ', 'ʚ', ']', '໔', 'δ', 'ᜨ', 'ᴏ', 'ᖙ', 'օ', '↯', 'ꮲ', 'ꭼ', 'ɍ', 'য', 'ᛇ', 'ɖ', 'ϸ', 'ཏ', '_', '‸', 'ট', 'ן', '.', 'ฅ', 'ӿ', 'ক', 'ʅ', '૨', 'ᚥ', 'ѵ', 'ɇ', 'ᱞ', 'ʞ', '\xad', 'ռ', 'র', 'ᴋ', 'เ', 'ᄋ', '\\', 'ք', 'ᚨ', 'צ', 'χ', '⋆', 'շ', 'რ', '\u2064', ',', 'ᔦ', 'ᛄ', 'ꭺ', 'ψ', '\u200c', 'ᚺ', 'ᘿ', 'ᜥ', 'κ', 'ѫ', '⃤', 'ӎ', 'ƈ', 'ተ', '±', 'უ', 'ᏽ', 'ѧ', '⃠', 'ᤉ', 'ɏ', 'อ', 'ਘ', '⇣', '·', 'ᜠ', 'ᚶ', 'ზ', '༆', 'π', 'ᶅ', 'ᅠ', 'ϻ', '⁂', 'ƀ', 'ᚲ', 'ྮ', '૮', '឵', 'ѳ', 'ᚴ', 'ߊ', 'ཀ', 'ɸ', 'ᓰ', '๏', '‵', '|', '\u206c', '᠆', 'ু', 'ა', 'ɯ', '⇀', 'մ', 'ꮱ', '–', '҈', 'ე', 'ҟ', 'ᱛ', 'া', 'ᚦ', 'ᵾ', 'ვ', 'ይ', '\U000e0077', 'ᖻ', 'ᑭ', '`', '༄', 'ᛋ', '+', 'ᛞ', '៸', '‿', 'ɨ', '੮', 'ɐ']
class StringConv:
    def __init__(self):
        self.keys = {'А': ['Ꭿ', '₳', 'Ǻ', 'ǻ', 'α', 'ά', 'Ǡ', 'ẫ', 'Ắ', 'ắ', 'Ằ', 'ằ', 'ẳ', 'Ẵ', 'ẵ', 'Ä', 'ª', 'ä', 'Å', 'À', 'Á', 'Â', 'å', 'ã', 'â', 'à', 'á', 'Ã', 'ᗩ', '@', 'Ⱥ', 'Ǟ'], 'Б': ['Ҕ', 'ҕ', 'Ϭ', 'ϭ', '', '', 'ƃ', 'ɓ'], 'В': ['ℬ', 'Ᏸ', 'β', '฿', 'ß', 'ᗷ', 'ᗽ', 'ᗾ', 'ᗿ', 'Ɓ', 'Ᏸ', 'ᗸ', 'ᗹ'], 'Г': ['୮', '┍', 'ℾ'], 'Д': ['ℊ', '∂'], 'Е': ['ℰ', 'ℯ', 'ໂ', 'Ē', '℮', 'ē', 'Ė', 'ė', 'Ę', 'ě', 'Ě', 'ę', 'Έ', 'ê', 'Ê', 'È', '€', 'É', 'Ế', 'Ề', 'Ể', 'Ễ', 'é', 'è', 'عЄ', 'є', 'έ', 'ε', 'Ҿ', 'ҿ'], 'Ж': ['♅', 'Җ', 'җ', 'Ӝ', 'ӝ', 'Ӂ', 'ӂ'], 'З': ['Յ', 'ℨ', 'ჳ'], 'И': ['น', 'ự', 'Ӥ', 'ӥ', 'Ũ', 'ũ', 'Ū', 'ū', 'Ŭ', 'ŭ', 'Ù', 'ú', 'Ú', 'ù', 'Ҋ', 'ҋ'], 'К': ['₭', 'Ꮶ', 'Ќ', 'k', 'ќ', 'ķ', 'Ķ', 'Ҝ', 'ҝ', 'ᶄ', 'Ҡ', 'ҡ'], 'Л': ['ለ', 'ሉ', 'ሊ', 'ሌ', 'ል', 'ሎ', 'Ꮧ', 'Ꮑ'], 'М': ['ጠ', 'ᛖ', 'ℳ', 'ʍ', 'ᶆ', 'Ḿ', 'ḿ', 'ᗰ', 'ᙢ', '爪', '₥'], 'Н': ['ਮ', 'ዘ', 'ዙ', 'ዚ', 'ዛ', 'ዜ', 'ዝ', 'ዞ', 'ዟ', 'ℍ', 'ℋ', 'ℎ', 'ℌ', 'ℏ', 'ዙ', 'Ꮵ', 'Ĥ', 'Ħ', 'Ή', 'Ḩ', 'ӈ'], 'О': ['ტ', 'ó', 'ό', 'σ', 'ǿ', 'Ǿ', 'Θ', 'ò', 'Ó', 'Ò', 'Ô', 'ô', 'Ö', 'ö', 'Õ', 'õ', 'ờ', 'ớ', 'ọ', 'Ọ', 'ợ', 'Ợ', 'ø', 'Ø', 'Ό', 'Ở', 'Ờ', 'Ớ', 'Ổ', 'Ợ', 'Ō', 'ō', 'Ő'], 'П': ['Ո', 'ກ', '⋒', 'Ҧ', 'ҧ'], 'Р': ['թ', 'ℙ', '℘', 'ρ', 'Ꭾ', 'Ꮅ', '尸', 'Ҏ', 'ҏ', 'ᶈ', '₱', '☧', 'ᖘ', 'ק', '₽', 'Ƿ', 'Ҏ', 'ҏ'], 'С': ['Ⴚ', '☾', 'ℭ', 'ℂ', 'Ç', '¢', 'ç', 'Č', 'ċ', 'Ċ', 'ĉ', 'ς', 'Ĉ', 'ć', 'Ć', 'č', 'Ḉ', 'ḉ', '⊂', 'Ꮸ', '₡', '¢'], 'Т': ['⍑', '⍡', 'T', 't', 'τ', 'Ţ', 'Ť', 'Ŧ', 'Ṫ', '₮'], 'У': ['ע', 'ɣ', 'Ꭹ', 'Ꮍ', 'Ẏ', 'ẏ', 'ϒ', 'ɤ', '￥', '௶', 'Ⴘ'], 'Ф': ['Փ', 'փ', 'Ⴔ', 'ቁ', 'ቂ', 'ቃ', 'ቄ', 'ቅ', 'ቆ', 'ቇ', 'ቈ'], 'Ц': ['Ա', 'ų'], 'Ч': ['Կ', 'կ', '੫', 'Ⴁ', 'Ӵ', 'ӵ', 'Ҹ', 'ҹ'], 'Ш': ['ש', 'ᗯ', 'ᙡ', 'ω'], 'Щ': ['պ', 'ખ'], 'Ъ': ['Ѣ', 'ѣ'], 'Ы': ['Ӹ', 'ӹ'], 'Ь': ['Ѣ', 'ѣ'], 'Э': ['∋', '∌', '∍', 'ヨ', 'Ӭ', 'ӭ', '℈'], 'Ю': ['ਠ'], 'A': ['Ꭿ', '凡', 'Ꮨ', '∀', '₳', 'Ǻ', 'ǻ', 'α', 'ά', 'Ά', 'ẫ', 'Ắ', 'ắ', 'Ằ', 'ằ', 'ẳ', 'Ẵ', 'ẵ', 'Ä', 'ª', 'ä', 'Å', 'À', 'Á', 'Â', 'å', 'ã', 'â', 'à', 'á', 'Ã', 'ᵰ'], 'B': ['ℬ', 'Ᏸ', 'β', '฿', 'ß', 'Ђ', 'Ɓ', 'ƀ', 'ხ', '方', '␢', 'Ꮄ'], 'C': ['ℭ', 'ℂ', 'Ç', '¢', 'ç', 'Č', 'ċ', 'Ċ', 'ĉ', 'ς', 'Ĉ', 'ć', 'Ć', 'č', 'Ḉ', 'ḉ', '⊂', 'Ꮸ', '₡', '¢'], 'D': ['Ɗ', 'Ď', 'ď', 'Đ', 'đ', 'ð', '∂', '₫', 'ȡ'], 'E': ['ℯ', '£', 'Ē', '℮', 'ē', 'Ė', 'ė', 'Ę', 'ě', 'Ě', 'ę', 'Έ', 'ê', 'ξ', 'Ê', 'È', '€', 'É', '∑', 'Ế', 'Ề', 'Ể', 'Ễ', 'é', 'è', 'ع', 'Є', 'є', 'έ', 'ε'], 'F': ['ℱ', '₣', 'ƒ', '∮', 'Ḟ', 'ḟ', 'ჶ', 'ᶂ', 'φ╒'], 'G': ['Ꮹ', 'Ꮆ', 'ℊ', 'Ǥ', 'ǥ', 'Ĝ', 'ĝ', 'Ğ', 'ğ', 'Ġ', 'ġ', 'Ģ', 'ģ', 'פ', 'ᶃ', '₲'], 'H': ['ℍ', 'ℋ', 'ℎ', 'ℌ', 'ℏ', 'ዙ', 'Ꮵ', 'Ĥ', 'Ħ', 'ħ', 'Ή', '廾', 'Ћ', 'ђ', 'Ḩ', 'Һ', 'ḩ'], 'I': ['ℐ', 'ℑ', 'ί', 'ι', 'Ï', 'Ί', 'Î', 'ì', 'Ì', 'í', 'Í', 'î', 'ϊ', 'ΐ', 'Ĩ', 'ĩ', 'Ī', 'ī', 'Ĭ', 'ĭ', 'İ', 'į', 'Į', 'Ꭵ'], 'J': ['ჟ', 'Ĵ', 'ĵ', 'ᶖ', 'ɉ'], 'K': ['₭', 'Ꮶ', 'Ќ', 'k', 'ќ', 'ķ', 'Ķ', 'Ҝ', 'ҝ', 'ﻸ', 'ᶄ'], 'L': ['ℒ', 'ℓ', 'Ŀ', 'ŀ', '£', 'Ĺ', 'ĺ', 'Ļ', 'ļ', 'λ', '₤', 'Ł', 'ł', 'ľ', 'Ľ', 'Ḽ', 'ḽ', 'ȴ', 'Ꮭ', '￡', 'Ꮑ'], 'M': ['ℳ', 'ʍ', 'ᶆ', 'Ḿ', 'ḿ', '爪', '₥'], 'N': ['ℕ', 'η', 'ñ', 'ח', 'Ñ', 'ή', 'ŋ', 'Ŋ', 'Ń', 'ń', 'Ņ', 'ņ', 'Ň', 'ň', 'ŉ', 'ȵ', 'ℵ', '₦'], 'O': ['ℴ', 'ტ', '٥', 'Ό', 'ó', 'ό', 'σ', 'ǿ', 'Ǿ', 'Θ', 'ò', 'Ó', 'Ò', 'Ô', 'ô', 'Ö', 'ö', 'Õ', 'õ', 'ờ', 'ớ', 'ọ', 'Ọ', 'ợ', 'Ợ', 'ø', 'Ø', 'Ό', 'Ở', 'Ờ', 'Ớ', 'Ổ', 'ổ', 'Ợ', 'Ō', 'ō'], 'P': ['ℙ', '℘', 'þ', 'Þ', 'ρ', 'Ꭾ', 'Ꮅ', '尸', 'Ҏ', 'ҏ', 'ᶈ', '₱', 'ק', 'ァ'], 'Q': ['ℚ', 'q', 'Q', 'ᶐ', 'Ǭ', 'ǭ', 'ჹ'], 'R': ['ℝ', 'ℜ', 'ℛ', '℟', 'ჩ', 'ř', 'Ř', 'ŗ', 'Ŗ', 'ŕ', 'Ŕ', 'ᶉ', 'Ꮢ', '尺'], 'S': ['Ꮥ', 'Ṧ', 'ṧ', 'ȿ', 'ى', '§', 'Ś', 'ś', 'š', 'Š', 'ş', 'Ş', 'ŝ', 'Ŝ', '₰', '∫', '$', 'ֆ'], 'T': ['₸', '†', 'T', 't', 'τ', 'ΐ', 'Ţ', 'ţ', 'Ť', 'ť', 'ŧ', 'Ŧ', 'ィ', '干', 'Ṫ', 'ṫ', 'ナ', 'Ꮏ', 'Ꮖ', 'テ', '₮'], 'U': ['∪', 'Ũ', '⋒', 'Ủ', 'Ừ', 'Ử', 'Ữ', 'Ự', 'ύ', 'ϋ', 'Ù', 'ú', 'Ú', 'ΰ', 'ù', 'Û', 'û', 'Ü', 'ử', 'ữ', 'ự', 'Џ', 'ü', 'ừ', 'Ũ', 'ũ', 'Ū', 'ū', 'Ŭ', 'ŭ', 'ų', 'Ų', 'ű', 'Ű', 'ů', 'Ů'], 'V': ['∨', '√', 'Ꮙ', 'Ṽ', 'ṽ', 'ᶌ', '\\/', '℣', 'ʋ'], 'W': ['₩', 'ẃ', 'Ẃ', 'ẁ', 'Ẁ', 'ẅ', 'ώ', 'ω', 'ŵ', 'Ŵ', 'Ꮤ', 'Ꮃ', 'ฬ', 'Ẅ', 'ѡ', 'Ꮚ', 'Ꮗ', 'ผ', 'ฝ', 'พ', 'ฟ'], 'Z': ['ℤ', 'ℨ', 'ჳ', '乙', 'Ẑ', 'ẑ', 'ɀ', 'Ꮓ']}
        self.conversion_dict = {}
        for key in self.keys:
            for symv in self.keys[key]:
                self.conversion_dict[symv] = key
        "им. ᴠᴏᴅɪᴄʜᴋᴀ. (tg://openmessage?user_id=5291004538)"
        keys = {
            'Σ': 'С', 
            'σ': 'o', 
            'φ': 'ф', 
            'α': 'а',
            "ʂ": "s", 
            "ɬ": "i", 
            "ყ": "y", 
            "Ɩ": "l", 
            "ɛ": "e", 
            "ҳ": "x", 
            "Ꮎ": "O", 
            "૯": "E", 
            "ᑯ": "d",
            "🇦": "A",
            "🇧": "B",
            "🇨": "C",
            "🇩": "D",
            "🇪": "E",
            "🇫": "F",
            "🇬": "G",
            "🇭": "H",
            "🇮": "I",
            "🇯": "J",
            "🇰": "K",
            "🇱": "L",
            "🇳": "N",
            "🇴": "O",
            "🇵": "P",
            "🇶": "Q",
            "🇷": "R",
            "🇸": "S",
            "🇹": "T",
            "🇺": "Y",
            "🇻": "V",
            "🇼": "W",
            "🇽": "X",
            "🇾": "Y",
            "🇿": "Z",
            "🇲": "M",
            "Ᏼ": "B",
            "Ꮻ": "O",
            "Ꮇ": "M",
            "𑲭": "",
            # "ʀ": "R",
            # "ᴠ": "V",
            # "ᴏ": "O",
            # "ᴅ": "D",
            # "ɪ": "I",
            # "ᴄ": "C",
            # "ʜ": "H",
            # "ᴋ": "K",
            # "ᴀ": "A"
        }
        for key in keys:
            self.conversion_dict[key] = keys[key]


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
        return str(text).replace("*", "\*").replace("`", "\`").replace("(", "\(").replace(")", "\)").replace("_", "\_").replace("[", "\[").replace("]", "\]")

    def delinkify(self, text):
        """ функция для удаления ссылок"""
        # return re.sub(r'^https?:\/\/.*[\r\n]*', '', str(text))
        return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str(text))

    def deEmojify(self, text):
        regrex_pattern = re.compile(pattern = "["
                               u"\U0001F600-\U0001F64F"  # эмодзи в категории эмоций
                               u"\U0001F300-\U0001F5FF"  # эмодзи в категории символов
                               u"\U0001F680-\U0001F6FF"  # эмодзи в категории транспорта
                               u"\U0001F700-\U0001F77F"  # эмодзи в категории символов (дополнительные)
                               u"\U0001F780-\U0001F7FF"  # эмодзи в категории символов (дополнительные)
                               u"\U0001F800-\U0001F8FF"  # эмодзи в категории символов (дополнительные)
                               u"\U0001F900-\U0001F9FF"  # эмодзи в категории символов (дополнительные)
                               u"\U0001FA00-\U0001FA6F"  # эмодзи в категории символов (дополнительные)
                               u"\U0001FA70-\U0001FAFF"  # эмодзи в категории символов (дополнительные)"
                               u"\U0001F004-\U0001F0CF"  # эмодзи из дополнительной таблицы
                               u"\U0001F170-\U0001F251"  # эмодзи из дополнительной таблицы
                               u"\U0001F004-\U0001F251"  # эмодзи из дополнительной таблицы
                               u"\U000025AA-\U00002B06"  # графические символы и стрелки
                               u"\U0000231A-\U0001F251"
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
    def normalaze(self, text: str, for_html: bool=True, replace=None, with_emoji: bool=False):
        text = unicodedata.normalize('NFKD', text.replace("й", "*h234*")) # *h234* нужно для того, чтобы буква й пережила фильтрацию, иначе оно просто очищает его
        text = ''.join([char for char in text if not unicodedata.combining(char)]).replace("*h234*", "й")
        text = re.sub(r'[\u0600-\u06FF]+', '', text)
        text = unicodedata.normalize('NFC', text)
        text = ''.join([self.conversion_dict.get(char, char) for char in text])

        if for_html: text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if not with_emoji: text = self.deEmojify(text)
        if replace is not None and text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "") == "": text = replace
        # text = emoji.demojize(text)

        return text

    def format_dir(self, _item, indent=4, base_indent=None):

        if base_indent is None: 
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
    def skl(self, num):
        skls = {
            "1-20": ['один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать', 'двадцать'],
            "%10": ['десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто'],
            "%100": ['сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот'],
            "%1000": ['тысяча', 'две тысячи', 'три тысячи', 'четыре тысячи', 'пять тысяч', 'шесть тысяч']
        }
        result = ''
        if num < 20:
            result = skls['1-20'][num-1]
        elif num < 100:
            result += skls['%10'][int(str(num)[0])-1]
            if num%10 != 0:
                result += ' ' + skls['1-20'][int(str(num)[1])-1]
        elif num < 1000:
            result += skls['%100'][int(str(num)[0])-1]
            if num%100 != 0:
                result += ' ' + skls['%10'][int(str(num)[1])-1] if str(num)[1] != '0' else ''
                if num%10 != 0:
                    result += ' ' + skls['1-20'][int(str(num)[2])-1]
        elif num < 10000:
            result += skls['%1000'][int(str(num)[0])-1]
            if num%1000 != 0:
                result += ' ' + skls['%100'][int(str(num)[1])-1] if str(num)[1] != '0' else ''
                if num%100 != 0:
                    result += ' ' + skls['%10'][int(str(num)[2])-1] if str(num)[2] != '0' else ''
                    if num%10 != 0:
                        result += ' ' + skls['1-20'][int(str(num)[3])-1]

        return result