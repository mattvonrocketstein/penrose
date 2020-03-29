#
""" penrose.hx.api
"""
import os

from penrose import (util,)
from penrose.hx.engine import Engine

LOGGER = util.get_logger(__name__)
ENGINE = Engine()


def test(file=None, **kwargs):
    """
    static-analysis for code base
    """
    import penrose
    src_root = os.path.dirname(penrose.__file__)
    demo_root = os.path.join(os.path.dirname(src_root), 'houdini')
    paths = [src_root, demo_root]
    errors=[]
    for path in paths:
        cmd = (
            "find {} "
            "| grep [.]py$ "
            "| xargs -I% bash -x -c '"
            "flake8 % "
            "||exit  255'").format(path)
        file_errs = util.invoke(cmd=cmd)
        if not file_errs.success:
            LOGGER.critical(
                'failed check! file errors follow {}'.format(file_errs.stdout))
            errors.append(file_errs.stdout)
    if errors:
        raise RuntimeError(errors)
        # return errors
        
        
def houdini(engine=None, file=None, verbose=False, **kargs):
    """
    houdini cli wrapper
    """
    assert os.path.exists(file), 'missing file: {}'.format(file)
    ENGINE.init()
    # LOGGER.debug("starting syslog listener")
    # from penrose.bin.pysyslogd import main
    # import multiprocessing
    # proc = multiprocessing.Process(target=main)
    # proc.start()
    # LOGGER.debug("done starting syslog listener")
    
    ENGINE.exec_script(file=file)
    remote_modules = ENGINE.import_remote_modules()
    namespace = locals().copy()
    
    namespace.update(
        conn=ENGINE.conn,
        remote_modules=remote_modules)
    namespace.update(**remote_modules)
    script_namespace = ENGINE.conn.modules.penrose.hx.SCRIPT
    LOGGER.debug("importing `{}`:".format(script_namespace.keys()))
    for k, v in script_namespace.items():
        if k.startswith('_'):
            LOGGER.debug("skipping `{}`:".format(k))
            continue
        # LOGGER.debug("importing `{}`:".format(k))
        # try:
        #     LOGGER.debug("  type={}".format(type(v)))
        #     LOGGER.debug("  val={}".format(v))
        # except:
        #     LOGGER.debug("failed.")
        # else:
        namespace.update({k: v})
    import IPython
    IPython.embed(user_ns=namespace)
    # proc.terminate()
    