#
# import os; execfile(os.path.expanduser('~/code/penrose/houdini/lib.py'))
#
import os, sys

venv = os.environ.get('VIRTUAL_ENV')

if venv:
    print "detected venv, adding to path.."
    lib_dir = os.path.join(venv, 'lib')
    for x in os.listdir(lib_dir):
        path = os.path.join(lib_dir, x, 'site-packages')
        print "  + {}".format(path)
        sys.path.append(path)

from penrose import (hx,)
import hou
import toolutils
import stateutils
import coloredlogs

LOGGER = hx.get_logger(__name__)
LOGGER.debug("logger init completed")
SRC_ROOT = os.environ['SRC_ROOT']
STL_ROOT = os.path.join(SRC_ROOT, 'stl')


# node = hou.pwd()
# geo = node.geometry()
#
# geo1 = hou.Geometry()
#
#
# geo.merge(geo1)
# geo.merge(geo2)

# def addTriangle(geo,  p,  q ,  r):
#     """ create polygon of 3 corners"""
#     f = geo.createPolygon()
#     f.addVertex(p)
#     f.addVertex(q)
#     f.addVertex(r)
#     return f
#


if __name__=='__main__':
    # https://houdinitricks.com/echo-hscript-commands-houdini/
    hou.hscript('commandecho on')
    # create tree
    out = hou.node('/out/')
    obj = hou.node('/obj/')
    geo = hx.load_stl(obj, "./houdini/demo-1.stl")

    # geo.loadFromFile('/Users/matt-admin/code/penrose/stl/compounds/cross-compound-3-spheres.py.scad.stl')
    # ufile = hou.pwd().createNode("file", "boonk", run_init_scripts=False, load_contents=True, exact_type_name=True)
    # hou_parm.lock(False)
    # hou_parm.setAutoscope(False)

    # root.move(hou.Vector2(0, 0))
    workspace = hx.Workspace()
    workspace.technical()
    # geo = create_node(root, 'compound1', type='geo')
    cam1 = hx.create_node(obj, 'cam1', type='cam')
    # cam2 = create_node('cam2', type='cam')
    hx.describe_nodes()


# # https://www.sidefx.com/docs/houdini/hom/hou/getPreference.html
# # hou.getPreferenceNames()
# # hou.item('/obj/cross-compound-3.py.scad')
# def main():
#     default = create_node("default")

# scene_viewer = stateutils.findSceneViewer()
# stl_file = create_node('stl_file')
# stl_file.loadFromFile(os.path.join(
#     STL_ROOT,
#     '/compounds/cross-compound-3.py.scad.stl'))
#     # get_viewport().setCamera(cam)
#     p0 = default.geo.createPoint()
#     p1 = default.geo.createPoint()
#     p2 = default.geo.createPoint()
#     p3 = default.geo.createPoint()
#     p4 = default.geo.createPoint()
#     p0.setPosition((0, 0, 0))
#     p1.setPosition((.5, .5, .5))
#     p2.setPosition((.5, -.5, -.5))
#     p3.setPosition((-.5, .5, -.5))
#     p4.setPosition((-.5, -.5, .5))
#     describe_nodes()
#     # addTriangle(default,  p,  q,  r)
#     addTriangle(default, p0, p1, p2)
#     addTriangle(default, p0, p1, p3)
#     addTriangle(default, p0, p1, p4)
#     addTriangle(default, p0, p2, p3)
#     addTriangle(default, p0, p2, p4)
#     addTriangle(default, p0, p3, p4)
#     describe_nodes()
# main()
