""" penrose.hx:
        houdini related code
"""
# import hou
# import toolutils
# import stateutils

from penrose import (util,)

from .framework import Framework
from .geometry import Geometry
from .workspace import Workspace

LOGGER = util.get_logger(__name__)

__all__ = [
    Framework, Geometry, Workspace
]

#
# def get_nodes():
#     return [n for n in hou.node('/').allSubChildren()]
#
#
# def print_tree(node, indent=0):
#     """ """
#     for child in node.children():
#         LOGGER.debug(" " * indent + child.name())
#         print_tree(child, indent + 3)
#
#
# def describe_nodes():
#     print_tree(hou.node('/'))
#     nodes = ["{} ({})".format(n.name(),  n.type().name(), )
#              for n in get_nodes()]
#     # hou.ui.displayMessage('\n'.join(nodes))
#     LOGGER.debug(nodes)
