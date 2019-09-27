""" Python Algebraic Data Types (ADTs)

    Example from `sumtypes` documentaiton
    http://sumtypes.readthedocs.io/en/latest/
"""

# %%
import attr
from sumtypes import sumtype, constructor, match

# %%
""" Decorate your classes to make them a sum type: """

@sumtype
class MyType(object):
    # constructors specify names for their arguments
    MyConstructor = constructor('x')
    AnotherConstructor = constructor('x', 'y')

    # You can also make use of any feature of the attrs
    # package by using attr.ib in constructors
    ThirdConstructor = constructor(
        # one=attr.ib(default=42),
        # ValueError: No mandatory attributes allowed after an attribute with a default value or factory
        two=attr.ib(validator=attr.validators.instance_of(int)),
        one=attr.ib(default=42))

""" Then construct them by calling the constructors: """
v = MyType.MyConstructor(1)
v2 = MyType.AnotherConstructor('foo', 2)

""" You can get the values from the tagged objects: """
assert v.x == 1
assert v2.x == 'foo'
assert v2.y == 2

""" You check the constructor used: """
assert type(v) is MyType.MyConstructor
assert type(v) is MyType.MyConstructor

""" And, like Scala case classes,
    the constructor type is a subclass of the main type: """
assert isinstance(v, MyType)

""" And the tagged objects support equality: """
assert v == MyType.MyConstructor(1)
assert v != MyType.MyConstructor(2)

""" Simple pattern matching is also supported.
    To write a function over all the cases of a sum type: """


@match(MyType)
class get_number(object):
    """ Get the number from `MyType` """
    def MyConstructor(x): return x
    def AnotherConstructor(x, y): return y
    def ThirdConstructor(one, two): return one + two

""" match() ensures that all cases are handled.
    If you really want to write a ‘partial function’
    (i.e. one that doesn’t cover all cases), use match_partial(). """
assert get_number(v) == 1
assert get_number(v2) == 2

print(get_number(v) == 1)
print(get_number(v2) == 2)

# %%
""" Decorate your classes to make them a sum type: """
# Another example...
@sumtype
class MyType(object):
    """ Name and Number """
    NamedNum = constructor('name', 'num')
    AnonymousNum = constructor('num')


@match(MyType)
class get_num(object):
    """ Pattern match on `MyType` """
    def NamedNum(_, num): return num
    def AnonymousNum(num): return num

assert get_num(MyType.NamedNum('foo', 1)) == 1
assert get_num(MyType.AnonymousNum(2)) == 2

print("NamedNum: {}".format(get_num(MyType.NamedNum('foo', 1))))
print("AnonymousNum: {}".format(get_num(MyType.AnonymousNum(2))))

print("Finished...")
