""" penrose.hx.node:
        node wrapper for houdini
"""

from penrose import (
    # abcs,
    util,)

import uuid
import hou

LOGGER = util.get_logger(__name__)


def create_node(under=None, into=None,  type='geo', run_init_scripts=True):
    """ """
    under = under or hou.node('/obj')
    into = into or str(uuid.uuid1())
    if hou.node('/obj/{}'.format(into)) is None:
        node = under.createNode(type, run_init_scripts=run_init_scripts)
        node.setName(into)
        LOGGER.debug("created node:  {}".format(into))
        node.moveToGoodPosition()
        return node
    else:
        item = hou.item('/obj/{}'.format(into))
        msg = '`{}` already exists in the scene, returning item {}'.format(
            into, item)
        LOGGER.debug(msg)
        return item


create = create_node