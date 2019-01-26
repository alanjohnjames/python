"""
spicydonuts/purescript.md

https://gist.github.com/spicydonuts/a2e712bc1872ee9eb898   

data Direction
  = North
  | South
  | East
  | West

class Reversible a where
  reverse :: a -> a

instance reversibleDirection :: Reversible Direction where
  reverse North = South
  reverse South = North
  reverse East = West
  reverse West = East

mirror :: forall a. (Reversible a) => a -> Tuple a a
mirror a = Tuple a (reverse a)

"""

#%%
from typing import TypeVar, Generic, Union
from dataclasses import dataclass

#%%
# NOTE: Should Direction be;
# a conventional class Direction
# or a Union https://mypy.readthedocs.io/en/latest/kinds_of_types.html?highlight=union#union-types

@dataclass(frozen=True)
class Direction: pass

class North(Direction): pass
class South(Direction): pass
class East(Direction): pass
class West(Direction): pass


#%%
# NOTE: Should Reversible be; 
# a Generic https://mypy.readthedocs.io/en/latest/generics.html
# or a Protocol https://mypy.readthedocs.io/en/latest/protocols.html#simple-user-defined-protocols

T = TypeVar('T')

# NOTE: Not actually used
class Reversible(Generic[T]):  # pylint: disable=unsubscriptable-object
    reverse: T

def reverse_direction(reverse: Direction) -> Direction:
    return {
        North(): South(),
        South(): North(),
        East(): West(),
        West(): East()
    }[reverse]


#%%
reverse_direction(North()) == South()
reverse_direction(South()) == North()
reverse_direction(East()) == West()
reverse_direction(West()) == East()

