##
# https://en.wikipedia.org/wiki/Dorothy_Young
##
import os, sys
import hou
import toolutils
import stateutils

def get_logger(name):
    import logging
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel('DEBUG')
    return logger

LOGGER = get_logger(__name__)

class Workspace(object):
    def technical(self):
        self.set_desktop('technical')

    def modeling(self):
        self.set_desktop('modeling')
    model = modeling

    def set_desktop(self, name):
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

def get_viewport():
    scene_view = toolutils.sceneViewer()
    return scene_view.curViewport()

def load_stl(root, filename):
    """  """
    assert os.path.exists(filename),'file {} is missing, cwd is {}'.format(filename, os.getcwd())
    geo = create_node(root, 'geo', type='geo')
    file = create_node(geo, 'file', type='file')
    hou_parm = file.parm("file")
    hou_parm.set(filename)
    return geo

def create_node(root, name,  type='geo'):
    """
    """
    if hou.node('/obj/{}'.format(name)) == None: #
        node = root.createNode(type,  run_init_scripts=False)
        node.setName(name)
        # hou.ui.displayMessage('{} node created!'.format(name))
        LOGGER.debug("created node")
        node.moveToGoodPosition()
        return node
    else:
        item=hou.item('/obj/{}'.format(name))
        msg='`{}` already exists in the scene, returning item {}'.format(name,item)
        # hou.ui.displayMessage(msg)
        LOGGER.debug(msg)
        print msg
        return item
