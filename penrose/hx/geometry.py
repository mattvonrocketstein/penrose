""" penrose.hx.geometry:
        houdini geometry wrapper
"""
import os
import hou

from penrose import (util,)
from penrose.abcs.hx import Universe
from .node import (create_node,)

LOGGER = util.get_logger(__name__)


class Geometry(Universe):

    def __init__(self, name='default', **kwargs):
        self.name = name
        super(Geometry,  self).__init__(name=name,  **kwargs)

    def init(self):
        return self

    def grid(self, under=None, into=None):
        """  """
        under = under or self.obj
        base_name = into or 'grid'
        geo = create_node(under=under, into=base_name, type='geo')
        grid = create_node(
            under=geo, into='-'.join([base_name, 'grid']), type='grid')
        return grid

    def line(self, *args, **kwargs):
        """ """
        kwargs['rows'] = 1
        return self.carpet(*args, **kwargs)

    def get_grid(self, x=None, y=None, **kargs):
        """
        ::x::
        ::y::
        """
        return [
            self.obj_run(y=n, x=x, **kargs)
            for n in range(1, y+1)
        ]

    def obj_run(self, x=None, offset=None, y=1, obj=None, base={}):
        if not base:
            base = dict(x=3, y=3, z=3)
        assert all([obj, y, x])
        row = self.copy_node(
            obj,
            into='row{}'.format(y),
            count=x)
        for i, item in enumerate(row):
            item.setParmTransform(hou.hmath.buildTranslate(
                base['x'] + (i*offset),
                base['y'] + offset*y,
                base['z']))
        return row

    def copy_node(self, node, into=None, under=None, type='geo', count=1):
        """ FIXME: detect type """
        results = []
        for i in range(count):
            result = hou.copyNodesTo(tuple([node]), self.obj)
            results += list(result)
        for copy in results:
            copy.moveToGoodPosition()
            copy.setName('-'.join([
                into, copy.name()]))
        return results

    def load(self, under=None, into='load', filename=None):
        """ currrently only supports stl """
        assert all([under, filename])
        err = 'file {} is missing, cwd is {}'
        assert os.path.exists(filename), err.format(filename, os.getcwd())
        geo = create_node(under=under, into="{}".format(into), type='geo')
        file = create_node(under=geo, into='{}-file'.format(into), type='file')
        hou_parm = file.parm("file")
        hou_parm.set(filename)
        return geo

    def poly(self, *points, **kwargs):
        """  """
        under = kwargs.pop('under', None)
        f = under.createPolygon()
        vertices = [f.addVertex(p) for p in points]
        self.logger.debug(vertices)
        return f

    def bpg(self, m, n, obj=None, interleave=10):
        """ """

        def duplicate(self, obj=None, copies=1):
            """ """
            assert obj
            raise NotImplementedError()

        def line_up(row, interleave):
            for i, x in enumerate(row):
                x.translate([i*interleave]*3)
        row1 = duplicate(obj, copies=m)
        row2 = duplicate(obj, copies=n)
        row1 = line_up(row1, interleave=interleave)
        row2 = line_up(row2, interleave=interleave)
