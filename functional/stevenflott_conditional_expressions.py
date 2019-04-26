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

#%% [markdown]
# # Exploiting non-strict dictionary rules

# A dictionary's keys have no order. If we try to create a dictionary with multiple items that share a common key value, we'll only have one item in the resulting dict object. It's not clear which of the duplicated key values will be preserved, and it shouldn't matter.

# Here's a situation where we explicitly don't care which of the duplicated keys is preserved. We'll look at a degenerate case of the max() function, it simply picks the largest of two values:

def max(a, b):
    f = {a >= b: lambda: a,
         b >= a: lambda: b}[True]
    return f()

max(5, 6)

#%% [markdown]

# In the case where `a == b`, both items in the dictionary will have a key of the `True` condition. Only one of the two will actually be preserved. Since the answer is the same, it doesn't matter which is kept and which is treated as a duplicate and overwritten.


#%% [markdown]
# # Filtering true conditional expressions

# We have a number of ways of determining which expression is `True`. In the previous example, we loaded the keys into a dictionary. Because of the way the dictionary is loaded, only one value will be preserved with a key of `True`.

# Here's another variation to this theme, written using the filter() function:

#%%
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
# This is markdown body...


#%%
