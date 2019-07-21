""" penrose.hx.framework:
        houdini framework wrapper
"""
# import toolutils,stateutils,

import time

import rpyc

from penrose import (util,)
from penrose.hx.abcs import HWrapper

LOGGER = util.get_logger(__name__)


def get_conn():
    """
    rpyc connection to the houdini engine
    """
    conn, count = None, 0
    while conn is None and count < 100:
        LOGGER.debug("attempting to connect to engine")
        try:
            conn = rpyc.classic.connect("127.0.0.1", port=18811)
        except (Exception,) as exc:
            count += 1
            LOGGER.debug(str(exc))
            time.sleep(count)
        else:
            LOGGER.debug("established connection to engine: {}".format(conn))
    if not conn:
        raise Exception('no conn')
    return conn


class Framework(HWrapper):

    def init(self):
        """ """
        # deprecated
        import hrpyc
        hrpyc.start_server(use_thread=True, quiet=False)
