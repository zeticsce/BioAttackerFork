import os

work_path = __file__.split("\\")
work_path.pop(-1)
work_path.pop(-1)
work_path = '\\'.join(work_path)

if not os.path.exists(work_path + '/chats'): os.mkdir(work_path + '/chats')

def save_message(message):
    if message.chat.type == "private": f = open(f"{work_path}/chats/user{message.chat.id}.txt", "a+", encoding="utf-8")
    else: f = open(f"{work_path}/chats/group{message.chat.id}.txt", "a+", encoding="utf-8")
    f.write(str(message) + '\n')
    f.close()

"""
    Штука парсит все сообщения юзеров и пишет их в индивидуальный файл по строкам

    На данный момент никаких действий с этим не проводится, далее возможно чтото сделать по типу веб интерфейса
    Я еще посмотрю сколько это будет занимать памяти на сервере, мб часть сообщений будет чиститься 
"""