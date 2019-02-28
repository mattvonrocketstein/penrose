import os
from penrose import util, objects
from penrose.objects import Collection, cross3d, jax
from penrose.mutators import Transmogrifier
from penrose.data import (
    CUBE1, SPHERE1,
    ALL_UNIT_VECTORS, UNIT_VECTORS, NEG_UNIT_VECTORS)

LOGGER = util.get_logger(__name__)

if __name__ == '__main__':
    base =
    main = Transmogrifier(base=objects.star()).simple_symmetric_compound(3)
    main = Collection(main)
    main.render()
