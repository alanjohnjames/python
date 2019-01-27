"""Direction classes."""

from dataclasses import dataclass

# NOTE: Should Direction be;
# a conventional class Direction
# or a mypy Union https://mypy.readthedocs.io/en/latest/kinds_of_types.html?highlight=union#union-types

@dataclass(frozen=True)
class Direction: pass

class North(Direction): pass
class South(Direction): pass
class East(Direction): pass
class West(Direction): pass
