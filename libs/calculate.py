from math import *


def pt(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 2.0)
        
        return count
    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"


def ql(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 2.6)
        
        return count
    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"


def zz(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 2.5)
        
        return count
    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"


def im(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 2.45)
        
        return count
    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"


def ll(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 1.95)
        
        return count

    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"


def bp(first, second):
    try:
        count = 0
        for i in range(int(second) - int(first)):
            count += floor((int(first) + i + 1) ** 2.1)
        
        return count
    except:
        return "Чувак, один из нас инвалид и я думаю что это ты :)"
        

print("calc funtions init")
