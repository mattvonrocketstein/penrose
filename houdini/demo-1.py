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

import logging.handlers
handler = logging.handlers.SysLogHandler(address = ('127.0.0.1', 514))
LOGGER = util.get_logger(__file__,handler=handler)

LOGGER.debug("setup framework, workspace, geometry")
workspace = Workspace()
workspace.init()
geo_engine = Geometry(unit=10)

LOGGER.debug("unpack tree")
tree = geo_engine.tree

LOGGER.debug("load data")
stl_file =  os.path.join(input_root, "demo-1.bstl")
stl = geo_engine.load(filename=stl_file, into='stl')
LOGGER.debug("done loading data")

# LOGGER.debug("building array from object: {}".format(stl))
# ng1 = node.NodeArray.create_from(
#     obj=stl, count=1,
#     container=node.Node(into='stl-copies'))
# ng1.logger.debug("orienting group")
# ng1.map_enum(lambda i, x: x.right(i * 1.25))
# ng1.container.right(geo_engine.unit)

def fxn():
    node = hou.pwd()
    geo = node.geometry()
    geo = hou.pwd().geometry()
    for i in range(0, 100):
      pt = geo.createPoint()
      pt.setPosition(hou.Vector3(i * 0.1, 0, 0))
code1 = node.Node(fxn=fxn, into='code1')

# ng2 = ng1.copy()
# ng2.logger.debug("orienting group")
# ng2.map_enum(lambda i,x: x.left(i * 1.25))
# ng2.container.left(geo_engine.unit)

# opparm
# https://www.sidefx.com/forum/topic/10888/
# [ _node.node.setNextInput(container) for _node in ng1 ]
# ng1.move_under(container)
    # x=3, y=2, obj=stl,
    # offset=1.25, )

LOGGER.debug("setup cameras")
cams = \
    geo_engine.default_cameras(focus=stl)

# stl.destroy()

LOGGER.debug("adjust layout for generated objects")
workspace.organize()

LOGGER.debug("useful handles for UI")
tabs = workspace.tabs()
vport = workspace.get_viewport()

LOGGER.debug("adjust viewport")
vport.homeAll()
# vport.setCamera(z_cam.name())
# workspace.python_mode(max=True)
# __file__ is not available inside houdini runtime >:/
workspace.set_status_msg(__file__)

# try:
#     network_ed = tabs['NetworkEditor']
# except KeyError:
#     LOGGER.debug("could not resolve `NetworkEditor` tab")
