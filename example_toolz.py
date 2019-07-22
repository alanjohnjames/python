""" Example Toolz

    From `toolz` pypi page
    https://pypi.python.org/pypi/toolz """

#%%
#
# Compose.
# 

from toolz import compose, frequencies, partial
from toolz.curried import map


def stem(word):
    """ Stem word to primitive form """
    return word.lower().rstrip(",.!:;'-\"").lstrip("'\"")

wordcount = compose(frequencies, map(stem), str.split)

sentence = "This cat jumped over this other cat!"
wordcount(sentence)
# {'this': 2, 'cat': 2, 'jumped': 1, 'over': 1, 'other': 1}

# %%
print("sentance: {}".format(sentence))
print("split: {}".format(str.split(sentence)))
print("stem: {}".format(stem(sentence)))
print("frequencies: {}".format(frequencies(sentence)))

#%%
#
# Curry.
# 

from toolz.functoolz import curry 

@curry
def add(x, y, echo=False):
    if echo:
        print(f"x = {x}")
        print(f"y = {y}")

    return x + y

plus1 = add(x=1, echo=True)

plus1(y=2)

#%%

add1 = add(y=1)

add1(2, echo=True)

#%%
#
# Compose / Do.
# 

from toolz import compose
from toolz.curried import do
from dataclasses import dataclass, field

def inc(x):
    print(f"inc: x = {x}")
    return x+1

@dataclass
class Log:
    """Stateful class."""
    _log: list = field(default_factory=list)

    def append(self, obj):
        """Change state of class."""
        print(f"Log.append: obj = {obj}")
        self._log.append(obj)

log = Log()

inc = compose(inc, do(log.append))

inc(1)
inc(11)

print(f"log = {log}")


#%%
#
# Pipe.
# 

from toolz.curried import pipe, flip

double = lambda i: 2 * i
pipe(3, double, str)


#%%
def program(*funcs):
    return lambda data: pipe(data, *funcs)


double_then_str = program(double, str)   # TODO: How to do this with curried.pipe ?

#%%
double_then_str(3)


#%%
