""" Example Toolz

    From `toolz` pypi page
    https://pypi.python.org/pypi/toolz """

# %%
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
