"""Alan match.

Some ideas for a `match` function and syntax based on 

http://averagehat.github.io/posts/types.html

https://gist.github.com/chadselph/1320421

"""

#%%
from typing import Dict, Callable, Any, NamedTuple, List

from functional.pattern.chadselph_patternmatching import OfType, BadMatch

from functional.pattern.pattern_matched import GiantRobot, RobotLegs, RobotArms
from functional.pattern.pattern_matched import Rifle, Knife
from functional.pattern.pattern_matched import  Point3D, Coordinate, SkyBlue


def test_oftype():

    rifle = Rifle(ammo=10, model='gun')

    assert rifle == OfType(Rifle)

#
# DESIGN 1:
#
# When using syntax `match(robot.weapon=OfType(Rifle))` 
# the `=` operator has to act as a kind of `bind` to 
# bind the `OfType` method to the weapon.


#%%
def match1(args):
    # process args
    # process defaults
    return args

def canFight1(robot: GiantRobot) -> bool:
    if match1(robot.weapon) is OfType(Rifle):
        return robot.weapon.ammo > 0
    if match1(robot.weapon) is OfType(Knife):
        return not robot.weapon.knifeIsBlunt
    else: 
        return False  # weapon is not a Rifle or a Knife


#
# DESIGN 2:
#
# match(...) in the dict has to be a function <...> that can be called
# possibly a function wrapper / decorator

#%%
def match2(args):
    # process args
    # process defaults
    return args

def canFight2(robot: GiantRobot) -> bool:
    return {  # type: Dict[Callable, bool]
        match2(robot.weapon) == OfType(Rifle): robot.weapon.ammo > 0,
        match2(robot.weapon) == OfType(Knife): not robot.weapon.knifeIsBlunt,
        match2(robot.weapon) == OfType(Rifle): False  # weapon is not a Rifle or a Knife
    }[robot]


#
# DESIGN 3:
#
# I like this design the best...

def match3(*args, conditions: Dict[Callable, Any]) -> Any:

    print(args)

    print(conditions)

    # all(passed == spec for (passed, spec) in zip(args, function.__defaults__))

    arg0 = args[0]

    matches = [(arg0 == key, func) for key, func in conditions.items()]
    result = matches[0][1](arg0)

    return result


def canFight3(robot: GiantRobot) -> bool:

    conds = {
        OfType(Rifle): lambda robot_weapon: robot_weapon.ammo > 0,
        OfType(Knife): lambda robot_weapon: not robot_weapon.knifeIsBlunt,
        OfType(Rifle): lambda robot_weapon: False  # weapon is not a Rifle or a Knife
    }

    result = match3(robot.weapon, conditions=conds)

    return result


def test_can_fight3():

    point = Point3D(0, 1.0, 3.98)
    points = [point, point, point]

    robot = GiantRobot(weapon=Rifle(ammo=10, model='Smart gun.'),
                       legs=RobotLegs(points, points, "fizbizzle"),
                       arms=RobotArms(leftArm=points, rightArm=points, color=SkyBlue))

    canFight3(robot)

    assert True


#
# DESIGN 4:
#
# Another `match` implementation
# Using `bind` function to bind the match function to the data ?

# NOTE: Maybe bind example

def bind(data, fn):
    if data is None:
        return data
    return fn(data)

#
# DESIGN 5:
#

#%%
class Pattern5:
    def __init__(self):
        pass

    def match(self, *args):
        self.args = args

    def of_type(self, type):
        return self

    def default(self): 
        return self

def canFight5(robot: GiantRobot) -> bool:
    return Pattern5().match(robot.weapon, {  # type: Dict[Callable, bool]
        Pattern5().of_type(Rifle): robot.weapon.ammo > 0,
        Pattern5().of_type(Knife): not robot.weapon.knifeIsBlunt,
        Pattern5().default(): False  # weapon is not a Rifle or a Knife
    })


#
# DESIGN 6:
#

#%%
from dataclasses import dataclass

class Pattern6:

    def __init__(self, *args):
        self.pattern = args

    def match(self, conditions: dict):
        keys = list(conditions.keys())
        values = list(conditions.values())
        pattern = self.pattern


        {}
        all(passed == spec for (passed, spec) in zip(keys, values))

        return {    
            self.pattern[0] == keys[0]: values[0]
        }[True]


#%%
Pattern6(1).match({
    1: 'one',
    2: 'two',
    3: 'three',
    4: lambda x: x*x
})

#%%
p = Pattern6(2, 1)

p.pattern

#%%
m = {
    (1, 1): 'one-one',
    (1, 2): 'one-two',
    (2, 1): 'two-one',
    (2, 2): 'two-two',
}

m[p.pattern]


#%%
p.match(m)


#
# DESIGN 7: simple `match` function
#

#%%
a = 2
b = 1

#%%
def pattern(*args):
    return all(args)

pattern(a == 2, b == 1)

#%%
a = 2
b = 1

m = {
    pattern(a == 1, b == 1): 'one-one',
    pattern(a == 1, b == 2): 'one-two',
    pattern(a == 2, b == 1): 'two-one',
    pattern(a == 2, b == 2): 'two-two',
}

m


#
# DESIGN 7:
#

#%%
from dataclasses import dataclass

class Pattern7:

    def __init__(self, *args):
        self.args = args

    def match(self, conditions: dict):
        keys = list(conditions.keys())
        values = list(conditions.values())

        # TODO: How to pass the conditions in here? 
        return {
            pattern(a == 1, b == 1): 'one-one',
            pattern(a == 1, b == 2): 'one-two',
            pattern(a == 2, b == 1): 'two-one',
            pattern(a == 2, b == 2): 'two-two',
        }[True]



#%%
def match(*kwargs, conditions: dict):

    p = pattern(kwargs)

    print(f"kwargs = {kwargs}")

    return conditions[True]

# TODO: def values(...)
k = {'c': 2, 'd': 1}

match(*k, conditions={True: 'Matched condition...'})


#%%

# TODO: This is the syntax I want...
# TODO: conditions=lambda x, y: {(x==.., y==..): ...}
match({'a': 2, 'b': 2}, conditions={
    pattern(a == 1, b == 1): 'one-one',
    pattern(a == 1, b == 2): 'one-two',
    pattern(a == 2, b == 1): 'two-one',
    pattern(a == 2, b == 2): 'two-two',
})


# TODO: This is the syntax I want...
def match(a, b, conditions):
    # TODO: Code to construct the conditions dict...in terms of `a` and `b`
    return conditions[True] 

# TODO: This is the syntax I want...
match(a=2, b=2, conditions={
    pattern(1, 1): 'one-one',  # TODO: Here patern returns a `tuple` 
    pattern(1, 2): 'one-two',
    pattern(2, 1): 'two-one',
    pattern(2, 2): 'two-two',
})

#%%
# https://medium.com/@jondot/functional-programming-with-python-for-people-without-time-1eebdbd9526c
# 
# As described in the above article, the function `pattern(...)` could be curried
# and match incrementally on each argument each time returning a new ( partially matched) funciton. 
#
# Remember that the arguments to `pattern` function imply and *and* condition between matches. 
# Are more flexible design might be to have a single key (rather than a `tuple`) that makes the `and` explicit;

a = 2
b = 1

conditions={
    a == 1 and b == 1: 'one-one',
    a == 1 and b == 2: 'one-two',
    a == 2 and b == 1: 'two-one',
    a == 2 and b == 2: 'two-two',
}[True]

conditions


#%%
