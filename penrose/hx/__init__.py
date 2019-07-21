""" penrose.hx:
        houdini related code.
        safe imports here only..
        implementors should import other needed submodules
        directly, anything below this cannot run in a python
        env that's disconnected from the houdini engine
"""
from penrose import (util,)

LOGGER = util.get_logger(__name__)
