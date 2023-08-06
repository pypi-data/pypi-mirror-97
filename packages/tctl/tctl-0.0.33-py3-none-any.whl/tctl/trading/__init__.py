#!/usr/bin/env python

import click
import sys
from .. import utils
from . import crud


try:
    command = sys.argv[1]
except:
    command = ""
commands = {
    "ls": "  Retreive " + command + " history: [--account|-a {ACCOUNT_ID}] [--strategy|-s {STRATEGY_ID}] [--start {DATETIME}] [--end {DATETIME}]",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)
rules.add_optional("list", {
    "account": ["-a", "--account"],
    "strategy": ["-s", "--strategy"],
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
