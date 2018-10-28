"""
Pattern | Matched

Some things with mypy: sum and product types

http://averagehat.github.io/posts/types.html

"""
import sys

from typing import Tuple, NamedTuple
from typing import List, Dict, Union
from typing import Generic, TypeVar, Optional

# NOTE: mypy enables static typing in python

# product type for points in a 3D plane
Point3D = NamedTuple("Point3D", [("x", float), ("y", float), ("z", float)])

Point3DTuple = Tuple[float, float, float]

point = Point3D(0, 1.0, 3.98)
x = point.x
y = point[1]  # this typechecks, it probably shouldn't

# NOTE: mypy knows how long the tuple is

# r = point[99]
# foo.py:10: error: Tuple index out of range

# NOTE: mypy enforces the safety of common operators
# This avoids meaningless comparisons...

# "foo" > sys.maxsize is True
# True # sure, why not?

# point.x + "Eureka"
# foo.py:10: error: Unsupported operand types for + ("float" and "str")

x = point.x  # mypy infers the type after assignment

# x > "Eureka" is True
# foo.py:10: error: Unsupported operand types for > ("float" and "str")

# NOTE: mypy limits attribute access

# sneaky = point.gecko
# foo.py:13: error: "Point3D" has no attribute "gecko"


# NOTE: mypy supports generics

ListOfInts = List[int]


# You can also create types by subclassing Generic

T = TypeVar('T')

class Maybe(Generic[T]):

    def __init__(self, value_or_none: Optional[T] = None) -> None:
        self.value: Optional[T] = value_or_none

    def getOrElse(self, t: T) -> Optional[T]:
        # Do something...
        if self.value is not None:
            return self.value
        else:
            return None

# Possible to use multiple type variables within a generic

E = TypeVar("E")
V = TypeVar("V")
class Either(Generic[E,V]):
    # ...
    pass


# NOTE: Let’s use List and 3DPoint to create a more complex product type

RobotLegs = NamedTuple("RobotLegs", [("leftLeg", List[Point3D]),
                                     ("rightLeg", List[Point3D]),
                                     ("color", str)])


# We only want pastel colors, and robots which exist in the cartesian plane.

points = [point, point, point]

blueRobot = RobotLegs(points, points, "fizbizzle")


# We could check for this condition in the functions that use the color:

def getColor(legs: RobotLegs) -> int:
    if legs.color not in ["skyblue", "red", "white"]:
        raise ValueError("Invalid color %s" % legs.color)
    else:
        return {
            "skyblue": 0,
            "red": 1,
            "white": 2}[legs.color]

# We only want to validate our input once.

# Do all the validation;
# -- cleaning up data from I/O,
# -- verifying it matches a certain shape,
# -- creating errors etc.
# When we construct the instances of our types.
# 
# That way all functions which accept those types are relieved from the obligation of checking themselves

SkyBlue = NamedTuple("SkyBlue", [])
PastelRed = NamedTuple("PastelRed", [])
White = NamedTuple("White", [])

Color = Union[SkyBlue, PastelRed, White]

NewRobotLegs = NamedTuple("RobotLegs", [("leftLeg", List[Point3D]),
                                        ("rightLeg", List[Point3D]),
                                        ("color", Color)])

# So we don’t have to worry about validating our data again!

def getNewColor(legs: NewRobotLegs) -> int:
    if legs.color == SkyBlue():
        return 0x87CEFA 
    elif isinstance(legs.color, SkyBlue): # this is equivalent
        return 0x87CEFA
    else:
        return 0x000000


# We can even safely use a statically typed dictionary which never raise a KeyErorr:

colors: Dict[Color, int] = { SkyBlue() : 0x87CEFA } 


# Let’s make sure the 3D coordinates are valid
# We’ll need something more powerful than a simple NamedTuple
# Note that a traditional python class won’t be safe 
# because python classes are mutable by default
# We can create more complex immutable objects in python:

class Coordinate(object):
    def __new__(self, x: float, y: float, z: float) -> Point3D:
        assert x >= 0 and y >= 0 and z >= 0
        return Point3D(x, y, z)


# NOTE: The assurance offered by static typing is significantly stronger 
# than the contract offered by ducked typing.


# Color is a very simple Union type, analogous to the “Enums” of other languages
# (including python 3), while providing additional safety.
# But union types are more powerful;
# It’s possible to create a union type out of product types,
# and model arbitrary complex systems this way.

# You can think of these types as representing the “set of all possible inputs and outputs”
# and functions accepting these types as representing the “cobminators”
# or “all the things I can ever do with my inputs”.
# Together, these form a sort of “algebra” that represents your domain.
# In the domain of giant robots:

Rifle = NamedTuple('Rifle', [('ammo' , int),
                             ('model' , str)])

Knife = NamedTuple('Knife', [('shape' , List[Coordinate]),
                             ('knifeIsBlunt', bool)])

Weapon = Union[Rifle, Knife]

RobotArms = NamedTuple("RobotArms", [("leftArm", List[Coordinate]),
                                     ("rightArm", List[Coordinate]),
                                     ("color", Color)])

GiantRobot = NamedTuple('GiantRobot', [('weapon', Weapon),
                                       ('legs' , RobotLegs),
                                       ('arms', RobotArms)])

def canFight(robot: GiantRobot) -> bool:
    if isinstance(robot.weapon, Rifle):
        return robot.weapon.ammo > 0
    else: 
        return not robot.weapon.knifeIsBlunt  # this is a knife

# Great! we’ve created an API that’s clear, self-documenting, and compartively safe.
# We’ve provided some limited guarantees of correctness;
# Our domain is well-defined, which will help us reason about our past and future code moving forward.
