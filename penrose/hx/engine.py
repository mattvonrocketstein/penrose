"""
penrose.hx.engine:
"""
import os
import sys
from penrose import (util,)
from penrose.hx import util as hx_util
from .abcs import HWrapper

# placeholder placeholder
CODE_LOAD_SCRIPT = """import os
namespace  = dict(__name__='{file}', __file__ = '{file}')
execfile('{file}', namespace, namespace)
print 'done with running script @{file}'
from penrose import hx
hx.SCRIPT = namespace
print 'exporting script execution namespace to var `hx.SCRIPT`'
"""

# these will be imported locally after rpyc is setup
REMOTE_MODULES = 'hou hrpyc toolutils stateutils'.split()

# minimal bash script to create a minimal houdini script
# which will open up the engine to some remote control
CMD_BOOTSTRAP = (
    'echo "import hrpyc; hrpyc.start_server(use_thread=True, quiet=False)"'
    '> .tmp.py ; houdini waitforui .tmp.py&')

# minimal bootstrap code to make the remote engine
# respect the same virtualenv as this runtime does.
CODE_VENV = """## This code is run by houdini, which knows VIRTUAL_ENV via
## env-vars, but does not by default honor it.  We need to setup
## the path to use VENV libraries
import hou
import os, sys
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    print "detected venv, adding to path.."
    lib_dir = os.path.join(venv, 'lib')
    for x in os.listdir(lib_dir):
        path = os.path.join(lib_dir, x, 'site-packages')
        print "  + {}".format(path)
        sys.path.append(path)"""

class Engine(HWrapper):
    """ """

    def init(self):
        """ """
        def get_env():
            """ """
            ENV = dict(
                HFS='/Applications/Houdini/Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources',
                # HOUDINI_DESKTOP_DIR = os.path.expanduser('~/Desktop'),
                HOUDINI_DESKTOP_DIR=os.path.expanduser('/tmp'),
                HOUDINI_OS='MacOS',
                HOUDINI_TEMP_DIR='/tmp/houdini_temp',
                HOUDINI_USER_PREF_DIR=os.path.expanduser(
                    '~/Library/Preferences/houdini/17.5'),
                BLBIN='/Applications/Blender/blender.app/Contents/MacOS/',
            )
            ENV.update(
                HSITE=os.path.join(ENV['HFS'], "site"),
                HBIN=os.path.join(ENV['HFS'], "bin"),
            )
            used_defaults = []
            for var_name, default in ENV.items():
                if var_name in os.environ:
                    msg = "var `{}` is present in env, using value: '{}'"
                    ENV[var_name] = os.environ[var_name]
                    self.logger.debug(msg.format(var_name, ENV[var_name]))
                else:
                    used_defaults.append(var_name)
                    msg = "var `{}` is missing from env, using default: '{}'"
                    self.logger.debug(msg.format(var_name, ENV[var_name]))
            if used_defaults:
                self.logger.warning(
                    "defaults were used for all of {}, "
                    "this probably isn't right for your setup..".format(used_defaults))
            ENV.update(
                PATH="{}:{}:{}".format(
                    os.environ['PATH'],
                    ENV["HBIN"], ENV["BLBIN"],)
            )
            return ENV
        result = util.invoke(
            cmd=CMD_BOOTSTRAP,
            system=True,
            environment=get_env())
        self.exec_code(CODE_VENV)

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
            self.logger.debug(
                "retrieving `{}` handle from remote".format(name))
            mod = getattr(self.conn.modules, name)
            remote_modules.update({name: mod})
            self.logger.debug("settings sys.modules[{}]={}".format(name, mod))
            sys.modules[name] = mod
        return remote_modules

    def exec_script(self, file=None, **kwargs):
        """
        exec script in the houdini engine
        """
        from penrose.util import highlight_code
        self.logger.debug("loading script: {}".format(file))
        return self.exec_code(
            CODE_LOAD_SCRIPT.format(file=file),
            **kwargs)

    def exec_code(self, code, conn=None):
        """
        exec python on the houdini engine
        """
        conn = conn or self.conn
        code_hash = util.hash(code)
        self.logger.debug("executing on engine: (sha={})\n{}".format(
            code_hash, util.indent(util.highlight_code(code))))
        x = conn.execute(code)
        self.logger.debug(
            "done executing on engine: {}".format(code_hash))
        return conn
