# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import
import os

import click
import functools32

import penrose
from penrose import (cli, util,)

LOGGER = penrose.util.get_logger(__name__)
# import os, math
# from collections import defaultdict, OrderedDict
#
# import click
#
# from penrose import util
#
# LOGGER = util.get_logger(__name__)
#
# from penrose import cli
# @click.group()
# # @click.command()
# def main(ctx):
#     # this could update global settings here
#     # ctx = {}
#     # ctx['verbose'] = verbose
#     # for key, value in config:
#     #     ctx[key] = value
#     pass
#
#
# BLENDER_EXEC = os.environ.get('BLENDER', '/Applications/Blender/blender.app/Contents/MacOS/blender')
#
# @main.command(name='houdini', help='show', cls=cli.Group)
# # @click.option('--verbose', help='set logger to DEBUG', default=False, is_flag=True)
# # @click.option('--size', help='img size', default='1024', required=False)
# # # @click.option('-o', '--output-dir', help='output dir', required=False, default=None)
# @click.argument('filename')
# def houdini(filename, verbose=False, ):
#     pass
#
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

ENV = dict(
    HFS = '/Applications/Houdini/Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources',
    # HOUDINI_DESKTOP_DIR = os.path.expanduser('~/Desktop'),
    HOUDINI_DESKTOP_DIR = os.path.expanduser('/tmp'),
    HOUDINI_OS = 'MacOS',
    HOUDINI_TEMP_DIR = '/tmp/houdini_temp',
    HOUDINI_USER_PREF_DIR = os.path.expanduser('~/Library/Preferences/houdini/17.5'),
    HSITE = "/Applications/Houdini/Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/site",
    HBIN='/Applications/Houdini//Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/bin',
    BLBIN='/Applications/Blender/blender.app/Contents/MacOS/',
)
ENV.update(
    PATH="{}:{}:{}".format(os.environ['PATH'], ENV["HBIN"], ENV["BLBIN"],)
)

LOGGER.debug("hacked up env: {}".format(ENV))

def panic(**kwargs):
    util.invoke("""ps aux
    	| grep -i houdini
    	| grep -v grep
    	| awk '{print $$2}'
    	| xargs -n1 -I% echo kill -KILL %
    	|| true""")

def houdini(file=None, verbose=False, **kargs):
    """ houdini wrapper """
    assert os.path.exists(file),'missing file: {}'.format(file)
    # missing = sum([
    #     0 if not os.environ.get(name, None) else 1
    #     for name in env_vars ] )
    # if missing:
    #     err = "Required env-vars are empty: {}"
    #     LOGGER.warning(err.format(""))
    #     err = "(Not sure how to guess these values for {})"
    #     LOGGER.warning(err.format(sys.platform))
    cmd =  """flake8 {file} | grep 'Error\|E112'""".format(file=file)
    file_errs = util.invoke(
        cmd=cmd,
        # system=True,
        )
    if file_errs.success:
        LOGGER.critical('failed check! file errors follow {}'.format(file_errs.stdout))
        return  None
    else:
        cmd = """houdini -desktop Technical waitforui {file}""".format(file=file)
        return util.invoke  (cmd=cmd,  environment=ENV)

_test = CliWrapper(
    fxn=houdini,
    aliases=['hx'],
    extra_options=[
        cli.options.script,
        cli.args.file,
    ])
