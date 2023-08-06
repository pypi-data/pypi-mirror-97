#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "list": "  Retreive orders list: [--account|-a {ACCOUNT_ID}] [--strategy|-s {STRATEGY_ID}] [--status {STATUS}] [--start {DATETIME}] [--end {DATETIME}] [--show-ids]",
    "info": "  Show order information: --order|-o {ORDER_ID}",
    "new": "   Create new order",
    "update": "Update (unfilled) order: --order|-o {ORDER_ID}",
    "delete": "Cancel (unfilled) order: --order|-o {ORDER_ID}",
    "submit": "Submit a (pending) order: --order|-o {ORDER_ID}",
}


rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_optional("new", {"type": ["-t", "--type"]})
rules.add_optional(["list", "ls"], {
    "account": ["-a", "--account"],
    "strategy": ["-s", "--strategy"],
    "status": ["-status"],
    "start": ["--start"],
    "end": ["--end"],
})
rules.add_flags(["ls", "list"], {
    "ids": ["--show-ids"]
})
rules.add_required(["info", "update", "patch", "delete", "rm", "submit"], {
    "order": ["-o", "--order"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def orders(options):
    """List, create, update, or cancel orders"""
    command, options = options

    if command in ["ls", "list"]:
        crud.orders_list(options)

    elif command == "info":
        crud.order_info(options)

    elif command == "new":
        crud.order_create(options)

    elif command in ["update", "patch"]:
        crud.order_update(options)

    elif command in ["rm", "delete"]:
        crud.order_delete(options)

    elif command == "submit":
        crud.order_submit(options)
