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
from typing import TypeVar, Generic, Union
from dataclasses import dataclass
from functional.type_classes.direction_class import Direction
from functional.type_classes.direction_class import North, South, East, West

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

#%%
def reverse_direction(reverse: Reversible[Direction]) -> Direction:
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
