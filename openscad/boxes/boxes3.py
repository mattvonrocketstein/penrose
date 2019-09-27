import os
import random
# ( union, translate, cube, polygon, color,
#   difference, cube, OpenSCADObject)
from solid import (
    cube, color, union, cube, difference, hole,
    translate, rotate)
from solid.utils import (
    Red, Black, Blue, back, forward, up, down, right, left,
    scad_render_to_file, scad_render)
SCAD_SEGMENTS = 10
MU = 2
SIGMA = 1


BASE1, BASE2 = cube(1), cube(2)


def basic():
    return union()(BASE1, BASE2,)


def salt(scalar=1):
    return 1  # scalar * random.gauss(MU, SIGMA)


def salt_vector(*vector):
    return [salt(scalar) for scalar in vector]


unitVectors = [
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    [0, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [1, 1, 1],
]
saltedVectors = [
    salt_vector(*v) for v in unitVectors
]

cube1 = cube(1)

import operator
unitVectors += [[operator.neg(x) for x in u] for u in unitVectors]
BASIC = basic()

MAIN = []
ANGLES = [45]


def widget():
    return [
        translate(v)(BASIC)
        for v in unitVectors]


for i, angle in enumerate(ANGLES):
    for w in widget():
        for v in unitVectors:
            rotation = rotate(angle, v)(w)
            obj = rotation - hole()(
                rotate(angle - 45, v)(w)
            )
            if i % 2 == 0:
                color(Red)(obj)
            MAIN.append(obj)

MAIN = rotate([-90, 90, 45])(union()(MAIN))
# + \
#     color(Black)(back(5)(left(5)(down(10.5)(cube(10))))) + \
#     color(Black)(back(0)(left(5)(up(0)(cube(10, center=True)))))
# MAIN = union()([up(5)(rotate(270)(MAIN)) + color(Black)
#                 (back(7)(rotate(180)(cube(10, center=True))))])
scad_render_to_file(
    MAIN,
    os.environ.get('EXPORT_AS', __file__ + '.scad'),
    include_orig_code=False,
    file_header='$fn = %s;' % SCAD_SEGMENTS)
