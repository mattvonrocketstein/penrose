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
workspace.technical_layout()
workspace.network_editor.maximize()
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

# https://www.quora.com/How-can-you-find-the-coordinates-in-a-hexagon
def py_src_sop(r=3):
    """ source node """
    node = hou.pwd()
    geo = node.geometry()
    poly = geo.createPolygon()
    a.setPosition((r, 0, 0))
    d.setPosition((-r, 0, 0))
    b.setPosition((r*cos(60), r*sin(60), 0))
    c.setPosition((r*cos(120), r*sin(120), 0))
    e.setPosition((r*cos(240), r*sin(240), 0))
    f.setPosition((r*cos(300), r*sin(300), 0))
    [ poly.addVertex(p) for p in [a,b,c,d,e,f] ]
    poly.setIsClosed()
    print poly.normal()
    # polyextrude1 parameters - ('depth', 3.0),
    #  ('basenormalx', 1.0),
    #  ('basenormaly', 1.0),
    #  ('basenormalz', 1.0),
    # [(parm.name(),parm.eval()) for parm in hou.node('/obj/code2/extrudevolume1').parms()]

def py_src_sop():
    # https://wordpress.discretization.de/houdini/home/advanced-2/python/
    node = hou.pwd()
    geo = node.geometry()

    # create 4 points and remember their names
    p0 = geo.createPoint()
    p1 = geo.createPoint()
    p2 = geo.createPoint()
    p3 = geo.createPoint()
    p4 = geo.createPoint()

    import math
    o = geo.createPoint()
    a, d = geo.createPoint(), geo.createPoint()
    b, c = geo.createPoint(), geo.createPoint()
    f, e = geo.createPoint(), geo.createPoint()
    cos = lambda x: math.cos(math.radians(x))
    sin = lambda x: math.cos(math.radians(x))

    # edit their position values
    p0.setPosition((0,0,0))
    p1.setPosition((.5,.5,.5))
    p2.setPosition((.5,-.5,-.5))
    p3.setPosition((-.5,.5,-.5))
    p4.setPosition((-.5,-.5,.5))

    # define a funciton to create triangels
    def addTriangle(p,q,r):
     # create polygon of 3 corners
     f = geo.createPolygon()
     f.addVertex(p)
     f.addVertex(q)
     f.addVertex(r)

    # create triangles inbetween the points
    # addTriangle(p0,p1,p2)
    addTriangle(p0,a,b)
    # addTriangle(p0,p1,p3)
    # addTriangle(p0,p1,p4)
    # addTriangle(p0,p2,p3)
    # addTriangle(p0,p2,p4)
    # addTriangle(p0,p3,p4)
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
workspace.network_editor.unmaximize()
workspace.network_editor.center()
workspace.set_status_msg(__file__)
