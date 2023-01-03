import math
nums = [-3, -5, 1, 4]
result = list(map(lambda x: round(x, 2), map(lambda x: 1.0 / (1.0 + (math.e**(-x))), nums)))
print(result)