import os
from penrose import util
from penrose.objects import Collection, cross3d
from penrose.mutators import Transmogrifier
from penrose.data import (
    CUBE1, SPHERE1,
    # VECTOR_X, VECTOR_Y, VECTOR_Z,
    ALL_UNIT_VECTORS, UNIT_VECTORS, NEG_UNIT_VECTORS)

LOGGER = util.get_logger(__name__)


if __name__ == '__main__':
    base = CUBE1  # cross3d()
    triple = Transmogrifier(base=base).simple_symmetric_compound(iterations=2)
    double = Transmogrifier(base=base).simple_symmetric_compound(iterations=1)
    main = Transmogrifier(base=triple).chomp(double, scale=.25)
    main = Collection(main)
    main.render()
