""" penrose.hx.workspace:
        houdini workspace/ui wrapper
"""
import hou
import toolutils
import stateutils

from penrose import (util,)
from penrose.hx.abcs import HWrapper
from .node import (Node,)

LOGGER = util.get_logger(__name__)


class Workspace(HWrapper):
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
