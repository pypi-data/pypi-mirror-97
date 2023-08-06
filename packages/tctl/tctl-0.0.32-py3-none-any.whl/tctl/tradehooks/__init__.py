#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "list": "  Retreive Tradehooks list",
    "info": "  Show Tradehook information: --tradehook|-t {TRADEHOOK_ID}",
    "new": "   Create new Tradehook",
    "update": "Update existing Tradehook: --tradehook|-t {TRADEHOOK_ID}",
    "delete": "Delete Tradehook: --tradehook|-t {TRADEHOOK_ID}",
    "attach": "Attach/assign Tradehook to strategy/ies: --tradehook|-t {TRADEHOOK_ID} [--strategy|-s {STRATEGY_ID}]",
    "detach": "Detach/assign Tradehook from strategy/ies: --tradehook|-t {TRADEHOOK_ID} [--strategy|-s {STRATEGY_ID}]",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

for command in ["info", "update", "patch", "delete", "attach", "detach"]:
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

    elif command in ["update", "patch"]:
        crud.tradehook_update(options)

    if command in ["rm", "delete"]:
        crud.tradehook_delete(options)

    elif command == "attach":
        crud.tradehook_attach(options)

    elif command == "detach":
        crud.tradehook_detach(options)
