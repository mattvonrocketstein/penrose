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

LOGGER = util.get_logger(__file__)

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

LOGGER.debug("building grid from original")
ng1 = node.NodeArray.create_from(
    obj=stl, count=2,
    container=node.Node(into='stl-copies'))
# ng1 = [ stl.copy(into='{}-{}'.format(stl.name, i)) for i in range(2) ]
ng1.map_enum(lambda i,x: x.right(i * 1.25))
ng1.container.right(geo_engine.unit)

ng2 = ng1.copy()
ng2.map_enum(lambda i,x: x.left(i * 1.25))
ng2.container.left(geo_engine.unit)
# opparm
# https://www.sidefx.com/forum/topic/10888/
# [ _node.node.setNextInput(container) for _node in ng1 ]
# ng1.move_under(container)
    # x=3, y=2, obj=stl,
    # offset=1.25, )

# umbrella = Node(into='umbrella')

# ng1.set_input(umbrella)
# umbrella2 = umbrella.copy(into='umbrella2')

LOGGER.debug("setup cameras")
o_cam, x_cam,  y_cam, z_cam = \
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
