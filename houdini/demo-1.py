import os, sys
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    print "detected venv, adding to path.."
    lib_dir = os.path.join(venv, 'lib')
    for x in os.listdir(lib_dir):
        path = os.path.join(lib_dir, x, 'site-packages')
        print "  + {}".format(path)
        sys.path.append(path)

from penrose import (dorothy,util,)
import hou
import toolutils
import stateutils
import coloredlogs

demo_root = os.path.join(os.getcwd(), "houdini")
input_root = os.path.join(demo_root, 'input')
output_root = os.path.join(demo_root, 'output')

LOGGER = util.get_logger(__name__)

## setup workspace
workspace_handle = dorothy.Workspace()
workspace_api = workspace_handle.init()

## setup geometry
geometry_handle = dorothy.Geometry()
htree = geometry_handle.init()

## unpack tree
obj = htree.obj

## load data
stl_file=os.path.join(input_root, "demo-1.stl")
stl = geometry_handle.load(filename=stl_file, into='stl', under=htree.obj)

## setup cameras
x_cam,  y_cam, z_cam = workspace_handle.default_cameras(unit=8.5, focus=stl)

# obj.createNode("geo", "geo1", run_init_scripts=False)
# > <hou.ObjNode of type geo at /obj/geo3>
# > >>> obj.node("geo1").children()
# > (<hou.SopNode of type file at /obj/geo1/file1>,)
# node = dorothy.create_node(obj, 'node', type= 'geo', run_init_scripts=False)
# geo = node.geometry()
# p0 = geo.createPoint()
# p1 = geo.createPoint()
# geo = dorothy.create_node(obj, 'geo', type='geo')
# p2 = geo.createPoint()
# p3 = geo.createPoint()
# p4 = default.geo.createPoint()
# p0.setPosition((0, 0, 0))
# p1.setPosition((.5, .5, .5))
# p2.setPosition((.5, -.5, -.5))
# p3.setPosition((-.5, .5, -.5))
# p4.setPosition((-.5, -.5, .5))




# stl_file.loadFromFile(os.path.join(
#     STL_ROOT,
#     '/compounds/cross-compound-3.py.scad.stl'))
#     # get_viewport().setCamera(cam)
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
# root.move(hou.Vector2(0, 0))
