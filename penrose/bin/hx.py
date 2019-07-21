# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import
from penrose.hx import api as hx_api
from penrose.hx.engine import Engine
import os
import sys

import click
import functools32

import penrose
from penrose import (api, cli, util,)
from penrose.hx.util import get_env
import rpyc
import time

LOGGER = penrose.util.get_logger(__name__)


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

CliWrapper(fxn=api.panic, aliases=['stop'], extra_options=[])
CliWrapper(fxn=hx_api.test, aliases=['test'], extra_options=[])
CliWrapper(
    fxn=hx_api.houdini,
    aliases=['hx'],
    extra_options=[
        cli.options.script,
        cli.args.file,
    ])
