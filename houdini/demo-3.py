#
"""
Layout workspace and viewports,
Create 3 cameras for perspective views,
Demo Python-native SOPs
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

def py_filter_sop():
    """ filter node (unfinished)
        this should be actually using parent's input geometry, see
        http://www.sidefx.com/docs/houdini/hom/pythonsop.html
    """
    node = hou.pwd()
    geo = node.geometry()
    geo = hou.pwd().geometry()
    for i in range(0, 100):
      pt = geo.createPoint()
      pt.setPosition(hou.Vector3(i * 0.1, 0, 0))
py_filter_sop = node.Node(fxn=py_filter_sop, into='py_filter_sop')

def py_src_sop():
    """ source node """
    node = hou.pwd()
    geo = node.geometry()
    poly = geo.createPolygon()
    for i in range(0, 5, 1):
      for position in map(lambda x: x*i, (0,0,0)), map(lambda x: x*i, (1,0,0)), map(lambda x: x*i, (0,1,0)):
        point = geo.createPoint()
        point.setPosition(position)
        poly.addVertex(point)
    # polyextrude1 parameters - ('depth', 3.0),
    #  ('basenormalx', 1.0),
    #  ('basenormaly', 1.0),
    #  ('basenormalz', 1.0),
    # [(parm.name(),parm.eval()) for parm in hou.node('/obj/code2/extrudevolume1').parms()]
py_src_sop = node.Node(fxn=py_src_sop, into='py_src_sop')


LOGGER.debug("setup cameras")
cams = geo_engine.default_cameras(focus=py_src_sop)
x_cam, y_cam, z_cam = cams

LOGGER.debug("adjust layout for generated objects")
workspace.organize()

LOGGER.debug("useful handles for UI")
vport = workspace.get_viewport()

LOGGER.debug("adjust viewport")
vport.homeAll()

workspace.network_editor.center()

workspace.set_status_msg(__file__)
