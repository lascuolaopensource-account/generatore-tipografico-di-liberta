# -*- coding: utf-8 -*-

### MODULES
from random import choice






### FUNCTIONS - UTILITY

# interpolate_points
# Interpolation of two tuples

# tuple, tuple, float -> tuple
def interpolate_points(pA, pB, f):
    return tuple([pA[i]+(pB[i]-pA[i])*f for i in (0, 1)])



# drawer
# A general function that links any given points

# RGlyph, list -> RGlyph
def drawer(gly, pts):

    # Getting glyph pen
    pen = gly.getPen()

    # Moving pen to first point of the list
    pen.moveTo(pts[0])

    # Drawing lines to the rest of the points
    for i in range(1, len(pts)):

        # Current point
        pt = pts[i]

        # If next point is expressed as tuple, that's a line point
        if len(pt) == 2:
            pen.lineTo(pt)

        # If next point is expressed as (tuple, tuple, float), that's a curve point
        elif len(pt) == 3:

            # Previous point
            if len(pts[i-1]) == 2:
                pt_previous = pts[i-1]
            elif len(pts[i-1]) == 3:
                pt_previous = pts[i-1][1]

            # Control point out
            cpt_o = interpolate_points(pt_previous, pt[0], pt[2])

            # Control point in
            cpt_i = interpolate_points(pt[1], pt[0], pt[2])

            # Drawing curve
            pen.curveTo(cpt_o, cpt_i, pt[1])

    pen.closePath()
    return gly



# make_clockwise
# does what it says

# RContour, boolean -> RContour
def make_clockwise(c, cw):

    # Making clockwise anyways
    if c.clockwise == 0:
        c.reverseContour()

    # Inverting if necessary
    if cw == False:
        c.reverseContour()

    return c






### FUNCTIONS - SHAPES

# do_nothing
# Does nothing - Used to leave blank space

# RGlyph, tuple, tuple, dict ->
def do_nothing(gly, position, size, properties):
    pass



# rectangle

# RGlyph, (float, float), (float, float), dict ->
def rectangle(gly, position, size, properties):

    # Getting rectangle properties
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points (ideally, we draw at (0,0), then we translate)
    p0 = -w, -h
    p1 = -w,  h
    p2 =  w,  h
    p3 =  w, -h

    # Drawing contour
    drawer(gly, [p0, p1, p2, p3])

    # Contour operations: scale, rotate, translate, clockwise, round points
    c = gly[-1]
    c.scale(scl)
    c.rotate(rot)
    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# ellipse
# Draws an ellipse

# RGlyph, (float, float), (float, float) dict ->
def ellipse(gly, position, size, properties):

    # Getting rectangle properties
    sqr = properties["squaring"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points (ideally, we draw at (0,0), then we translate)
    p0 = -w,  0
    p1 = -w,  h
    p2 =  0,  h
    p3 =  w,  h
    p4 =  w,  0
    p5 =  w, -h
    p6 =  0, -h
    p7 = -w, -h

    # Drawing contour
    drawer(gly,
           [p0, (p1, p2, sqr), (p3, p4, sqr), (p5, p6, sqr), (p7, p0, sqr)])

    # Contour operations: scale, rotate, translate, clockwise, round points
    c = gly[-1]
    c.scale(scl)
    c.rotate(rot)
    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# quarter
# Draws a quarter of circumference

# RGlyph, (float, float), (float, float), dict ->
def ellipse_quarter(gly, position, size, properties):

    # Getting quarter properties
    sqr = properties["squaring"]
    orn = properties["orientation"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points
    p0 = -w, -h
    p1 = -w,  h
    p2 =  w,  h
    p3 =  w, -h

    # Drawing contour
    drawer(gly, [p0, p1, (p2, p3, sqr)])

    # Contour operations - Selecting contour
    c = gly[-1]

    c.scale(scl)

    # Mirroring
    if "N" in orn:
        if "W" in orn:
            c.scale((-1,  1))
        elif "E" in orn:
            pass
    if "S" in orn:
        if "W" in orn:
            c.scale((-1, -1))
        elif "E" in orn:
            c.scale(( 1, -1))

    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# ellipse_quarter_ro
# Ellipse quarter with random orientation
def ellipse_quarter_ro(gly, position, size, properties):

    # Choosing random orientation
    properties["orientation"] = choice(["NW", "SW", "NE", "SE"])

    # Drawing ellipse
    ellipse_quarter(gly, position, size, properties)



# quarter
# Draws a quarter of circumference

# RGlyph, (float, float), (float, float), dict ->
def ellipse_half(gly, position, size, properties):

    # Getting quarter properties
    sqr = properties["squaring"]
    orn = properties["orientation"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points
    p00 = -w,  0
    p01 = -w,  h
    p02 =  0,  h
    p03 =  w,  h
    p04 =  w,  0
    p05 =  0,  0
    p06 = p04
    p07 =  w, -h
    p08 = -w, -h
    p09 = p00
    p10 = p05

    # Drawing contour
    drawer(gly, [p00, (p01, p02, sqr), (p03, p04, sqr), p05, (p06, p07, sqr), p08, (p09, p10, sqr)])

    # Contour operations - Selecting contour
    c = gly[-1]

    # Orientating
    if   "N" == orn:
        pass
    elif "S" == orn:
        c.scale((1, -1))
    elif "W" == orn:
        c.rotate(-90)
        c.scale((size[0]/size[1], size[1]/size[0]))
    elif "E" == orn:
        c.rotate(90)
        c.scale((size[0]/size[1], size[1]/size[0]))

    make_clockwise(c, clw)
    c.move(position)
    c.round()
    gly.update()



# ellipse_half_ro
# Ellipse half with random orientation
def ellipse_half_ro(gly, position, size, properties):

    # Choosing random orientation
    properties["orientation"] = choice(["E", "W", "N", "S"])

    # Drawing ellipse
    ellipse_half(gly, position, size, properties)






### SYMBOL FUNCTION


# Draws a symbol taken from a glyph
# RGlyph, (float, float), (float, float), dict ->
def symbol(gly, position, size, properties):

    # Getting symbol properties
    src = properties["source_glyph"]
    scl = properties["scale"]
    rot = properties["rotation"]
    proportions_keep = properties["proportions_keep"]
    proportions_mode = properties["proportions_mode"]

    # Useful shortcut
    w = size[0]
    h = size[1]

    # Getting source glyph size and position
    src_x = src.box[0]
    src_y = src.box[1]
    src_wdt = abs(src.box[0] - src.box[2])
    src_hgt = abs(src.box[1] - src.box[3])

    # Calculating scaling factor
    scl_x = w/src_wdt
    scl_y = h/src_hgt


    # Iterating over all contours in source glyph
    for c in src:

        # Copying contour
        d = c.copy()

        # Moving the contour to (0,0)
        d.move((-src_x - src_wdt/2, -src_y - src_hgt/2))

        # Scaling the glyph accordingly to properties
        if proportions_keep == False:
            d.scale((scl_x, scl_y))
        else:
            if   proportions_mode == "X":
                d.scale((scl_x, scl_x))
            elif proportions_mode == "Y":
                d.scale((scl_y, scl_y))

        # Contour operations
        d.scale(scl)
        d.rotate(rot)
        d.move(position)
        d.round()

        # Getting pen on target glyph
        pen = gly.getPen()
        # Drawing contour on target glyph
        d.draw(pen)


# Draws a random symbol taken from a glyph list
# RGlyph, (float, float), (float, float), dict ->
def symbol_list(gly, position, size, properties):

    # Getting glyph list
    gly_list = properties["source_glyph_list"]

    # Building symbol properties
    p_symbol = {
        "source_glyph"    : choice(gly_list),
        "scale"           : properties["scale"],
        "rotation"        : properties["rotation"],
        "proportions_keep": properties["proportions_keep"],
        "proportions_mode": properties["proportions_mode"]
    }

    symbol(gly, position, size, p_symbol)






### FUNCTIONS - COMPOSITION

# random_function
# This function accepts a list of tuples with this structure:
# (function_name, function_properties)
# It randomly chooses one of those and runs it

# RGlyph, (float, float), (float, float), list
def random_function (gly, position, size, properties):

    # Choosing randomly a tuple (function, function_properties)
    random_choice = choice(properties)

    # Function name (type: function)
    f_name = random_choice[0]

    # Function properties (type: dictionary)
    f_prop = random_choice[1]

    # Running function
    f_name(gly=gly, position=position, size=size, properties=f_prop)
