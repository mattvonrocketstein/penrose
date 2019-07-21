#
"""
"""

import os

import hou
import toolutils
import stateutils

import coloredlogs

## Now that the VENV is ready, more imports are possible
from penrose import (hx, util,)
from penrose.hx.workspace import Workspace
from penrose.hx.geometry import Geometry
from penrose.hx import node

demo_root = os.path.join(os.getcwd(), "houdini")
input_root = os.path.join(demo_root, 'input')
output_root = os.path.join(demo_root, 'output')

LOGGER = util.get_logger(__name__)

## setup framework, workspace, geometry
workspace = Workspace()
workspace.init()
geo_engine = Geometry()

## unpack tree
obj = geo_engine.obj

## load data
stl_file =  os.path.join(input_root, "demo-1.stl")
stl = geo_engine.load(
    filename=stl_file, into='stl',
    under=geo_engine.obj)

rows = geo_engine.get_grid(
    x=3, y=2, obj=stl,
    offset=1.25, )
# geo_engine.bbox(rows[0][0])
# rows = [] \
#     + obj_run(n=1, obj=stl, num_cols=num_cols, offset=offset) \
#     + obj_run(n=2,  obj=stl,num_cols=num_cols, offset=offset)
# bottom = geo_engine.copy_node(stl, into='bottom', count=num_cols)
# [   obj.setParmTransform(hou.hmath.buildTranslate(
#         base['x'] + (-1**i) * (offset*i),
#         base['y'] - offset,
#         base['z']))
#     for i,obj in enumerate(bottom)  ]
# top = geo_engine.copy_node(stl, into='top', count=num_cols)
# [ obj.setParmTransform(hou.hmath.buildTranslate(
#         base['x'] + (-1**i) * (offset*i),
#         base['y'] + offset,
#         base['z']))
#     for i, obj in enumerate(top)  ]

umbrella = node.create(
    under=geo_engine.obj,
    into='umbrella', type='geo')

# rows = top + middle + bottom
# rows = top + bottom
for x, row in enumerate(rows):
    for y, _node in enumerate(row):
        _node.setNextInput(umbrella)
        geo = _node.children()[0].geometry()
        bbox = geo.boundingBox()
        center=bbox.center()
        rows[x][y] = dict(
            node=_node, x=x, y=y,
            center=center)
        # https://www.sidefx.com/docs/houdini/hom/hou/BoundingBox.html https://www.sidefx.com/forum/topic/49734/ https://www.sidefx.com/forum/topic/11472/?page=1#post-54958
        # create points at bounding box corners:
        a = bbox.minvec()
        b = (bbox.minvec()[0], bbox.maxvec()[1], bbox.minvec()[2])
        c = (bbox.maxvec()[0], bbox.maxvec()[1], bbox.minvec()[2])
        d = (bbox.maxvec()[0], bbox.minvec()[1], bbox.minvec()[2])
        e = bbox.maxvec()
        f = (bbox.maxvec()[0], bbox.minvec()[1], bbox.maxvec()[2])
        g = (bbox.minvec()[0], bbox.minvec()[1], bbox.maxvec()[2])
        h = (bbox.minvec()[0], bbox.maxvec()[1], bbox.maxvec()[2])
        corners = [a,b,c,d,e,f,g,h]
        print("corners: {}".format(corners))
        # for i, position in enumerate(corners):
        #     point = node.create(type='geo').children()[0].geometry().createPoint()
        #     point.setPosition(position)

# nx = hou.ObjNode.origin(umbrella)
# umbrella.setParmTransform(
#     hou.hmath.buildTranslate(
#         nx.x(),nx.y(),nx.z()))

umbrella2 = geo_engine.copy_node(
    umbrella, into='umbrella2')

# setup cameras
o_cam, x_cam,  y_cam, z_cam = \
    workspace.default_cameras(unit=10, focus=stl)

stl.destroy()

# adjust layout for generated objects
workspace.organize()

# useful handles for UI
tabs = workspace.tabs()
vport = workspace.get_viewport()

## adjust viewport
vport.homeAll() # vport.setCamera(z_cam.name())
# workspace.python_mode(max=True)
# __file__ is not available inside houdini runtime >:/
workspace.set_status_msg(__file__)

try:
    network_ed = tabs['NetworkEditor']
except KeyError:
    LOGGER.debug("could not resolve `NetworkEditor` tab")
