import os
import math
import random
import operator
import cmath
import cairocffi as cairo

from solid import (
    union, translate, cube, polygon, color,
    difference, cylinder, OpenSCADObject)
from solid.utils import (forward, back, up, down, left,
                         right, scad_render_to_file)
SCAD_SEGMENTS = 33
from solid import *
objects = []
MU = 2
SIGMA = 1


def salt(x=1):
    return x * random.gauss(MU, SIGMA)


def saltv(v):
    return map(salt, v)


def saltm(m):
    return [saltv(v) for v in m]


unitVectors = [
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    # [0, 1, 1],
    # [1, 1, 0],
    # [1, 0, 1],
    # [1, 1, 1],
]
offsetVectors = saltm([
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 0],
    [0, 0, 0],
])

cube1 = cube(1)

MAIN = []
STEP = 90
A90 = ANGLES = range(0, 360 + STEP, STEP)
STEP = 180
A180 = ANGLES = range(0, 360 + STEP, STEP)


def widget():
    return [
        mirror(v)(cube(1))
        for v in unitVectors]


for angle in A180:
    for w in widget():
        for v in unitVectors:
            MAIN.append(rotate(angle, v)(w))

MAIN = union()(MAIN)
MAIN += union()(
    [mirror(v)(translate(v)(
        rotate(90, v)(MAIN))) for v in unitVectors])
MAIN += up(.5)(back(.5)(MAIN))
MAIN += left(.5)(down(.5)(MAIN))
MAIN += forward(.5)(right(.5)(MAIN))
MAIN += up(.5)(back(.5)(MAIN))
MAIN += left(.5)(down(.5)(MAIN))
MAIN += forward(.5)(right(.5)(MAIN))
# MAIN += union()(
#     [scale(v)(translate(v)(
#         rotate(90, v)(MAIN))) for v in unitVectors])
print(scad_render(MAIN))
scad_render_to_file(
    MAIN,
    os.environ.get('EXPORT_AS', __file__ + '.scad'),
    include_orig_code=False,
    file_header='$fn = %s;' % SCAD_SEGMENTS)
