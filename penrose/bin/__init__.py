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
import rpyc
import time

LOGGER = penrose.util.get_logger(__name__)

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
import os, sys
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    print "detected venv, adding to path.."
    lib_dir = os.path.join(venv, 'lib')
    for x in os.listdir(lib_dir):
        path = os.path.join(lib_dir, x, 'site-packages')
        print "  + {}".format(path)
        sys.path.append(path)"""

# placeholder
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

# @main.command(name='stl-render', help='show')
# @click.option('--verbose', help='set logger to DEBUG', default=False, is_flag=True)
# @click.option('--size', help='img size', default='1024', required=False)
# # @click.option('-o', '--output-dir', help='output dir', required=False, default=None)
# @click.argument('filename')
# @click.pass_context
# def stl_render(ctx, verbose, size, filename):
#     LOGGER.debug("rendering filename: {}".format(filename))
#     # cmd = '{} -b -P mesh2img.py -- --paths {} --dimensions {} --camera-coords 0.0,0.0,10.0'.format(BLENDER_EXEC, filename, size)
#     # {filepath}_{width}.{ext}
#     util.invoke(cmd)
#     # from stl import mesh
#     # from mpl_toolkits import mplot3d
#     # from matplotlib import pyplot
#     # # Create a new plot
#     # figure = pyplot.figure()
#     # axes = mplot3d.Axes3D(figure)
#     # # Load the STL files and add the vectors to the plot
#     # your_mesh = mesh.Mesh.from_file(filename)
#     # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#     # # Auto scale to the mesh size
#     # scale = your_mesh.points.flatten(-1)
#     # axes.auto_scale_xyz(scale, scale, scale)
#     # # Show the plot to the screen
#     # pyplot.show()
#
#
#
# @main.command(name='stl-rotate', help='rotate')
# @click.option('--verbose', help='set logger to DEBUG', default=False, is_flag=True)
# @click.option('--step', help='step angle', required=False, default='10')
# @click.option('-o', '--output-dir', help='output dir', required=False, default=None)
# @click.argument('filename')
# @click.pass_context
# def stl_rotate(ctx, verbose, step, output_dir, filename):
#     from stl import mesh
#     stl_mesh = mesh.Mesh.from_file(filename)
#     step = int(step)
#     output_dir = output_dir or os.path.join(os.getcwd(),'output')
#     if not os.path.isdir(output_dir):
#         LOGGER.debug("saving to: ".format(output_dir))
#         os.makedirs(output_dir)
#
#     rotation_axises = [0.0, 1.0, 0.0]
#     iterations = int(360.0/step)
#     for i in range(1, iterations):
#         angle = step*i
#         file = os.path.join(output_dir,'angle-{}.stl'.format(angle))
#         LOGGER.debug(" angle {}: saving to {}".format(angle,file) )
#         stl_mesh.rotate(rotation_axises, math.radians(angle))
#         stl_mesh.save(file)


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

def hexec(code, conn=None):
    """
    exec python on the houdini engine
    """
    from penrose.hx import framework
    conn = conn or framework.get_conn()
    code_hash=id(code)
    LOGGER.debug("executing on engine: (sha={})\n{}".format(
        code_hash, util.indent(code)))
    x = conn.execute(code)
    LOGGER.debug("done executing on engine: \n{}".format(
        code_hash))
    return conn

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

def houdini(file=None, verbose=False, **kargs):
    """
    houdini cli wrapper
    """
    assert os.path.exists(file), 'missing file: {}'.format(file)
    errors = hx_test(file=file)
    if any(errors):
        raise RuntimeError(errors)
    result = util.invoke(
        cmd=CMD_BOOTSTRAP,
        system=True,
        environment=get_env())
    hexec(CODE_VENV)
    LOGGER.debug("loading script: {}".format(file))
    conn = hexec(CODE_LOAD_SCRIPT.format(file=file))
    namespace = locals().copy()
    remote_modules = {}
    for name in REMOTE_MODULES:
        LOGGER.debug("retrieving `{}` handle from remote".format(name))
        mod = getattr(conn.modules, name)
        remote_modules.update({name: mod})
        LOGGER.debug("settings sys.modules[{}]={}".format(name, mod))
        sys.modules[name] = mod
    namespace.update(
        conn=conn,
        remote_modules=remote_modules)
    namespace.update(**remote_modules)
    for k, v in conn.modules.penrose.hx.SCRIPT.items():
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
