##
#
##
import logging

from solid.utils import (
    mirror, forward, back, up, down, left, right,
    Black, Blue, Red, Yellow, rotate, scale,
    scad_render, scad_render_to_file)

from solid import (
    cube, sphere,
    union, translate, intersection, linear_extrude, minkowski,
    polygon, color,
    difference, cylinder, OpenSCADObject)

import subprocess
import termcolor
import functools32
bold = functools32.partial(termcolor.colored, attrs=['bold'])

def get_logger(name):
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel('DEBUG')
    return logger

LOGGER=get_logger(__name__)
def indent(txt, level=2):
    """
    """
    return '\n'.join([
        (' ' * level) + line
        for line in txt.split('\n') if line.strip()])
def invoke(cmd=None, stdin='', interactive=False, large_output=False):
    """ replacement for invoke module, which isn't great with pipes """
    LOGGER.debug("running command:\n{}".format(indent(bold(cmd))))
    exec_kwargs = dict(shell=True, )
    if stdin:
        LOGGER.debug("command will receive pipe:\n{}".format(
            blue(indent(stdin))))
        exec_kwargs.update(
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        exec_cmd = subprocess.Popen(cmd, **exec_kwargs)
        exec_cmd.stdin.write(stdin)
        exec_cmd.stdin.close()
        exec_cmd.wait()
    else:
        if not interactive:
            exec_kwargs.update(
                stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE
            )
        exec_cmd = subprocess.Popen(cmd, **exec_kwargs)
        exec_cmd.wait()
    if exec_cmd.stdout:
        exec_cmd.stdout = exec_cmd.stdout.read() if not large_output else '<LargeOutput>'
    else:
        exec_cmd.stdout = '<Interactive>'
    exec_cmd.failed = exec_cmd.returncode > 0
    exec_cmd.succeeded = not exec_cmd.failed
    exec_cmd.success = exec_cmd.succeeded
    exec_cmd.failure = exec_cmd.failed
    return exec_cmd
