##
#
##

from solid.solidpython import OpenSCADObject
import os
import datetime
from penrose import util

LOGGER = util.get_logger(__name__)

SCAD_BIN_DEFAULT = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'

# headers from: lib/shapes.scad
HEADERS = """box(width, height, depth);
roundedBox(width, height, depth, radius);
cone(height, radius);
ellipticalCylinder(width, height, depth);
ellipsoid(width, height);
hexagon(height, depth);
octagon(height, depth);
dodecagon(height, depth);
hexagram(height, depth);
rightTriangle(adjacent, opposite, depth);
equiTriangle(side, depth);
12ptStar(height, depth);""".split(';')
# tube(height, radius, wall, center = false);
# tube2(height, ID, OD, center = false);
# ovalTube(width, height, depth, wall, center = false);


# class shapes(object):
#     pass
#
#
# HEADERS = filter(None, [x.strip() for x in HEADERS])
# for line in HEADERS:
#     name = line[:line.find('(')].strip()
#     args = line[line.find('(') + 1:line.find(')')]
#     args = [x.strip() for x in args.split(',')]
#     fxn = eval(
#         "lambda {}: util.union()(_{}({}))".format(
#             ",".join(args), name,
#             ",".join(args)
#         ))
#     import new
#     kls = type(
#         '_{}'.format(name),
#         (OpenSCADObject,),
#         {'__init__':
#             classmethod(
#                 lambda himself, **kwargs:
#                     OpenSCADObject.__init__(himself, name, kwargs),
#             )
#          })()
#     setattr(shapes, '_{}'.format(name), kls)
#     setattr(shapes, name, fxn)

def hexagon(size, height):
    return util.union()(_hexagon(size, height))


class _hexagon(OpenSCADObject):
    def __init__(self, size=None, height=None):
        OpenSCADObject.__init__(
            self, 'hexagon',
            dict(size=None, height=None))


def octagon(size, height):
    return util.union()(_octagon(size, height))


class _octagon(OpenSCADObject):
    def __init__(self, size=None, height=None):
        OpenSCADObject.__init__(
            self, 'octagon',
            dict(size=size, height=height))


def roundedBox(width=None, height=None, depth=None, radius=None):
    return util.union()(_roundedBox(width=width, height=height, depth=depth, radius=radius))


class _roundedBox(OpenSCADObject):
    def __init__(self, width=None, height=None, depth=None, radius=None):
        OpenSCADObject.__init__(
            self, 'roundedBox',
            dict(width=width, height=height, depth=depth, radius=radius))


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

    def render(self, lib=''):
        """ """
        result = self.union
        print util.scad_render(result)
        LOGGER.debug('saving to: {}'.format(self.fname))
        util.scad_render_to_file(
            result, self.fname,
            include_orig_code=False,
            file_header=lib + '$fn = %s; ' % self.SCAD_SEGMENTS)
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


def star():
    base = util.cylinder(h=1, d1=1, d2=0)
    base = util.union()(
        [util.rotate([0, 180, 0])(util.translate([0, 0, 0])(base)),
         util.translate([0, 0, 0])(base)])
    tmp = [
        # util.cube(.25, center=True), # anchor
        util.translate([0, 0, -1])(
            util.union()(
                util.rotate([90, 90, 0])(util.translate([-1, 0, 0])(base)),
                util.translate([0, 0, 1])(base)))]
    tmp = util.union()(tmp)
    tmp = util.union()(tmp, util.rotate([90, 90, 90])(tmp))
    return tmp


jax = star
#
#
# def jjax():
#     base = util.cylinder(h=1, d1=1, d2=0)
#     base = util.union()(
#         [
#             util.rotate([0, 180, 0])(util.translate([0, 0, 0])(base)),
#             (util.translate([0, 0, 0])(base)),
#         ])
#     return util.translate([0, 0, -1])(util.union()(
#         [  # util.cube(1, center=True),
#             util.rotate([90, 90, 0])(util.translate([-1, 0, 0])(base)),
#             # util.translate([1, 0, 0])(base),
#             # util.translate([0, 1, 0])(base),
#             util.translate([0, 0, 1])(base),
#             # util.translate([0, 0, -1])(base),
#             # util.translate([0, -1, 0])(base),
#         ]
#     ))
#     #     [util.cube(1, center=True),
#     #      util.translate([1, 0, 0])(util.cube(1, center=True)),
#     #      util.translate([0, 1, 0])(util.cube(1, center=True)),
#     #      util.translate([0, 0, 1])(util.cube(1, center=True)),
#     #      util.translate([-1, 0, 0])(util.cube(1, center=True)),
#     #      util.translate([0, -1, 0])(util.cube(1, center=True)),
#     #      util.translate([0, 0, -1])(util.cube(1, center=True)),
#     #      ]
#     # ))
