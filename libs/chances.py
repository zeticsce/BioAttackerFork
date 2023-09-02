from random import *


def get_chance(params=0):
    
    chance = randint(1, 100)

    if params == 0:

        if chance > 80:
            return 1
            
        else:
            return 0

    elif params == 1:

        if chance > 75:
            return 1

        else:
            return 0

    else:
        pass


