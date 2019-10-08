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
net_ed = workspace.network_editor
net_ed.maximize()
net_ed.flash_msg("penrose!")

geo_engine = Geometry(unit=10)
hou.session.HEXAGON_RADIUS = geo_engine.unit / 2.0
# https://www.quora.com/How-can-you-find-the-coordinates-in-a-hexagon

def hexagon(r=hou.session.HEXAGON_RADIUS):
    """
    source node SOP,
    this will not get the global context..
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

def hex_module(n, m, name=None, parent=None, r=hou.session.HEXAGON_RADIUS, **kwargs):
    """ """
    import hou
    import math
    from penrose.hx.node import uniq
    name = name or uniq()
    const = (math.sqrt(3) / 2.0)
    _3x5 = node.Node(fxn=hexagon, into=name, parent=parent)
    python1 = _3x5['python1']
    extrude = _3x5.createNode("extrude", 'extrude-{}'.format(name))
    extrude.setParms(depthscale=1)
    extrude.setInput(0, python1)
    copy1 = _3x5.createNode("copyxform", 'copy1-{}'.format(name))
    copy1.setInput(0, extrude)
    tmp=dict({
        'tx': 0,
        'ty': 2*const*hou.session.HEXAGON_RADIUS,
        'ncy': n,
    })
    tmp.update(**kwargs.get('copy1',{}))
    copy1.setParms(tmp)
    copy2 = _3x5.createNode("copyxform", 'copy2-{}'.format(name))
    copy2.setInput(0, copy1)
    tmp = dict({
        'ty': const*hou.session.HEXAGON_RADIUS,
        'tx': (2*hou.session.HEXAGON_RADIUS)* (3.0/4.0) ,
        'ncy': m,
        })
    tmp.update(**kwargs.get('copy2',{}))
    copy2.setParms(tmp)
    color = _3x5.createNode('color')
    color.setInput(0, copy2)
    color.setParms(**kwargs.get('color',{}))
    _3x5.setParms(kwargs.get('parms',{}))
    return _3x5

n, m = 3, 5
# g1 = node.Node(into='g1')
g1 = None

import copy

whole = dict(
    base = [ (n, m),
        dict(name='base', parent=g1,
        color=dict(colorr=0, colorg=0, colorb=1),
        parms=dict(
            tx=-20,  ty=-5, tz=-.5,
            rx=0, ry=0, rz=-30,
            sx=1, sy=1, sz=1.75,
            ))],
    center = [ (3, 5),
        dict(name='center', parent=g1,
        copy1=dict(rz=30),
        copy2=dict(ncy=2, tx=0,tz=.25, sx=.5, sy=.5, sz=.5,),
        color=dict(colorr=0.1, colorg=0.1, colorb=0.1),
        parms=dict(
            sx=.75, sy=.75, sz=.75,
            rx=0, ry=0, rz=150,
            tx=5, ty=8, tz=1,))],
    mod2 = [ (3, 5),
        dict(name='mod2',
        copy2=dict(ncy=2, tx=7.5, ty=4.33, tz=0,  sx=1, sy=1, sz=1,),
        color=dict(colorr=0.937255, colorg=0.937255, colorb=0.937255),
        parms=dict(
            tx=6, ty=-4.86, tz=.8,
            rx=0, ry=0, rz=90,
            sx=1, sy=1, sz=1.2,))],
    mod3 = [ (3, 5),
        dict(name='mod3',
        copy2=dict(ncy=2, tx=7.5, ty=4.3, tz=0,  sx=1, sy=1, sz=1,),
        color=dict(colorr=0.937255, colorg=0.937255, colorb=0.937255),
        parms=dict(
            tx=19, ty=2.6, tz=.8,
            rx=0, ry=0, rz=90,
            sx=1, sy=1, sz=1.2,))],
    left = [ (3, 4),
        dict(name='left',
        copy2=dict(sx=.5, sy=.5, sz=.5,),
        color=dict(colorr=0.5, colorg=0.5, colorb=0.5, colortype=1),
        parms=dict(
            sx=1, sy=1, sz=2,
            rx=0, ry=0, rz=-30,
            tx=-20, ty=-5, tz=1.25,))],
    right = [ (3, 4,),
        dict(name='right',
            copy2=dict(sx=.5, sy=.5, sz=.5,),
            color=dict(colorr=0.5, colorg=0.5, colorb=0.5, colortype=1),
            parms=dict(
                sx=1, sy=1, sz=2,
                rx=0, ry=0, rz=150,
                tx=23.33, ty=10, tz=1.25,),),
        ],
    # _base = [ (n, m),
    #     dict(name='base', parent=g1,
    #     color=dict(colorr=0, colorg=0, colorb=1),
    #     parms=dict(
    #         tx=-20,  ty=-5, tz=-.5,
    #         rx=0, ry=0, rz=-30,
    #         sx=1, sy=1, sz=1.75,
    #         ))],
    # _center1 = [ (3, 5),
    #     dict(name='center', parent=g1,
    #     copy1=dict(rz=30),
    #     copy2=dict(ncy=2, tx=0,tz=.25, sx=.5, sy=.5, sz=.5,),
    #     color=dict(colorr=0.1, colorg=0.1, colorb=0.1),
    #     parms=dict(
    #         sx=.75, sy=.75, sz=.75,
    #         rx=0, ry=0, rz=150,
    #         tx=5, ty=8, tz=1,))],
    # _mod2 = [ (3, 5),
    #     dict(name='mod2',
    #     copy2=dict(ncy=2, tx=7.5, ty=4.33, tz=0,  sx=1, sy=1, sz=1,),
    #     color=dict(colorr=0.937255, colorg=0.937255, colorb=0.937255),
    #     parms=dict(
    #         tx=6, ty=-4.86, tz=.8,
    #         rx=0, ry=0, rz=90,
    #         sx=1, sy=1, sz=1.2,))],
    # _mod3 = [ (3, 5),
    #     dict(name='mod3',
    #     copy2=dict(ncy=2, tx=7.5, ty=4.3, tz=0,  sx=1, sy=1, sz=1,),
    #     color=dict(colorr=0.937255, colorg=0.937255, colorb=0.937255),
    #     parms=dict(
    #         tx=19, ty=2.6, tz=.8,
    #         rx=0, ry=0, rz=90,
    #         sx=1, sy=1, sz=1.2,))],
    # left = [ (3, 4),
    #     dict(name='left',
    #     copy2=dict(sx=.5, sy=.5, sz=.5,),
    #     color=dict(colorr=0.5, colorg=0.5, colorb=0.5, colortype=1),
    #     parms=dict(
    #         sx=1, sy=1, sz=2,
    #         rx=0, ry=0, rz=-30,
    #         tx=-20, ty=-5, tz=1.25,))],
    # right = [ (3, 4,),
    #     dict(name='right',
    #         copy2=dict(sx=.5, sy=.5, sz=.5,),
    #         color=dict(colorr=0.5, colorg=0.5, colorb=0.5, colortype=1),
    #         parms=dict(
    #             sx=1, sy=1, sz=2,
    #             rx=0, ry=0, rz=150,
    #             tx=23.33, ty=10, tz=1.25,),),
    )

for module_name, component in whole.items():
    print 'building module "{}":\n  -> {}'.format(module_name, component)
    args, kargs = component
    whole[module_name] = hex_module(*args, **kargs)

LOGGER.debug("setup cameras")
cams = geo_engine.default_cameras(focus=whole['center'])
x_cam, y_cam, z_cam = cams

LOGGER.debug("adjust layout for generated objects")
workspace.organize()

LOGGER.debug("useful handles for UI")
vport = workspace.get_viewport()

LOGGER.debug("adjust viewport")
vport.homeAll()
workspace.network_editor.center()
workspace.set_status_msg(__file__)
