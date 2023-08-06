#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "ls": "    Retreive monitors list (optional --strategy|-s <STRATEGY-ID>, --with-id)",
    "list": "  Retreive monitors list (optional --strategy|-s <STRATEGY-ID>, --with-id)",
    "new": "   Create new monitor (optional --strategy|-s <STRATEGY-ID>)",
    "delete": "Delete monitor (via --monitor|-m <MONITOR-ID>)",
    "rm": "    Delete monitor (via --monitor|-m <MONITOR-ID>)",
}

rules = utils.args_actions()
rules.add_optional(["ls", "list", "new"], {"strategy": ["-s", "--strategy"]})
rules.add_flags(["ls", "list"], {
    "ids": ["--with-id"]
})
rules.add_required(["delete", "rm"], {"monitor": ["-m", "--monitor"]})
rules.add_optional("new", {"type": ["-t", "--type"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def monitors(options):
    """List, create, update, or delete monitors"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.monitors_list(options)

    elif command == "new":
        crud.monitor_create(options)

    elif command in ["rm", "delete"]:
        crud.monitor_delete(options)
