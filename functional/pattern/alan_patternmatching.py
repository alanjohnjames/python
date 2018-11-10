"""Alan match.

Some ideas for a `match` function and syntax based on 

http://averagehat.github.io/posts/types.html

https://gist.github.com/chadselph/1320421

"""

from typing import Dict, Callable, Any, NamedTuple, List

from chadselph_patternmatching import OfType,BadMatch

from pattern_matched import GiantRobot, RobotLegs, RobotArms
from pattern_matched import Rifle, Knife
from pattern_matched import  Point3D, Coordinate, SkyBlue


def test_oftype():

    rifle = Rifle(ammo=10, model='gun')

    assert rifle == OfType(Rifle)

#
# DESIGN 1:
#
# When using syntax `match(robot.weapon=OfType(Rifle))` 
# the `=` operator has to act as a kind of `bind` to 
# bind the `OfType` method to the weapon.


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

def match2(args):
    # process args
    # process defaults
    return args

def canFight2(robot: GiantRobot) -> bool:
    return {  # type: Dict[Callable, bool]
        match(robot.weapon) == OfType(Rifle): robot.weapon.ammo > 0,
        match(robot.weapon) == OfType(Knife): not robot.weapon.knifeIsBlunt,
        match(robot.weapon) == OfType(Rifle): False  # weapon is not a Rifle or a Knife
    }[robot]


#
# DESIGN 3:
#
# I like this design the best...

def match(*args, conditions: Dict[Callable, Any]) -> Any:

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

    result = match(robot.weapon, conditions=conds)

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

class Pattern:
    def __init__(self):
        pass

    def match(self, *args):
        self.args = args

    def of_type(self, type):
        return self

    def default(self): 
        return self

def canFight5(robot: GiantRobot) -> bool:
    return Pattern().match(robot.weapon, {  # type: Dict[Callable, bool]
        Pattern().of_type(Rifle): robot.weapon.ammo > 0,
        Pattern().of_type(Knife): not robot.weapon.knifeIsBlunt,
        Pattern().default(): False  # weapon is not a Rifle or a Knife
    })
