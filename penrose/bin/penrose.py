# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import
from penrose.hx import api as hx_api
import os
import sys

import click
import functools32

import penrose
from penrose import (cli, util,)
import rpyc
import time

LOGGER = penrose.util.get_logger(__name__)


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

CliWrapper(fxn=hx_api.houdini, aliases=['hx'], extra_options=[
    cli.options.script,
    cli.args.file,])

CliWrapper(fxn=hx_api.test, aliases=['hx-test'], extra_options=[])
