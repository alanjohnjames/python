"""Steven F. Lott.

Chapter 13: Conditional Expressions and the Operator Module

http://xlb.es/Functional%20Python%20Programming%20-%20Steve%20Lott%20-%202015.pdf

"""

#%%
import functools

prod = lambda iterable: functools.reduce(lambda x, y: x*y, iterable, 1)

prod((1,2,3))


#%%
def fact(n):
    f= {n == 0: lambda n: 1,
        n == 1: lambda n: 1,
        n == 2: lambda n: 2,
        n > 2: lambda n: fact(n-1)*n }[True]
    return f(n)

fact(5)

#%%
def max(a, b):
    f = {a >= b: lambda: a,
         b >= a: lambda: b}[True]
    return f()

max(5, 6)

#%%
# # Filtering true conditional expressions
# We have a number of ways of determining which expression is True. In the previous example, we loaded the keys into a dictionary. Because of the way the dictionary is loaded, only one value will be preserved with a key of True.
# Here's another variation to this theme, written using the filter() function:
from operator import itemgetter

def semifact(n):
    alternatives= [(n == 0, lambda n: 1),
                   (n == 1, lambda n: 1),
                   (n == 2, lambda n: 2),
                   (n > 2, lambda n: semifact(n-2)*n)]
    _, f= next(filter(itemgetter(0), alternatives))
    return f(n)

semifact(10)

#%% [markdown]
# # Using the operator module instead of lambdas

