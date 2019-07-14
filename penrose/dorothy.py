##
# https://en.wikipedia.org/wiki/Dorothy_Young
##
import os, sys

import hou
import toolutils
import stateutils

from penrose import (abcs, util,)

LOGGER = util.get_logger(__name__)
# def api(node):
# g = hou.node('/obj').createNode('geo')
# n = g.createNode(node)
# print n.parms()
# g.destroy()
#
# def api2(node, param):
# g = hou.node('/obj').createNode('geo')
# n = g.createNode(node)
# print n.parm(param).parmTemplate()
# g.destroy()

class HTree(abcs.Loggable):
    def __init__(self, tree, **kwargs):
        self.tree = tree
        self.out = tree['out']
        self.obj = tree['obj']
        Workspace.htree = self

class Geometry(abcs.Loggable):

    def __init__(self, name='default', **kwargs):
        self.name=name
        super(Geometry,self).__init__(name=name,  **kwargs)

    def init(self):
        # load tree
        self.tree = HTree(get_tree())
        return self.tree

    def load(self, under=None, into='load_stl', filename=None):
        """  """
        assert all([under, filename])
        assert os.path.exists(filename),'file {} is missing, cwd is {}'.format(filename, os.getcwd())
        geo = create_node(under=under, into=into, type='geo')
        file = create_node(under=geo, into='{}-file'.format(into), type='file')
        hou_parm = file.parm("file")
        hou_parm.set(filename)
        return geo

    def poly(*points, **kwargs):
        """  """
        under = kwargs.pop('under',None)
        f = under.createPolygon()
        vertices  = [f.addVertex(p) for p in points]
        return f

    def bpg(self, m, n, obj=None, interleave=10):
        """ """
        def duplicate(self, obj=None, copies=1):
            """ """
            assert obj
            raise NotImplementedError()
        def line_up(row, interleave):
            for i,x in enumerate(row):
                x.translate([i*interleave]*3)
        row1 = duplicate(obj, copies=m)
        row2 = duplicate(obj, copies=n)
        row1 = line_up(row1, interleave=interleave)
        row2 = line_up(row2, interleave=interleave)

class Workspace(abcs.Loggable):
    htree =  None
    def __init__(self, **kwargs):
        self.scene_viewer = stateutils.findSceneViewer()

    def  init(self):
        self.technical()
        self.echo_hscript()
        api = self
        return api

    def create_camera(self, into=None, xform=None, under=None, focus=None):
        """ """
        assert all([focus,xform,under])
        cam = create_node(under=under, into=into, type='cam')
        cam.setParmTransform(xform)
        cam.setWorldTransform(cam.buildLookatRotation(focus))
        return cam

    def default_cameras(self, unit=None,  under=None, focus=None):
        """
        x_cam,  y_cam, z_cam = workspace.default_cameras(unit=8.5)
        """
        assert unit
        units = [ [unit, 0, 0],
                  [0, unit, 0],
                  [0, 0, unit], ]
        units = map(tuple, units)
        units = map(hou.hmath.buildTranslate, units)
        under = under or (Workspace.htree and Workspace.htree.obj)
        assert under
        cam_kwargs = dict(under=under, focus=focus)
        return [
            self.create_camera(into='x_cam', xform=units[0], **cam_kwargs),
            self.create_camera(into='y_cam', xform=units[1], **cam_kwargs),
            self.create_camera(into='z_cam', xform=units[2], **cam_kwargs), ]

    @property
    def panes(self):
        '''Return a tuple of all visible panes, regardless of whether or not
           they are attached to a desktop.'''
        # Loop through all the pane tabs and add each tab's pane to the result
        # if it's not already there.  Note that the only way to uniquely
        # identify a pane is using its id.
        ids_to_panes = {}
        for pane_tab in hou.ui.paneTabs():
            pane = pane_tab.pane()
            if pane.id() not in ids_to_panes:
                ids_to_panes[pane.id()] = pane
        return ids_to_panes.values()

    def get_viewport():
        """  """
        scene_view = toolutils.sceneViewer()
        return scene_view.curViewport()

    def set_cam(cam):
        LOGGER.debug("type {}".format(type(cam)))
        return get_viewport().setCamera(cam)

    def echo_hscript(self):
        hou.hscript('commandecho on')

    # def display_msg(msg, **kwargs):
    #     """ """
    #     hou.ui.displayMessage(msg.format(**kwargs))

    def technical(self):
        self.set_desktop('technical')

    def modeling(self):
        self.set_desktop('modeling')
    model = modeling

    def set_desktop(self, name):
        """ """
        # desktops.keys(): ['LookDev', 'Technical', 'Terrain', 'Image', 'TOPs', 'Games', 'Build', 'Output', 'Textport', 'Modeling', 'Animate', 'Grooming']
        desktops = dict((i.name().lower(), i) for i in hou.ui.desktops())
        desktops[name].setAsCurrent()

def get_nodes():
    return [ n for n in hou.node('/').allSubChildren() ]

def print_tree(node, indent=0):
    """ """
    for child in node.children():
        LOGGER.debug(" " * indent + child.name())
        print_tree(child, indent + 3)

def describe_nodes():
    print_tree(hou.node('/'))
    nodes = ["{} ({})".format( n.name(),  n.type().name(), ) for n in get_nodes()]
    # hou.ui.displayMessage('\n'.join(nodes))
    LOGGER.debug(nodes)


def create_node(under=None, into=None,  type='geo', run_init_scripts=True):
    """ """
    assert under and into
    if hou.node('/obj/{}'.format(into)) == None: #
        node = under.createNode(type, run_init_scripts=run_init_scripts)
        node.setName(into)
        LOGGER.debug("created node:  {}".format(into))
        node.moveToGoodPosition()
        return node
    else:
        item=hou.item('/obj/{}'.format(name))
        msg='`{}` already exists in the scene, returning item {}'.format(name,item)
        LOGGER.debug(msg)
        return item

def get_tree():
    # yep, that's not a real tree yet
    return dict(
        out = hou.node('/out/'),
        obj = hou.node('/obj/'))
