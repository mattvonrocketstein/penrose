##
#
##

import os
import datetime
from penrose import util

LOGGER = util.get_logger(__name__)

SCAD_BIN_DEFAULT = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'


class Collection(object):
    SCAD_SEGMENTS = 10

    SCAD_BIN = os.environ.get('SCAD_BIN', SCAD_BIN_DEFAULT)

    def __init__(self, objects=[]):
        """ """
        self.objects = objects if isinstance(objects, list) else [objects]

    @property
    def caller_fname(self):
        import inspect
        frame = inspect.stack()[-1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        return filename

    @property
    def fname(self):
        import os
        return os.path.join(os.getcwd(), '{}.scad'.format(self.caller_fname))

    @property
    def stl_fname(self):
        return self.fname + '.stl'

    def __add__(self, other):
        if not isinstance(other, list):
            return Collection(self.objects + [other])
        else:
            raise ValueError()

    def __sub__(self, other):
        return Collection([util.difference()(self.union, other)])

    def save(self):
        """ """
        t1 = datetime.datetime.now()
        LOGGER.debug('converting to stl begins at t={}'.format(t1))
        os.system('{} -o {} {}'.format(
            SCAD_BIN_DEFAULT, self.stl_fname, self.fname))
        t2 = datetime.datetime.now()
        LOGGER.debug('converting to stl finishes at t={}'.format(t2))
        LOGGER.debug('total time: {}'.format(t2 - t1))

    @property
    def union(self):
        return util.union()(self.objects)

    def render(self):
        """ """
        result = self.union
        print util.scad_render(result)
        LOGGER.debug('saving to: {}'.format(self.fname))
        util.scad_render_to_file(
            result, self.fname,
            include_orig_code=False,
            file_header='$fn = %s;' % self.SCAD_SEGMENTS)
        return self.save()


def cross3d():
    return util.union()(
        [util.cube(1, center=True),
         util.translate([1, 0, 0])(util.cube(1, center=True)),
         util.translate([0, 1, 0])(util.cube(1, center=True)),
         util.translate([0, 0, 1])(util.cube(1, center=True)),
         util.translate([-1, 0, 0])(util.cube(1, center=True)),
         util.translate([0, -1, 0])(util.cube(1, center=True)),
         util.translate([0, 0, -1])(util.cube(1, center=True)),
         ]
    )
