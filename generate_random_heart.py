import time
import random
from random import randint

random.seed(time.time())

arr = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

res = ''

hearts = ['🤍', '🖤', '🤎', '💜', '💙', '💚', '💛', '🧡', '❤️']

for i in range(len(arr)):
    for j in range(len(arr[i])):
        res += hearts[0] if arr[i][j] == 0 else hearts[randint(1, 8)]
    res += '\n'

print(res)