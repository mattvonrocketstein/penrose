"""
"""
import os
import numpy as np
from penrose import util
from penrose.data import (
    UNIT_VECTORS, NEG_UNIT_VECTORS,
    CUBE1)

import random


class Transmogrifier(object):
    """ """

    def __init__(self, base=None, random_combinators=None, rotation_vectors=None, random_scale=None):
        self.rotation_vectors = UNIT_VECTORS if rotation_vectors is None else rotation_vectors
        self.random_combinators = random_combinators
        self.random_scale = random_scale or [1]
        if base:
            if isinstance(base, list):
                self.base = util.union()(*base)
            else:
                self.base = base
        else:
            self.base = CUBE1
        params = getattr(self.base, 'params', None)
        self.unit = params and params.get('size', 1) or 1

    @property
    def debug(self):
        return os.environ.get('DEBUG')

    def simple_symmetric_compound(self, iterations=1, noself=False, chomp=None, angle=45):
        out = [] if noself else [self.base]
        for i, v in enumerate(self.rotation_vectors):
            v = list(angle * v)
            rscale = random.choice(self.random_scale)
            tmp = util.scale(rscale)(util.rotate(v)(self.base))
            out.append(tmp)
        if self.random_combinators is None:
            out = util.union()(out)
        else:
            new = []
            assert len(out) % 2 == 0
            while out:
                c = random.choice(self.random_combinators)
                tmp = out.pop()
                if not out:
                    new.append(tmp)
                if out:
                    new.append(c()(tmp, out.pop()))
            out = util.union()(out)

        if chomp:  # deprecate
            chomps = [util.translate(list(self.unit * v))(chomp)
                      for v in UNIT_VECTORS]
            chomps += [util.translate(list(self.unit * v))(chomp)
                       for v in NEG_UNIT_VECTORS]
            combinator = util.difference() if not self.debug else util.union()
            out = combinator(out, *chomps)
        if iterations == 1:
            return out
        else:
            return self.__class__(base=out).simple_symmetric_compound(
                iterations=iterations - 1, chomp=chomp, angle=angle)

    def chomp(self, shape, scale=1):
        """ chomps a `shape` shaped bite out every symmetric corner """
        vx = list(scale * np.array([1, 1, 1], dtype=np.float))
        _1 = 1 * scale
        return util.difference()(
            self.base,
            util.color(util.Black)(
                util.union()(
                    util.translate([_1,   _1, _1])(shape),
                    util.translate([_1,  -_1, _1])(shape),
                    util.translate([_1,  -_1, -_1])(shape),
                    util.translate([_1,   _1, -_1])(shape),
                    util.translate([-_1,  _1, -_1])(shape),
                    util.translate([-_1,  _1, _1])(shape),
                    util.translate([-_1, -_1, _1])(shape),
                    util.translate([-_1, -_1, -_1])(shape),)))
