##
#
##
import numpy as np

from penrose import util
# import cube, sphere

from solid.utils import (
    forward, back, up, down, left, right,
    Black, Blue, Red, Yellow,
    scad_render_to_file)

CUBE1 = util.cube(1, center=True)
SPHERE1 = util.sphere(1)

VECTOR_X = np.array([1, 0, 0])
VECTOR_Y = np.array([0, 1, 0])
VECTOR_Z = np.array([0, 0, 1])

VECTOR_XY = np.array([1, 1, 0])
VECTOR_YZ = np.array([0, 1, 1])

VECTOR_NEG_X = -1 * VECTOR_X
VECTOR_NEG_XY = -1 * VECTOR_XY
VECTOR_NEG_YZ = -1 * VECTOR_YZ
VECTOR_NEG_Y = -1 * VECTOR_Y
VECTOR_NEG_Z = -1 * VECTOR_Z

UNIT_VECTORS = np.array([VECTOR_X, VECTOR_Y, VECTOR_Z], dtype=np.int)
NEG_UNIT_VECTORS = np.array(
    [VECTOR_NEG_X, VECTOR_NEG_Y, VECTOR_NEG_Z], dtype=np.int)
ALL_UNIT_VECTORS = np.array(
    [VECTOR_X, VECTOR_Y, VECTOR_Z,
     # VECTOR_XY, VECTOR_YZ,
     VECTOR_NEG_X, VECTOR_NEG_Y, VECTOR_NEG_Z], dtype=np.int)
