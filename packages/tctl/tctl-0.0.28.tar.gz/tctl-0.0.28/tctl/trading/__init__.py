#!/usr/bin/env python

import click
import sys
from .. import utils
from . import crud


commands = {
    "ls": "  Retreive {cmd} history (optional: --account, --strategy, --status, --start, --end)".format(cmd=sys.argv[0]),
    "list": "Retreive {cmd} history (optional: --account, --strategy, --status, --start, --end)".format(cmd=sys.argv[0])
}

rules = utils.args_actions()
rules.add_optional("list", {
    "account": ["-a", "--account"],
    "strategy": ["-s", "--strategy"],
    "status": ["-statuses"],
    "start": ["--start"],
    "end": ["--end"],
})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def positions(options):
    """Retreive position history with filtering options"""
    command, options = options

    if command in ["ls", "list"]:
        crud.positions_list(options)


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def trades(options):
    """Retreive trade history with filtering options"""
    command, options = options

    if command in ["ls", "list"]:
        crud.trades_list(options)
