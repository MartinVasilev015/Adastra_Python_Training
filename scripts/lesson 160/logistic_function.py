'''
-Map a lambda which applies the logistic function to the list [-3, -5, 1, 4] 
-Round each number to 4 decimal places 
'''
import math
nums = [-3, -5, 1, 4]
result = list(map(lambda x: round(x, 4), map(lambda x: 1.0 / (1.0 + (math.e**(-x))), nums)))
print(result)