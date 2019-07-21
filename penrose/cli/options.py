# -*- coding: utf-8 -*-
""" penrose.cli.options """
from __future__ import absolute_import
import click
from functools import partial

debug = click.option(
    '--debug',
    default=False, is_flag=True,
    help='Enables verbose mode.',)

force = click.option(
    '--force',
    default=False, is_flag=True,
    help='Forces action',)

force = click.option(
    '--verbose',
    default=False, is_flag=True,
    help='verbose logging',)

existing_file = click.option('--file', type=click.Path(exists=True))
file_format_partial = partial(click.option,
                              '--format', type=click.Choice(['json', 'yaml', 'yml', 'env']),
                              help='file format', )
file_format = format = file_format_partial(required=True)
file_format_yml_default = file_format_yaml_default = file_format_partial(
    required=False, default='yaml')

script = click.option(
    '--script', '-s', help='Script to run', default='')

command = click.option(
    '--command', '-c', required=False, default='',
    help='Command to run (like bash -c)', )
required_command = click.option(
    '--command', '-c', default='',
    help='Command to run (like bash -c)', )

cascade_partial = partial(
    click.option,
    '--cascade/--no-cascade', '-c/',
    required=False, help='cascading search')
cascade = cascade_partial(default=True)
no_cascade = cascade_partial(default=False)
