#
"""
Layout workspace and viewports,
Create 3 cameras for perspective views,
Demo Python-native SOPs (hexagon)
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
workspace.modeling_layout()
geo_engine = Geometry(unit=10)


# https://www.quora.com/How-can-you-find-the-coordinates-in-a-hexagon
def py_src_sop(r=.5):
    """
    source node.
    as a SOP, this will not get the global context..
    you might need fresh imports here
    """
    import math
    node, geo = hou.pwd(), hou.pwd().geometry()
    poly = geo.createPolygon()
    a,b,c,d,e,f  = [geo.createPoint() for x in 'abcdef']
    sin = lambda x: math.sin(math.radians(x))
    cos = lambda x: math.cos(math.radians(x))
    a.setPosition((r*cos(0),   r*sin(0),   0))
    b.setPosition((r*cos(60),  r*sin(60),  0))
    c.setPosition((r*cos(120), r*sin(120), 0))
    d.setPosition((r*cos(180), r*sin(180), 0))
    e.setPosition((r*cos(240), r*sin(240), 0))
    f.setPosition((r*cos(300), r*sin(300), 0))
    [ poly.addVertex(p) for p in [a,b,c,d,e,f] ]
    poly.setIsClosed(True)
    print poly.normal()
    # polyextrude1 parameters - ('depth', 3.0),
    #  ('basenormalx', 1.0),
    #  ('basenormaly', 1.0),
    #  ('basenormalz', 1.0),
    # [(parm.name(),parm.eval()) for parm in hou.node('/obj/code2/extrudevolume1').parms()]
py_src_sop = node.Node(fxn=py_src_sop, into='py_src_sop')

# LOGGER.debug("setup cameras")
# cams = geo_engine.default_cameras(focus=py_src_sop)
# x_cam, y_cam, z_cam = cams

LOGGER.debug("adjust layout for generated objects")
workspace.organize()

LOGGER.debug("useful handles for UI")
vport = workspace.get_viewport()

LOGGER.debug("adjust viewport")
vport.homeAll()
workspace.network_editor.center()
workspace.set_status_msg(__file__)
