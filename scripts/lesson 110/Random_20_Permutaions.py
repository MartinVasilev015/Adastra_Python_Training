import sys
from functools import cache
import random

num = random.randint(15, 20)
count = 0
percent_chance = 99.9

@cache
def generate_permutations(a, n):

    global count

    if n == 0:
        if not count == num and random.uniform(0.0, 100.0) > percent_chance:
            print(''.join(a))
            count += 1
    else:
        for i in range(n):
            generate_permutations(a, n - 1)
            j = 0 if n % 2 == 0 else i
            b = list(a)
            b[j], b[n] = b[n], b[j]
        generate_permutations(tuple(b), n - 1)

if len(sys.argv) != 2:
    sys.stderr.write('Exactly one argument is required\n')
    sys.exit(1)

word = sys.argv[1]

generate_permutations(tuple(list(word)), len(word) - 1)