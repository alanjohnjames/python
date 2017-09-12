""" Python Algebraic Data Types (ADTs)

    `Shape` example from `F# For Fun and Profit`

    Pattern matching with union types
    https://swlaschin.gitbooks.io/fsharpforfunandprofit/content/posts/key-concepts.html

    In the following example, we create a Shape type
    representing four different shapes and
    then define a draw function with different behavior
    for each kind of shape.

    This is similar to polymorphism in an object oriented language,
    but based on functions.
"""

# %%
""" Define a "union" of alternative structures

    type Shape =
    | Circle of int
    | Rectangle of int * int
    | Polygon of (int * int) list
    | Point of (int * int)
"""

# shape_type = (if_circle, if_rectangle, if_polygon, if_point)

def circle(radius):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_circle(radius)

def rectangle(width, length):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_rectangle(width, length)

def polygon(list_of_points):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_polygon(list_of_points)

def point(x, y):
    return lambda if_circle, if_rectangle, if_polygon, if_point: if_point(x, y)


# %%
""" Define a function "draw" with a shape param

    let draw shape =
        match shape with
            | Circle radius ->
                printfn "The circle has a radius of %d" radius
            | Rectangle (height,width) ->
                printfn "The rectangle is %d high by %d wide" height width
            | Polygon points ->
                printfn "The polygon is made of these points %A" points
            | _ -> printfn "I don't recognize this shape"
"""

# type printShape = Shape -> String
def print_shape(shape):
    return shape(
        if_circle=lambda radius: "radius: {0}".format(str(radius)),
        if_rectangle=lambda width, length: "width: {0}, length: {1}".format(str(width), str(length)),
        if_polygon=lambda list_of_points: ["point: {0}".format(str(print_shape(point))) for point in list_of_points],
        if_point=lambda x, y: "x: {0}, y: {1}".format(str(x), str(y)))

# %%
"""
    let circle = Circle(10)
    let rect = Rectangle(4,5)
    let polygon = Polygon( [(1,1); (2,2); (3,3)])
    let point = Point(2,3)

    [circle; rect; polygon; point] |> List.iter draw
"""

cir = circle(1.0)
rec = rectangle(1.0, 2.0)
pol = polygon([point(3.0, 4.0), point(5.0, 6.0), cir, rec])
pnt = point(7.0, 8.0)

shapes = [cir, rec, pol, pnt]

for s in shapes:
    print(print_shape(s))

print("Finished...")
