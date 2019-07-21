"""
"""
import os
from penrose import (util,)

LOGGER = util.get_logger(__name__)

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
            LOGGER.debug(msg.format(var_name, ENV[var_name]))
        else:
            used_defaults.append(var_name)
            msg = "var `{}` is missing from env, using default: '{}'"
            LOGGER.debug(msg.format(var_name, ENV[var_name]))
    if used_defaults:
        LOGGER.warning(
            "defaults were used for all of {}, "
            "this probably isn't right for your setup..".format(used_defaults))
    ENV.update(
        PATH="{}:{}:{}".format(
            os.environ['PATH'],
            ENV["HBIN"], ENV["BLBIN"],)
    )
    return ENV
