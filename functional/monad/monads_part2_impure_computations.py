"""
Monads, part 2: impure computations

Stephan Boyer

https://www.stephanboyer.com/post/10/monads-part-2-impure-computations

"""

# raw_input = input  # Remove conflict with between Python 3 funciton and variables called `input` 


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

# Original implementation
# input = Computation(Computation.INPUT, [])

# New implementation as a funciton accepting a prompt
def _input(prompt='input: '):
    return Computation(Computation.INPUT, [prompt])

def output(text):
    return Computation(Computation.OUTPUT, [text])


def execute(computation):
    if computation.type == Computation.UNIT:
        return computation.data[0]
    elif computation.type == Computation.BIND:
        return execute(computation.data[1](execute(computation.data[0])))
    elif computation.type == Computation.INPUT:
        return input(computation.data[0])
    elif computation.type == Computation.OUTPUT:
        print(computation.data[0])
        return None

def test_output():

    main = output('Hello, World!')

    # What is main? Let’s find out:
    print(main)

    execute(main)
    "Hello, World!"

    assert main.__repr__() == """Computation(Computation.OUTPUT, ['Hello, World!'])"""


# NOTE: More advanced examples

def test_repeat_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "Repeat Input")

    main = bind(_input('repeat input: '), output)
    print(main)

    execute(main)
    "input: This will get printed back!"
    "This will get printed back!"

    assert True


def respond(input):
    if input == 'yes':
        return output('You said YES!')
    else:
        return output('You said NO!')

def test_respond_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "Respond Input")

    main = bind(_input('respond input: '), respond)
    print(main)

    execute(main)

    assert True


# Let’s modify the example so that it keeps asking the user for input until he/she says yes

def main_wrapper(dummy):
    return main

def respond(input):
    if input == 'yes':
        return output('You said YES!')
    else:
        return bind(output('Try saying \'yes\' once in a while.'), main_wrapper)

def test_repeat_respond_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "Repeat Respond Input")

    main = bind(_input('repeat respond input: '), respond)
    print(main)

    execute(main)

    assert True


# So now recursion doesn’t seem to be a problem either.
# Notice how we defined main_wrapper simply because bind expects a function of one argument.

# It turns out that this is a common monadic pattern, so let’s abstract it:

def sequence(u, v):
    return bind(u, lambda x: v)

def respond(input):
    if input == 'yes':
        return output('You said YES!')
    else:
        return sequence(output('Try saying \'yes\' once in a while.'), main)

def test_sequence_respond_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "Yes")

    main = bind(_input('sequence respond input: '), respond)
    print(main)

    execute(main)

    assert True


# To conclude, let’s write a program that asks the user for two lines of input,
# concatenates them, and prints the result:

def respond2(input1):
    return lambda input2: output('You said "' + input1 + '" and "' + input2 + '".')

def respond1(input1):
    return bind(_input('respond 2 input: '), respond2(input1))

def test_respond12_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "Yes")

    main = bind(_input('respond 1 input: '), respond1)
    print(main)

    execute(main)

    assert True
