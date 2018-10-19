"""
Metaprogramming Beyond Decency: Part 1

http://hackflow.com/blog/2015/03/29/metaprogramming-beyond-decency/

"""


# Here we create a class that produces lambda upon addition 
# and then creates its instance named _.

class Whatever(object):
    def __add__(self, y):
        return lambda x: x + y

    def __mul__(self, y):
        return lambda x: x * y

    def __getattr__(self, y):
        return lambda x: x.y

_ = Whatever()


m = map(_ + 1, [1, 2, 3])

print(list(m))


from typing import NamedTuple

Guy = NamedTuple('Guy', [('name', str),
                         ('weight', float),
                         ('height', float)])

guys = [Guy('Alan', 88, 185), Guy('Allan', 75, 190)]

# Test guys
print(guys[0].height)

# list(map(_.height, [Guy('Al', 1, 2)]))

# Sort guys by height descending
# sorted(guys, key=-_.height)


from functools import reduce

# Reduce my multiplication
factorial = lambda n: reduce(_ * _, range(2, n+1))

# NOTE: TypeError: <lambda>() takes 1 positional argument but 2 were given
# print(factorial(5))

# from dataclasses import dataclasses

class Select:
    def __init__(self, choices):
        self.choices = choices

class TextInput:
    def __init__(self, coerce=None):
        self.coerce = coerce

class TextArea:
    def __init__(self, text=None):
        self.text = text

class Checkbox:
    def __init__(self, label):
        self.label = label
        self.checked = False

# Use simple pattern matching to construct form field widget
TYPE_TO_WIDGET = (
    [lambda f: isinstance(f, list), lambda f: Select(choices=f.choices)],
    [lambda f: isinstance(f, int),  lambda f: TextInput(coerce=int)],
    [lambda f: isinstance(f, str), lambda f: TextInput()],
    [lambda f: isinstance(f, str),  lambda f: TextArea()],
    [lambda f: isinstance(f, bool), lambda f: Checkbox(f.label)],
)

field = "Some text!"

first = next

match = first(do(field) for cond, do in TYPE_TO_WIDGET if cond(field))

assert isinstance(match, TextInput)

print(match)

# This actually could be useful for many things:
# recursive functions, chatbots, binary protocol implementations 
# and other occasions when you resolve to long if-elses or switch-cases.
# The general idea, however, comes beyond pattern matching.

