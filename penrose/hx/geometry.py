""" penrose.hx.geometry:
        houdini geometry wrapper
"""
import os

import hou

from penrose import (util,)
from penrose.hx.abcs import HWrapper
from .node import (Node,)

LOGGER = util.get_logger(__name__)


class Geometry(HWrapper):

    def __init__(self, name='default', unit=10, **kwargs):
        self.name = name
        self.unit = unit  # affects cameras only right now
        super(Geometry,  self).__init__(name=name,  **kwargs)

    def init(self):
        return self
    #
    # def grid(self, under=None, into=None):
    #     """  """
    #     under = under or self.obj
    #     base_name = into or 'grid'
    #     geo = Node(under=under, into=base_name, type='geo')
    #     grid = Node(
    #         under=geo, into='-'.join([base_name, 'grid']),
    #         type='grid')
    #     return grid

    # def line(self, *args, **kwargs):
    #     """ """
    #     kwargs['rows'] = 1
    #     return self.carpet(*args, **kwargs)
    #
    # def get_grid(self, x=None, y=None, **kargs):
    #     """
    #     ::x::
    #     ::y::
    #     """
    #     result = [
    #         self.obj_run(y=n, x=x, **kargs)
    #         for n in range(1, y+1)
    #     ]
    #     return NodeGroup(*result)
    #
    # def obj_run(self, x=None, offset=None, y=1, obj=None, base={}):
    #     """
    #     """
    #     if not base:
    #         base = dict(x=3, y=3, z=3)
    #     assert all([obj, y, x])
    #     row = obj.copy(
    #         # under=Node.create('')# into='row{}'.format(y),
    #         count=x)
    #     # for i, item in enumerate(row):
    #     #     item.node.setParmTransform(hou.hmath.buildTranslate(
    #     #         base['x'] + (i*offset),
    #     #         base['y'] + offset*y,
    #     #         base['z']))
    #     return NodeGroup(*row)

    def load(self, **kwargs):
        """ currrently only supports stl """
        filename = kwargs.pop('filename', None)
        if not filename or not os.path.exists(filename):
            err = 'file {} is missing, cwd is {}'
            err = err.format(filename, os.getcwd())
            self.logger.critical(err)
        into = kwargs.pop('into', 'load')
        parent = Node(into=into, type='geo', **kwargs)
        file = Node(
            under=parent,
            into='{}-file'.format(into),
            type='file')
        file.parm("file").set(filename)
        return parent

    def create_camera(self, xform=None, focus=None, **kwargs):
        """ """
        assert all([focus])
        cam = Node(type='cam', **kwargs)
        if xform:
            cam.node.setParmTransform(xform)
            cam.node.setWorldTransform(
                cam.node.buildLookatRotation(focus.node))
        return cam

    @property
    def units(self):
        units = [
            [0,    0, 0],
            [self.unit, 0, 0],
            [0, self.unit, 0],
            [0, 0, self.unit], ]
        units = map(tuple, units)
        units = map(hou.hmath.buildTranslate, units)
        return units

    def default_cameras(self, focus=None, **kwargs):
        """
        x_cam,  y_cam, z_cam = workspace.default_cameras(unit=8.5)
        """
        units = self.units
        cam_kwargs = dict(focus=focus)
        return [
            self.create_camera(into='o_cam', xform=units[0], **cam_kwargs),
            self.create_camera(into='x_cam', xform=units[1], **cam_kwargs),
            self.create_camera(into='y_cam', xform=units[2], **cam_kwargs),
            self.create_camera(into='z_cam', xform=units[3], **cam_kwargs), ]
    # def poly(self, *points, **kwargs):
    #     """  """
    #     under = kwargs.pop('under', None)
    #     f = under.createPolygon()
    #     vertices = [f.addVertex(p) for p in points]
    #     self.logger.debug(vertices)
    #     return f

    # def bpg(self, m, n, obj=None, interleave=10):
    #     """ """
    #
    #     def duplicate(self, obj=None, copies=1):
    #         """ """
    #         assert obj
    #         raise NotImplementedError()
    #
    #     def line_up(row, interleave):
    #         for i, x in enumerate(row):
    #             x.translate([i*interleave]*3)
    #     row1 = duplicate(obj, copies=m)
    #     row2 = duplicate(obj, copies=n)
    #     row1 = line_up(row1, interleave=interleave)
    #     row2 = line_up(row2, interleave=interleave)
