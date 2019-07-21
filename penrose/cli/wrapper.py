""" penrose.cli.wrapper
"""
from __future__ import absolute_import
import functools

import click

from penrose import (abcs, util,)

LOGGER = util.get_logger(__name__)


class CliWrapper(abcs.Loggable):
    """
    a wrapper that turns a API function into a click CLI subcommand
    """

    def __init__(self, fxn=None, command_name=None, subcommand_name=None, extra_options=None, aliases=[], help=None, entry=None):
        self.entry = entry
        self.aliases = aliases
        self.is_subcommand = isinstance(self.entry, (click.core.Group,))
        self.is_stand_alone = self.entry is None
        self.subcommand_name = self.name = subcommand_name or \
            fxn.__name__.replace('_', '-')
        self.command_name = command_name
        self.fxn = fxn
        self.extra_options = extra_options
        default_help = 'no docstring'
        self.help = help or getattr(
            fxn, '__doc__', default_help) or default_help
        self.help = self.help.strip()
        self.proxy = self.get_proxy()
        if not callable(self.proxy):
            err = "Expected callable for proxy, got '{}'".format(self.proxy)
            raise ValueError(err)
        if not (self.is_subcommand or self.is_stand_alone):
            err = (
                'expected a group or a standalone '
                'command, got {} of type {} for entry')
            err = err.format(self.entry, type(self.entry))
            raise ValueError(err)
        super(CliWrapper, self).__init__()

    def get_proxy(self):
        """ """
        from penrose import cli
        BASE_OPTIONS = [
            # every command gets the --debug option
            cli.options.debug,
        ]
        options = self.extra_options
        if self.is_subcommand:
            # otherwise base options would be added twice for stand-alone style CLIs
            options += BASE_OPTIONS

        @functools.wraps(self.fxn)
        def proxy(*args, **kwargs):
            """ """
            # if args and isinstance(args[0],(click.core.Context,)):
            #     # none of the api commands are anticipating the click context
            #     args = args[1:]
            args = [x for x in args if not isinstance(
                x, (click.core.Context,))]
            LOGGER.debug("proxying args={}, kwargs={}".format(args, kwargs))
            api_result = self.fxn(*args, **kwargs)
            LOGGER.debug("api result: {}".format(api_result))
            # trigger_event(fxn, api_result)
            # return?
        for option in options:
            proxy = option(proxy)
        if self.is_subcommand:
            if self.aliases:
                return self.entry.command(
                    name=self.name, help=self.help,
                    aliases=self.aliases)(proxy)
            else:
                return self.entry.command(
                    name=self.name, help=self.help)(proxy)
        elif self.entry is None:
            return click.command()(proxy)
        else:
            err = "unknown Entry type '{}' for '{}'".format(
                type(self.entry), self.entry)
            LOGGER.critical(err)
            raise RuntimeError(err)
