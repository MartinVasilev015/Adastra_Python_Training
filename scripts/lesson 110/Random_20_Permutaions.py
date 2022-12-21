import sys
import random

results = []

def generate_permutaions(a, n):

    if n == 0:
        #print(''.join(a))
        results.append(''.join(a))
    else:
        for i in range(n):
            generate_permutaions(a, n - 1)
            j = 0 if n % 2 == 0 else i
            a[j], a[n] = a[n], a[j]
        generate_permutaions(a, n - 1)

if len(sys.argv) != 2:
    sys.stderr.write('Exactly one argument is required\n')
    sys.exit(1)

word = sys.argv[1]

generate_permutaions(list(word), len(word) - 1)

randoms = []
size = 20

for i in range(0, size):
    randoms.append(random.randint(0, len(results)))

for i in range(0, len(randoms)):
    print(results[randoms[i]])