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
from typing import TypeVar, Generic, Union, Type, Iterable
from typing_extensions import Protocol
from enum import Enum

from dataclasses import dataclass
from functional.type_classes.direction_class import Direction
from functional.type_classes.direction_class import North, South, East, West

#%%
# NOTE: Should Reversible be; 
# Protocol https://mypy.readthedocs.io/en/latest/protocols.html#simple-user-defined-protocols

T = TypeVar('T')

class Reversible(Protocol):
    @staticmethod
    def reverse(item: T) -> T:
        ...

class ReverseDirection:  # NOTE: No Reversible base class!
    @staticmethod
    def reverse(direction: Direction) -> Direction:
        return {
            North: South,
            South: North,
            East: West,
            West: East
        }[direction]

#%%
# NOTE: How to use Reversible ?
ReverseDirection.reverse(North)

#%%
def reverse_all(items: Iterable[Reversible]) -> list:
    return [ReverseDirection.reverse(item) for item in items]

#%%
rev = reverse_all([North])

rev

#%%
print(rev)

#%%
