""" Python Algebraic Data Types (ADTs)

    Example from `attr` documentation
    http://attrs.readthedocs.io/en/stable/overview.html#on-the-attr-s-and-attr-ib-names
"""

# %%
import attr

@attr.s
class SomeClass(object):
    a_number = attr.ib(default=42)
    list_of_numbers = attr.ib(default=attr.Factory(list))

    def hard_math(self, another_number):
        return self.a_number + sum(self.list_of_numbers) * another_number

sc = SomeClass(1, [1, 2, 3])
# sc

SomeClass(a_number=1, list_of_numbers=[1, 2, 3])
sc.hard_math(3)
# 19

sc == SomeClass(1, [1, 2, 3])
# True

sc != SomeClass(2, [3, 2, 1])
# True

attr.asdict(sc)
# {'a_number': 1, 'list_of_numbers': [1, 2, 3]}

SomeClass()
SomeClass(a_number=42, list_of_numbers=[])

C = attr.make_class("C", ["a", "b"])
C("foo", "bar")
# C(a='foo', b='bar')

print("Finished...")
