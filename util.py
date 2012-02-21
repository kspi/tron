import random

RANDOM = random.SystemRandom()

def choose_randomly(probs_choices):
    r = RANDOM.random()
    for prob, choice in probs_choices:
        r -= prob
        if r <= 0:
            return choice
    return choice

def player_name(num):
    if num == 1:
        return 'Alice'
    elif num == 2:
        return 'Bob'
    else:
        return 'Player %d' % num

def list_rotated_left(a, amount=1):
    return a[amount:] + a[0:amount]
