"""
Monads, part 1: impure computations

Stephan Boyer

https://www.stephanboyer.com/post/9/monads-part-1-a-design-pattern

"""

# NOTE: Example 1: exception handling (a.k.a. “Maybe”)

def divide100(divisor):
    if divisor == 0:
        return None
    else:
        return 100 / divisor

def sqrt(x):
    if x < 0:
        return None
    else:
        return x ** 0.5


# What if we wanted to compute something like...
# sqrt(divide100(sqrt(x))) 

x = 2
a = sqrt(x)
if a is not None:
    b = divide100(a)
    if b is not None:
        c = sqrt(b)

print(c)

# Imagine how tedious it would be if we had to do manual error checking
# like this for all of our function calls

# A better solution is to rewrite divide100 and sqrt
# such that they each do the error handling themselves. 

def composable_divide100(divisor):
    if divisor is None or divisor == 0:
        return None
    else:
        return 100 / divisor

def composable_sqrt(x):
    if x is None or x < 0:
        return None
    else:
        return x**0.5


# Now we can evaluate expressions
x = 9
c = composable_sqrt(composable_divide100(composable_sqrt(x)))
print(c)

# When x <= 0, the entire expression evaluates to None just as we would expect
x = -9 
c = composable_sqrt(composable_divide100(composable_sqrt(x)))
print(c)


# Rather than modifying all of our functions to check for None,
# let’s write a wrapper function (let’s call it bind) to do the error handling for us

# It takes a value (either a number or None) and a function (such as divide100 or sqrt)
# and applies the function to that value.

def bind(x, f):
    if x is None:
        return None
    else:
        return f(x)

# Now we can compose ordinary functions

x = 2
c = bind(bind(bind(x, sqrt), divide100), sqrt)

print(c)

# We have a way to compose numerical functions that might fail.
# You’ve essentially just implemented Haskell’s Maybe monad

# NOTE: Example 2: vector operations (a.k.a. “List”)

# We know that, mathematically, positive numbers have two square roots.
# Let’s modify sqrt to return a list of values:

def sqrt(x):
    if x < 0:
        return []
    elif x == 0:
        return [0]
    else:
        return [x**0.5, -x**0.5]

# Our sqrt function now makes more mathematical sense, at least for real numbers.
# But we have the same problem as in Example 1—it is no longer composable with itself

# We can’t just compute sqrt(sqrt(x)),
# because the inner call to sqrt returns a list,
# and the outer call expects a number.

# As before, we need to define a bind function to help us with composition:

def bind(x, f): 
    return [j for i in x for j in f(i)]


# Here, bind takes a list of numbers x and a function f.

# The doubly-iterated list comprehension might look cryptic—you can think of it like this:
# We apply f to each value in x, which gives us a list of lists.
# Then we flatten the result into one list and return it.

r = bind(bind([5, 0, 3], sqrt), sqrt)
assert r == [1.4953487812212205, -1.4953487812212205, 0, 1.3160740129524924, -1.3160740129524924]
print(r)

# But our original goal was to find the square roots of one number.
# We could always write bind([x], sqrt) where x is a number,
# maybe it would be better to use a function to abstract the representation of our input.
# Let’s call this function unit

def unit(x):
    return [x]

# Now we don’t have to put our input into a list—instead, we run it through unit,
# which puts it in the necessary representation:

r = bind(bind(unit(4), sqrt), sqrt) 
assert r == [1.4142135623730951, -1.4142135623730951]
print(r)

# Now intelligently compose functions that might return several values

# NOTE: Example 3: debug output (a.k.a. “Writer”)

# Suppose we have some functions u and v, and each function takes a number and returns a number

def u(x): 
    return x + 4 

def v(x): 
    return x * 2

# suppose we want each function to also return a string indicating that the function had been called.
# We might modify u and v like this:

def verbose_u(x): 
    return (x + 4, '[verbose_u was called on ' + str(x) + ']') 

def verbose_v(x): 
    return (x * 2, '[verbose_v was called on ' + str(x) + ']')

# Now we have the same problem as before, we broke composability:
# verbose_u(verbose_v(x)) doesn’t work.
# By now, we know the solution to this problem is bind

def bind(x, f): 
    result, output = f(x[0]) 
    return (result, x[1] + output)

# Here, x is a tuple containing the result from another operation
# (such as verbose_u or verbose_v) and the output from that operation

# This means we can once again compose verbose_u and verbose_v, using bind:
r =  bind(bind((4, ''), verbose_v), verbose_u) 
assert r == (12, '[verbose_v was called on 4][verbose_u was called on 8]')
print(r)

# Awesome!
# Not only do we get a numerical result, but we also get a complete execution trace.
# Notice how we passed (4, ''), when all we cared about was the 4
# It would be better to write a unit function to construct this tuple for us

def unit(x):
    return (x, '')

r = bind(bind(unit(4), verbose_v), verbose_u)
assert r == (12, '[verbose_v was called on 4][verbose_u was called on 8]')
print(r)

# Still works! We’ve just implemented Haskell’s Writer monad!

# NOTE: The pattern



# NOTE: Monad axioms


# NOTE: But what about side effects?

