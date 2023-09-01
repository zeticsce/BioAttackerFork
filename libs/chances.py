from random import *

percentOfFault = int()

def get_chance():
    
    chance = randint(1, 10)

    if chance > percentOfFault:
        return 1
    else:
        return 0
