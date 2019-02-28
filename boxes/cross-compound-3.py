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
    main = Transmogrifier(
        base=cross3d()).simple_symmetric_compound(iterations=3)
    main = main
    main = Collection(main)
    main.render()
