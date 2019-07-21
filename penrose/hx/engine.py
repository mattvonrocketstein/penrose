"""
penrose.hx.engine:
"""
import sys
from penrose import (util)
from .abcs  import HWrapper

# placeholder placeholder
CODE_LOAD_SCRIPT = """import os
namespace  = dict(__file__ = '{file}')
execfile('{file}', namespace, namespace)
print 'done with running script @{file}'
from penrose import hx
hx.SCRIPT = namespace
print 'exporting script execution namespace to var `hx.SCRIPT`'
"""

# these will be imported locally after rpyc is setup
REMOTE_MODULES = 'hou hrpyc toolutils stateutils'.split()


class Engine(HWrapper):
    """
    """
    @property
    def conn(self):
        """
        get rpyc connection
        """
        from penrose.hx.framework import get_conn
        if getattr(self, '_conn', None) is None:
            self._conn = get_conn()
        return self._conn

    def import_remote_modules(self):
        """
        import modules from engine runtime into local runtime
        """
        remote_modules = {}
        for name in REMOTE_MODULES:
            self.logger.debug("retrieving `{}` handle from remote".format(name))
            mod = getattr(self.conn.modules, name)
            remote_modules.update({name: mod})
            self.logger.debug("settings sys.modules[{}]={}".format(name, mod))
            sys.modules[name] = mod
        return remote_modules
        
    def exec_script(self, file=None, **kwargs):
        """
        exec script in the houdini engine
        """
        self.logger.debug("loading script: {}".format(file))
        return self.exec_code(
            CODE_LOAD_SCRIPT.format(file=file),
            **kwargs)

    def exec_code(self, code, conn=None):
        """
        exec python on the houdini engine
        """
        conn = conn or self.conn
        code_hash = id(code)
        self.logger.debug("executing on engine: (sha={})\n{}".format(
            code_hash, util.indent(code)))
        x = conn.execute(code)
        self.logger.debug(
            "done executing on engine: \n{}".format(code_hash))
        return conn
