""" Python Algebraic Data Types (ADTs)

    `Shape` example from `F# For Fun and Profit`

    Pattern matching with union types
    https://swlaschin.gitbooks.io/fsharpforfunandprofit/content/posts/key-concepts.html

    Fsharp example... define a "union" of alternative structures
    type Shape =
    | Circle of int
    | Rectangle of int * int
    | Polygon of (int * int) list
    | Point of (int * int)
"""

# %%
# shape_type = (if_circle, if_rectangle, if_polygon, if_point)

def circle(radius):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_circle(radius)

def rectangle(width, length):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_rectangle(width, length)

def polygon(list_of_points):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_polygon(list_of_points)

def point(x, y):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_point(x, y)


# type printShape = Shape -> String
def print_shape(shape):
    return shape(
        if_circle = lambda radius: "radius: {0}".format(str(radius)), 
        if_rectangle = lambda width, length: "width: {0}, length: {1}".format(str(width), str(length)),
        if_polygon = lambda list_of_points: ["x: {0}, y: {1}".format(str(x), str(y)) for p in list_of_points])

print("Finished...")
