"""
Monads, part 2: impure computations

Stephan Boyer

https://www.stephanboyer.com/post/10/monads-part-2-impure-computations

"""

# NOTE: The IO monad

class Computation:
    UNIT   = 0
    BIND   = 1
    INPUT  = 2
    OUTPUT = 3

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def __repr__(self):
        if self.type == Computation.UNIT:
            type_str = 'Computation.UNIT'
        elif self.type == Computation.BIND:
            type_str = 'Computation.BIND'
        elif self.type == Computation.INPUT:
            type_str = 'Computation.INPUT'
        elif self.type == Computation.OUTPUT:
            type_str = 'Computation.OUTPUT'
        return 'Computation(' + type_str + ', ' + self.data.__repr__() + ')'

def unit(x):
    return Computation(Computation.UNIT, [x])

def bind(x, f):
    return Computation(Computation.BIND, [x, f])


input = Computation(Computation.INPUT, [])

def output(text):
    return Computation(Computation.OUTPUT, [text])


def execute(computation):
    if computation.type == Computation.UNIT:
        return computation.data[0]
    elif computation.type == Computation.BIND:
        return execute(computation.data[1](execute(computation.data[0])))
    elif computation.type == Computation.INPUT:
        return input('input: ')
    elif computation.type == Computation.OUTPUT:
        print(computation.data[0])
        return None

main = output('Hello, World!')

# What is main? Let’s find out:

print(main)
assert main.__repr__() == """Computation(Computation.OUTPUT, ['Hello, World!'])"""

execute(main)
"Hello, World!"


# NOTE: More advanced examples

