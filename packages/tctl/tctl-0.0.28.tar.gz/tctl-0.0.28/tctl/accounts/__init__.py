#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "ls": "    Retreive accounts list",
    "list": "  Retreive accounts list",
    "info": "  Show account information (via --account|-a <ACCOUNT-ID>)",
    "new": "   Create new account",
    "update": "Update existing account (via --account|-a <ACCOUNT-ID>)",
    "delete": "Delete account (via --account|-a <ACCOUNT-ID>)",
    "rm": "    Delete account (via --account|-a <ACCOUNT-ID>)"
}

rules = utils.args_actions()

for command in ["info", "update", "delete"]:
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

    elif command == "update":
        crud.account_update(options)

    elif command in ["rm", "delete"]:
        crud.account_delete(options)
