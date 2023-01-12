'''
-Write a function which takes any number of parameters and returns their average. 
'''

'''def get_avg_v1(*args):
    sum = 0
    count = 0

    for i in args:
        sum += i
        count += 1
    return sum * 1.0 / count'''

def get_avg_v2(*args):
    return sum(args) / len(args)  

x = get_avg_v2(1, 2, 3, 4, 5, 6, 10)
print(x)