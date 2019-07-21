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
    def test_file(fname):
        cmd = """flake8 {file} | grep 'Error\|E112'""".format(file=fname)
        file_errs = util.invoke(
            cmd=cmd,
            # system=True,
        )
        if file_errs.success:
            LOGGER.critical(
                'failed check! file errors follow {}'.format(file_errs.stdout))
            return file_errs.stdout
    checklist = ['penrose/hx/*py']
    checklist += ([] if file is None else [file])
    errors = [test_file(x) for x in checklist]
    return errors


def houdini(engine=None, file=None, verbose=False, **kargs):
    """
    houdini cli wrapper
    """
    assert os.path.exists(file), 'missing file: {}'.format(file)
    errors = test(file=file)
    if any(errors):
        raise RuntimeError(errors)
    ENGINE.init()
    ENGINE.exec_script(file=file)
    remote_modules = ENGINE.import_remote_modules()
    namespace = locals().copy()

    namespace.update(
        conn=ENGINE.conn,
        remote_modules=remote_modules)
    namespace.update(**remote_modules)
    for k, v in ENGINE.conn.modules.penrose.hx.SCRIPT.items():
        LOGGER.debug("importing `{}`:".format(k))
        try:
            LOGGER.debug("  type={}".format(type(v)))
            LOGGER.debug("  val={}".format(v))
        except:
            LOGGER.debug("failed.")
        else:
            namespace.update({k:v})
    import IPython; IPython.embed(user_ns=namespace)
