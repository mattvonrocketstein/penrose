# -*- coding: utf-8 -*-
""" penrose.cli.args: Common CLI arguments for reuse """
from __future__ import absolute_import
import click

file = click.argument('file', nargs=1)
