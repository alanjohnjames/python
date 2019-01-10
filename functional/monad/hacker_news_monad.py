#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'functional/monad'))
	print(os.getcwd())
except:
	pass

#%%
import os

os.getcwd()


#%% 
"""
And Monads for (Almost) All: The State Monad
--------------------------------------------

http://rcardin.github.io/design/programming/fp/monad/2018/11/22/and-monads-for-all-state-monad.html)
"""


#%%
"""
Hacker News 
-----------

And Monads for All: The State Monad
curryhoward (37 days ago)

I think this article makes a simple concept seem unnecessarily convoluted. The first paragraph says:

    > This very complex object coming from the Category Theory is so important in functional programming that is very hard to program without it in this kind of paradigm.

May I try to dispel this myth that monads (and functional programming ideas in general) are complex?

New functional programmer are often faced with a dilemma: how do I do side effects (e.g., mutable state) in a purely functional way? Isn't that a contradiction? In 1989, Eugenio Moggi gave us a compelling answer to these questions: monads. The idea of monads originally comes from category theory, but category theory is not at all necessary to understand them as they apply to programming.
"""


"""
We start with this: since a pure functional programming language doesn't have step-by-step procedures built into the language, we instead have to choose our own suitable representation for impure programs and define a notion for composing them together. For example, a stateful program (a program that has read/write access to some piece of mutable state) can be represented by a function which takes the initial state and returns a value and the new state (as a pair).

So, for example, if the mutable state is some integer value, then stateful programs that return a value of type `a` will have this type:

    Int -> (a, Int)

Let's give that type constructor a convenient name:

    StatefulProgram(a) = Int -> (a, Int)
"""

#%%
from typing import Callable
from typing import Tuple
from typing import TypeVar
from typing import NewType


# If the mutable state is type `int`
# Stateful programs that return a value of type `a` will have this type

a = TypeVar('a')

State = int

State

#%%
NewState = Tuple[a, State]

NewState

#%%
StatefulProgram = Callable[[State], NewState[a]]

StatefulProgram[str]


#%%
"""
One key piece of the story is that this type constructor is a functor, which is just a fancy way to say that we can `map` over it (like we can for lists):

    map(f, program) = function(initialState) {
        (result, newState) = program(initialState)
        return (f(result), newState)
    }
"""

#%%
def fmap(program: StatefulProgram[a], f: Callable[[a], State]) -> NewState[a]: 
    def function(initialState: State) -> NewState[a]:
        result, newState = program(initialState)
        return f(result), newState
    return function


#%%
"""
Then, if we have a stateful program which produces a string (i.e. its type is `StatefulProgram(String)`) and a function `stringLength` which takes a string and returns its length, we could easily convert the program into a new program that returns the length of the string instead of the string itself:

    newProgram = map(program, stringLength)

"""

#%%
def stringLength(s: str) -> int:
    return len(s)

def program(initial_state: State) -> NewState[str]:
    return "initial_state", initial_state

program(5)


#%%
newProgram = fmap(program, stringLength)

newProgram

#%%
initialState: State = 5

program(initialState)

#%%
newProgram(initialState)


#%%
"""
Another way to phrase this is: we can compose a stateful program with a pure function to get a new stateful program. But that's not quite enough to write useful programs. We need to be able to compose two stateful programs together. There are a few equivalent ways to define this. In Haskell, we would have a function pronounced bind that takes a stateful program and a callback. The callback gets the result of the stateful program and returns a new stateful program to run next.

    bind(program, callback) = function(initialState) {
        (result, newState) = program(initialState)
        newProgram = callback(result)
        return newProgram(newState)
    }
"""

#%%
# def bind(program, callback): pass

"""
Some languages call this function `flatMap` instead of `bind`. In JavaScript, this is like the `then` function for promises. Whatever we call it, we can easily use it to write a helper function which sequences two stateful programs:

    sequence(program1, program2) = bind(program1, function(result) {
        return program2
    })

This amounts to running the first program, throwing away its result (see that the `result` variable is never used), and then running the second program.
"""

#%%

"""
One more ingredient is needed to make this `StatefulProgram` idea really useful. We need a way to construct a stateful program that just produces a value without touching the state. We'll call this function `pure`:

    pure(x) = function(initialState) {
        return (x, initialState)
    }
"""

"""
Here's what makes `StatefulProgram` a monad:
    a) First of all, it needs to be a functor. That amounts to having a `map` function like we defined above.
    
    b) We need a way to construct a `StatefulProgram(a)` given an `a`. That's our `pure` function.

    c) We need some notion of composition. That's given by our `bind` function. (And note that `sequence` is just a special case of `bind` where the callback doesn't use its argument.)

Category theory also gives us some common sense laws that monads must satisfy. For example, `bind(pure(x), callback) = callback(x)`.
"""

"""
The brilliant insight of Eugenio Moggi is that these three functions are essentially an interface for any kind of side effect. Mutable state is just one example. We could represent other kinds of side-effectful programs in the same way. For example, a program which returns multiple times could be represented as a list. Then the `map` and `flatMap`/`bind` functions are exactly what you expect, and the `pure` function just constructs a list with a single element. Other examples of monads are IO (for interacting with the operating system), continuations (for doing fancy control flow), maybe/optional (for programs that may return a `null` value), exceptions, logging, reading from an environment (e.g., for threading environment variables through your program), etc. They all have the same interface, which is represented in Haskell as the `Monad` type class (type classes are Haskell's notion of interfaces).
"""

"""
Haskell also provides a convenient syntax called `do notation` for working with monads (this is a vast generalization of the async/await syntax that is creeping into some popular languages). For example, a stateful program that reads the state and mutates it could be written like this:

    program = do
        x <- get     -- Read the state
        put 3        -- Update the state
        pure (x + 3) -- Return what the state used to be plus 3

In our syntax, that would be equivalent to writing:

program = bind(get, function(x) {
    return bind(put(3), function(result) {
      return pure(x + 3)
    })
  })


That callback hell is quite an eyesore, and I think that's one of several reasons why monads are not very popular outside of the Haskell community.
"""


#%% [END OF FILE]



"""
In Haskell, we would have a function pronounced bind that takes a stateful program and a callback. The callback gets the result of the stateful program and returns a new stateful program to run next.

    bind(program, callback) = function(initialState) {
        (result, newState) = program(initialState)
        newProgram = callback(result)
        return newProgram(newState)
    }
"""

#%%
def bind(program, callback):
    def function(initialState):
        result, newState = program(initialState)
        newProgram = callback(result)
        return newProgram(newState)
    return function

bind(program, stringLength)(initialState)

