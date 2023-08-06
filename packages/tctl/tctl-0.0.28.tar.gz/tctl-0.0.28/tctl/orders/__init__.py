#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "ls": "    Retreive orders list (optional --strategy|-s <STRATEGY-ID>, --with-id)",
    "list": "  Retreive orders list (optional --strategy|-s <STRATEGY-ID>, --with-id)",
    "info": "  Show order information (via --order|-o <ORDER-ID>)",
    "new": "   Create new order",
    "update": "Update existing order (via --order|-o <ORDER-ID>)",
    "delete": "Delete (cancel) order (via --order|-o <ORDER-ID>)",
    "rm": "    Delete (cancel) order (via --order|-o <ORDER-ID>)",
    "submit": "Submit a (pending) order (via --order|-o <ORDER-ID>)",
}

rules = utils.args_actions()
rules.add_optional("new", {"type": ["-t", "--type"]})
rules.add_optional(["list", "ls"], {
    "account": ["-a", "--account"],
    "strategy": ["-s", "--strategy"],
    "status": ["-statuses"],
    "start": ["--start"],
    "end": ["--end"],
})
rules.add_flags(["ls", "list"], {
    "ids": ["--with-id"]
})
rules.add_required(["info", "update", "delete", "rm", "submit"], {
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

    elif command == "update":
        crud.order_update(options)

    elif command in ["rm", "delete"]:
        crud.order_delete(options)

    elif command == "submit":
        crud.order_submit(options)
