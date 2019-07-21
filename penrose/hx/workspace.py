""" penrose.hx.workspace:
        houdini workspace/ui wrapper
"""
import hou
import toolutils
import stateutils

from penrose import (util,)
from penrose.abcs.hx import Universe
from .node import (create_node,)

LOGGER = util.get_logger(__name__)


class Workspace(Universe):
    def __init__(self, **kwargs):
        self.scene_viewer = stateutils.findSceneViewer()

    def init(self):
        self.technical()
        self.echo_hscript()
        api = self
        return api

    def set_status_msg(self, msg):
        """ """
        hou.ui.setStatusMessage(msg)

    def python_mode(self, max=True):
        """
        """
        tabs = self.tabs()
        tabs['PythonShell'].setIsCurrentTab()
        if max:
            tabs['PythonShell'].pane().setIsMaximized(True)
        return tabs['PythonShell']

    def organize(self):
        """
        """
        return self.obj.layoutChildren()

    def create_camera(self, into=None, xform=None, under=None, focus=None):
        """ """
        assert all([focus, xform, under])
        cam = create_node(under=under, into=into, type='cam')
        cam.setParmTransform(xform)
        cam.setWorldTransform(cam.buildLookatRotation(focus))
        return cam

    def default_cameras(self, unit=None,  under=None, focus=None):
        """
        x_cam,  y_cam, z_cam = workspace.default_cameras(unit=8.5)
        """
        assert unit
        units = [
            [0,    0, 0],
            [unit, 0, 0],
            [0, unit, 0],
            [0, 0, unit], ]
        units = map(tuple, units)
        units = map(hou.hmath.buildTranslate, units)
        under = under or self.obj
        assert under
        cam_kwargs = dict(under=under, focus=focus)
        return [
            self.create_camera(into='o_cam', xform=units[0], **cam_kwargs),
            self.create_camera(into='x_cam', xform=units[1], **cam_kwargs),
            self.create_camera(into='y_cam', xform=units[2], **cam_kwargs),
            self.create_camera(into='z_cam', xform=units[3], **cam_kwargs), ]

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

    def get_viewport(self):
        """  """
        scene_view = toolutils.sceneViewer()
        return scene_view.curViewport()

    def tabs(self):
        """
        """
        out = {}
        for p in self.panes:
            for t in p.tabs():
                out.update({t.type().name(): t})
        return out

    def set_cam(self,  cam):
        """  """
        LOGGER.debug("type {}".format(type(cam)))
        return self.get_viewport().setCamera(cam)

    def echo_hscript(self):
        """  """
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
        # desktops.keys(): [
        #    'LookDev', 'Technical', 'Terrain', 'Image', 'TOPs',
        #    'Games', 'Build', 'Output', 'Textport', 'Modeling',
        #    'Animate', 'Grooming']
        desktops = dict((i.name().lower(), i) for i in hou.ui.desktops())
        desktops[name].setAsCurrent()
