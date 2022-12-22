'''
-Write a function which takes any number of parameters and returns their average. 
'''
def get_avg(*args):
    sum = 0
    count = 0

    for i in args:
        sum += i
        count += 1
    return sum * 1.0 / count


x = get_avg(1, 2, 3, 4, 5, 6, 10)
print(x)