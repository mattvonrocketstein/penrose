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
        self.scene_viewer = self.scene
        self.logger = LOGGER

    def init(self):
        self.technical_layout()
        self.echo_hscript()
        api = self
        return api

    def set_status_msg(self, msg):
        """ """
        hou.ui.setStatusMessage(msg)

    def python_mode(self, max=True):
        """
        """
        tabs = self.get_tabs()
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

    @property
    def scene(self):
        # stateutils.findSceneViewer()
        return toolutils.sceneViewer()

    def get_viewport(self):
        """  """
        return self.scene.curViewport()

    def get_tabs(self):
        """
        """
        out = {}
        for p in self.panes:
            for t in p.tabs():
                out.update({t.type().name(): t})
        return out

    def get_tab(self, type_name):
        """ """
        return self.get_tabs().get(type_name, None)

    def get_tree_tab(self):
        """ """
        return self.get_tab('DataTree')


    def get_network_editor_tab(self):
        """ """
        return self.get_tab('NetworkEditor')

    @property
    def network_editor(self):
        class NetEd(object):
            """
            https://www.sidefx.com/docs/houdini/hom/hou/NetworkEditor.html
            """
            def __init__(himself, pane):
                himself.workspace=self
                himself.pane = pane
                pane.setLocatingEnabled(True)
                # pane.setIsCurrentTab()
                #  highlight in viewer whatever's under mouse in net-editor pane
                pane.homeToSelection()

            def set_max(himself,bool):
                himself.pane.pane().setIsMaximized(bool)
            def maximize(himself): himself.set_max(True)
            def unmaximize(himself): himself.set_max(False)

            def flash_msg(himself, msg, delay=5, img=None):
                """ """
                himself.pane.flashMessage(img, msg, 5)

            def center(himself, *bbox_points, **kwargs):
                default_box = [0, 0, 1, 15]
                bbox_points = bbox_points or default_box
                kwargs = kwargs or dict(transition_time=0.0, max_scale=100)
                himself.workspace.logger.debug('building bbox: {}'.format(bbox_points))
                center = hou.BoundingRect(*bbox_points)
                himself.pane.setVisibleBounds(center, **kwargs)
                himself.pane.redraw()

            def center_search(himself):
                for i in range(15):
                    for j in range(15):
                        for x in range(15):
                            for y in range(15):
                                import time; time.sleep(.5)
                                himself.workspace.logger.debug("trying []".format([i,j,x,y]))
                                himself.center(i,j,x,y)

        return NetEd(self.get_network_editor_tab())

    def get_viewer_tab(self):
        return self.get_tab('OutputViewer')

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

    def technical_layout(self):
        self.set_desktop('technical')

    def modeling_layout(self):
        self.set_desktop('modeling')

    def set_desktop(self, name):
        """ """
        # desktops.keys(): [
        #    'LookDev', 'Technical', 'Terrain', 'Image', 'TOPs',
        #    'Games', 'Build', 'Output', 'Textport', 'Modeling',
        #    'Animate', 'Grooming']
        desktops = dict((i.name().lower(), i) for i in hou.ui.desktops())
        desktops[name].setAsCurrent()
