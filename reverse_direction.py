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

instance reverseDirection :: Reversible Direction where
  reverse North = South
  reverse South = North
  reverse East = West
  reverse West = East

mirror :: forall a. (Reversible a) => a -> Tuple a a
mirror a = Tuple a (reverse a)

"""

#%%
from typing import TypeVar, Generic, Union, Type
from dataclasses import dataclass

#%%
# NOTE: Should Direction be;
# a conventional class Direction
# or a mypy Union https://mypy.readthedocs.io/en/latest/kinds_of_types.html?highlight=union#union-types

@dataclass(frozen=True)
class Direction: pass

class North(Direction): pass
class South(Direction): pass
class East(Direction): pass
class West(Direction): pass


#%%
# NOTE: Should Reversible be; 
# Generic https://mypy.readthedocs.io/en/latest/generics.html

T = TypeVar('T')

@dataclass(frozen=True)  # NOTE: Must be immutable (forzen) to use as dict key
class Reversible(Generic[T]):  # pylint: disable=unsubscriptable-object
    type: T

# NOTE: How to use Reversible ?
Reversible[Direction]
Reversible[North]
Reversible[str]

#%%
# TODO: Why does reverse: Reversible[Direction] cause mypy error ?
def reverse_direction(reverse: Type[Direction]) -> Type[Direction]:
    # NOTE: This is a dict of *types* not class *instances*
    return {
        North: South,
        South: North,
        East: West,
        West: East
    }[reverse]


#%%
reverse_direction(North) == South
reverse_direction(South) == North
reverse_direction(East) == West
reverse_direction(West) == East

#%%
# NOTE: Should Reversible be; 
# Protocol https://mypy.readthedocs.io/en/latest/protocols.html#simple-user-defined-protocols
