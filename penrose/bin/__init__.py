# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import
import os
import sys

import click
import functools32

import penrose
from penrose import (cli, util,)
from penrose.hx.util import get_env
import rpyc
import time

LOGGER = penrose.util.get_logger(__name__)


from penrose.hx.engine import Engine
ENGINE = Engine()

@click.command(cls=cli.Group)
def main(*args, **kargs):
    """
    ..penrose..
    """
    # this could update global settings here
    # ctx = {}
    # ctx['verbose'] = verbose
    # for key, value in config:
    #     ctx[key] = value
    pass


CliWrapper = functools32.partial(cli.CliWrapper, entry=main,)

def panic(**kwargs):
    """ stop all engines """
    util.invoke(cmd=("ps aux "
                     "| grep -i houdini "
                     "| grep -v grep "
                     "| awk '{print $2}'  "
                     "| xargs -n1 -I% kill -KILL % "
                     "|| true"), system=True)
CliWrapper(fxn=panic, aliases=['stop'], extra_options=[])

def hx_test(file=None, **kwargs):
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
CliWrapper(fxn=hx_test, aliases=['test'], extra_options=[])


# def hx_shell(verbose=False, **kargs):
#     import IPython
#     IPython.embed()
# CliWrapper(
#     fxn=hx_shell,
#     aliases=['shell'],
#     extra_options=[
#         # cli.options.script,
#         # cli.args.file,
#     ])

def houdini(engine=None, file=None, verbose=False, **kargs):
    """
    houdini cli wrapper
    """
    assert os.path.exists(file), 'missing file: {}'.format(file)
    errors = hx_test(file=file)
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
CliWrapper(
    fxn=houdini,
    aliases=['hx'],
    extra_options=[
        cli.options.script,
        cli.args.file,
    ])
