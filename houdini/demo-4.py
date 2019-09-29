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
hou.session.HEXAGON_RADIUS = geo_engine.unit / 2.0
# https://www.quora.com/How-can-you-find-the-coordinates-in-a-hexagon

def hexagon(r=hou.session.HEXAGON_RADIUS):
    """
    source node.
    as a SOP, this will not get the global context..
    you might need fresh imports here
    """
    from penrose import util
    node, geo = hou.pwd(), hou.pwd().geometry()
    poly = geo.createPolygon()
    a, b, c, d, e, f  = [ geo.createPoint() for x in 'abcdef' ]
    for i, point in enumerate([a, b, c, d, e, f]):
        point.setPosition(util.hexagon(r)[i])
        poly.addVertex(point)
    poly.setIsClosed(True)

def hex_module(n, m, r=hou.session.HEXAGON_RADIUS):
    """ """
    import math
    const = (math.sqrt(3) / 2.0)
    _3x5 = node.Node(fxn=hexagon, into='_3x5')
    python1 = _3x5['python1']
    extrude = _3x5.createNode("extrude", "extrude")
    extrude.setParms(depthscale=1)
    extrude.setInput(0, python1)
    copy1 = _3x5.createNode("copyxform", "copy1")
    copy1.setInput(0, extrude)
    copy1.setParms(dict({
        'tx': 0,
        'ty': 2*const*hou.session.HEXAGON_RADIUS,
        'ncy': n,
    }))
    copy2 = _3x5.createNode("copyxform", "copy2")
    copy2.setInput(0, copy1)
    copy2.setParms(dict({
        'ty': const*hou.session.HEXAGON_RADIUS,
        'tx': (2*hou.session.HEXAGON_RADIUS)* (3.0/4.0) ,
        'ncy': m,}))
    return _3x5

mod1 = hex_module(3, 5)
# bbox = mod1.bbox()
mod1.setParms(rz=30)
# mod1.setParms(rx=HEXAGON_RADIUS)
# print mod1.parms

LOGGER.debug("setup cameras")
cams = geo_engine.default_cameras(focus=mod1)
x_cam, y_cam, z_cam = cams

LOGGER.debug("adjust layout for generated objects")
workspace.organize()

LOGGER.debug("useful handles for UI")
vport = workspace.get_viewport()

LOGGER.debug("adjust viewport")
vport.homeAll()
workspace.network_editor.center()
workspace.set_status_msg(__file__)
