import numpy as np
import os
from penrose import util
from penrose import objects
from penrose.mutators import Transmogrifier
from penrose import data
from penrose.data import (
    CUBE1, SPHERE1,
    # VECTOR_X, VECTOR_Y, VECTOR_Z,
    ALL_UNIT_VECTORS, UNIT_VECTORS, NEG_UNIT_VECTORS)

LOGGER = util.get_logger(__name__)

SHAPE_LIB = open('lib/shapes.scad', 'r').read()
if __name__ == '__main__':
    main = Transmogrifier(
        # random_combinators=[
        #     util.union,
        #     #     # util.difference,
        # ],
        base=objects.roundedBox(5, 5, 5, 5),
        # base=objects.hexagon(5, 8),
        # random_scale=[1, 3, 5, 8],
        rotation_vectors=np.array(
            [data.VECTOR_X, data.VECTOR_Y,
                data.VECTOR_Z, data.VECTOR_NEG_Z,
                data.VECTOR_NEG_Y,
                data.VECTOR_NEG_X],
            dtype=np.int)).simple_symmetric_compound(
                noself=True,
                iterations=1)
    main1 = util.union()(util.cube([3, 3, 3], center=True),
                         util.difference()(
        util.union()(
            util.intersection()(
                util.cube([8, 8, 8], center=True),
                Transmogrifier(base=main).chomp(CUBE1),
                # Transmogrifier(base=main).chomp(CUBE1, scale=8),
            ),
            Transmogrifier(base=util.cube(10)).simple_symmetric_compound(iterations=2),),
        util.cube([13, 13, 13], center=True),
    )
    )

    main = main1
    # main2 = Transmogrifier(
    #     base=main1,
    #     # random_scale=[1, 3, 5, 8],
    #     rotation_vectors=np.array(
    #         [data.VECTOR_Z, data.VECTOR_NEG_Z,
    #          data.VECTOR_XY, data.VECTOR_NEG_XY],
    #         dtype=np.int)).simple_symmetric_compound(
    #             noself=True,
    #             iterations=1)
    # main = util.intersection()(main1, main2, )
    main = main
    main = objects.Collection(main)
    main.render(lib=SHAPE_LIB)
