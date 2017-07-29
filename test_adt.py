""" Python Algebraic Data Types (ADTs) """

# From last comment post: http://stupidpythonideas.blogspot.co.uk/2014/08/adts-for-python.html 

import date

# type durationPeriod = end_date * duration
# type datePeriod = end_date * start_date
# type Period = durationPeriod | datePeriod

def duration_period(end_date, duration):
    return lambda if_duration, if_date: if_duration(end_date, duration)

def date_period(end_date, start_date):
    return lambda if_duration, if_date: if_date(end_date, start_date)

# In what way are duration_period and date_period a data type (class) ?
# I suppose duration_period and date_period could be methods (type ctors) in class Period


# Period -> String
def print_period(period):  # period -> match_period
    return period(
        if_duration = lambda end_date, nPeriods:
            "end_date: {0}, nPeriods: {1}".format(str(end_date), str(nPeriods)), 
        if_date = lambda end_date, start_date:
            "end_date: {0}, start_date: {1}".format(str(end_date), str(start_date)))

def calc_period(period):
    return period(
        if_duration = lambda end_date, nPeriods: nPeriods,
        if_date = lambda end_date, start_date: end_date - start_date)


start = date(2017, 7, 28)
end = date(2017, 8, 28)
duration = "1D"

print_period(date_period(start, end))
print_period(duration_period(start, duration))


calc_period(date_period(start, end))
calc_period(duration_period(start, duration))


# Shape example from F#

# - Pattern matching with union types
#   https://swlaschin.gitbooks.io/fsharpforfunandprofit/content/posts/key-concepts.html

"""fsharp
type Shape =        // define a "union" of alternative structures
| Circle of int 
| Rectangle of int * int
| Polygon of (int * int) list
| Point of (int * int) 
"""

shape_type = (if_circle, if_rectangle, if_polygon, if_point)

def circle(radius):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_circle(radius)

def rectangle(width, length):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_rectangle(width, length)

def polygon(list_of_points):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_polygon(list_of_points)

def point(x, y):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_point(x, y)


# Period -> String
def print_shape(shape):  # period -> match_period
    return shape(
        if_circle = lambda radius: "radius: {0}".format(str(radius)), 
        if_rectangle = lambda width, length: "width: {0}, length: {1}".format(str(width), str(length)),
        if_polygon = lambda list_of_points: ["x: {0}, y: {1}".format(str(x), str(y)) for p in list_of_points],
        if_rectangle = lambda width, length: "width: {0}, length: {1}".format(str(width), str(length)))


