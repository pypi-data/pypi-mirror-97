#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "ls": "    Retreive Tradehooks list",
    "list": "  Retreive Tradehooks list",
    "info": "  Show Tradehook information (via --tradehook|-t <TRADEHOOK-ID>)",
    "new": "   Create new Tradehook",
    "update": "Update existing Tradehook (via --tradehook|-t <TRADEHOOK-ID>)",
    "delete": "Delete Tradehook (via --tradehook|-t <TRADEHOOK-ID>)",
    "rm": "    Delete Tradehook (via --tradehook|-t <TRADEHOOK-ID>)",
    "attach": "Attach/assign Tradehook to strategies (via --tradehook|-t <TRADEHOOK-ID>, optional: --strategy <STRATEGY-ID>)",
    "detach": "Detach/assign Tradehook from strategies (via --tradehook|-t <TRADEHOOK-ID>, optional: --strategy <STRATEGY-ID>)",
}

rules = utils.args_actions()
for command in ["info", "update", "delete", "attach", "detach"]:
    rules.add_required(command, {"tradehook": ["-t", "--tradehook"]})
for command in ["attach", "detach"]:
    rules.add_optional(command, {"strategy": ["-s", "--strategy"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def tradehooks(options):
    """List, create, update, or delete Tradehooks"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.tradehooks_list(options)

    elif command == "info":
        crud.tradehook_info(options)

    elif command == "new":
        crud.tradehook_create(options)

    elif command == "update":
        crud.tradehook_update(options)

    if command in ["rm", "delete"]:
        crud.tradehook_delete(options)

    elif command == "attach":
        crud.tradehook_attach(options)

    elif command == "detach":
        crud.tradehook_detach(options)
