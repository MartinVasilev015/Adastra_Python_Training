'''
-Write a function to calculate Lucas numbers using recursion. 
    -Lucas numbers are very similar to Fibonacci numbers and are defined by L(0)=2, L(1)=1 and L(n)=L(n-1)+L(n-2) 
-Use a timing decorator to log how long each call. How long does it take to calculate L(35)? What about L(100)? 
-Now add a memoize decorator. Can you calculate L(100) now?
-Write a function which does prime factorization of a number, e.g. 20633239 = 11*29*71*911. 
    -Calculate the prime factorization of L(60) and L(61). 
'''
import collections
import functools
from functools import wraps
import time
import math
   
class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if not isinstance(args, collections.abc.Hashable):
           # uncacheable. a list, for instance.
           # better to not cache than blow up.
           return self.func(*args)
        if args in self.cache:
           return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def primefactors(n):
   while n % 2 == 0:
      print(2),
      n = n / 2

   for i in range(3, int(math.sqrt(n)) + 1, 2):
      while (n % i == 0):
         print(i)
         n = n / i
    
   if n > 2:
      print(n)


@memoized
@timeit
def lucas(n):
    if n == 0:
        return 2
    if n == 1:
        return 1
    return lucas(n-1) + lucas(n-2)

a = lucas(60)
print("Prime factors of " + str(a) + ":")
primefactors(a)

b = lucas(61)
print("Prime factors of " + str(b) + ":")
primefactors(b)
