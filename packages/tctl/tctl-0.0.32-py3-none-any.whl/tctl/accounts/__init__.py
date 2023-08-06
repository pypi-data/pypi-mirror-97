#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "list": "Retreive accounts list",
    "info": "Show account information: --account|-a {ACCOUNT_ID}",
    "new": "Create new account",
    "update": "Update existing account: --account|-a {ACCOUNT_ID}",
    "delete": "Delete account: --account|-a {ACCOUNT_ID}",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

for command in ["info", "update", "patch", "delete"]:
    rules.add_required(command, {"account": ["-a", "--account"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def accounts(options):
    """List, create, update, or delete broker accounts"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.accounts_list(options)

    elif command == "info":
        crud.account_info(options)

    elif command == "new":
        crud.account_create(options)

    elif command in ["update", "patch"]:
        crud.account_update(options)

    elif command in ["rm", "delete"]:
        crud.account_delete(options)
