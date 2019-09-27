##
#
##
import os
import logging

# from solid.utils import (
#     mirror, forward, back, up, down, left, right,
#     Black, Blue, Red, Yellow, rotate, scale,
#     scad_render, scad_render_to_file)
#
# from solid import (
#     cube, sphere,
#     union, translate, intersection, linear_extrude, minkowski,
#     polygon, color,
#     difference, cylinder, OpenSCADObject)

import subprocess
import termcolor
import functools32

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

PY_LEX = PythonLexer()
PY_FMT = TerminalFormatter()

bold = functools32.partial(termcolor.colored, attrs=['bold'])


def hash(msg):
    """ """
    import hashlib
    return hashlib.md5(msg).hexdigest()


def get_logger(name, handler=None):
    handler = handler or logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(process)d] - %(name)s - %(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
        )
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')
    return logger


LOGGER = get_logger(__name__)

# def indent(txt, level=2):
#     """
#     """
#     return '\n'.join([
#         (' ' * level) + line
#         for line in txt.split('\n') if line.strip()])

try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount=2, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount=2, ch=' '):
        return textwrap.indent(text, amount * ch)


def invoke(cmd=None, stdin='', interactive=False, large_output=False, log_command=True, environment={}, log_stdin=True, system=False):
    """
    replacement for invoke module, which isn't great with pipes
    """
    assert isinstance(environment, (dict,)
                      ), 'expected dictionary for environment'
    log_command and LOGGER.info(
        "running command: {}".format(bold(indent(cmd))))
    if system:
        assert not stdin and not interactive
        error = os.system(cmd)

        class result(object):
            failed = failure = bool(error)
            success = succeeded = not bool(error)
            stdout = stdin = '<os.system>'
        return result
    env_string = ["{}='{}'".format(k, v) for k, v in environment.items()]
    env_string = ' '.join(env_string)
    cmd = "{} {}".format(env_string, cmd)
    exec_kwargs = dict(shell=True, )
    if stdin:
        msg = "command will receive pipe:\n{}"
        log_stdin and LOGGER.debug(msg.format(indent(stdin)))
        exec_kwargs.update(
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        exec_cmd = subprocess.Popen(cmd, **exec_kwargs)
        exec_cmd.stdin.write(stdin.encode('utf-8'))
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
        exec_cmd.stdout = '<LargeOutput>' if large_output else exec_cmd.stdout.read().decode('utf-8')
    else:
        exec_cmd.stdout = '<Interactive>'
    if exec_cmd.stderr:
        exec_cmd.stderr = exec_cmd.stderr.read().decode('utf-8')
    exec_cmd.failed = exec_cmd.returncode > 0
    exec_cmd.succeeded = not exec_cmd.failed
    exec_cmd.success = exec_cmd.succeeded
    exec_cmd.failure = exec_cmd.failed
    return exec_cmd

def memoized(fxn):
    """
    memoized/cache decorator for expensive computations
    """
    try:
        return functools.lru_cache(64)(fxn)
    except:
        import backports.functools_lru_cache
        return backports.functools_lru_cache.lru_cache(64)(fxn)

def memoized_property(fxn):
    """ memoized/caching property decorator """
    return property(memoized(fxn))

def highlight_code(code):
    """ """
    return highlight(code, PY_LEX, PY_FMT)



import math

sin = lambda x: math.sin(math.radians(x))
cos = lambda x: math.cos(math.radians(x))

def hexagon(r):
    return [
    (r*cos(0),   r*sin(0),   0),
    (r*cos(60),  r*sin(60),  0),
    (r*cos(120), r*sin(120), 0),
    (r*cos(180), r*sin(180), 0),
    (r*cos(240), r*sin(240), 0),
    (r*cos(300), r*sin(300), 0),]
