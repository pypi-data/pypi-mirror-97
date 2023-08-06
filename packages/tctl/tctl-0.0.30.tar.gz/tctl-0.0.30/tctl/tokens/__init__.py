#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "list": "    Retreive list of active tokens [--decode]",
    "info": "    Show token info: --token|-t {TOKEN_ID}",
    "new": "     Create new token",
    "extend": "  Update token's expiry: --token|-t {TOKEN_ID} [--ttl {SECONDS}]",
    "delete": "  Delete tokens: --token|-t {TOKEN_ID}",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_optional("extend", {"ttl": ["--ttl"]})

for command in ["info", "extend", "delete"]:
    rules.add_required(command, {"token": ["-t", "--token"]})

for command in ["info", "list"]:
    rules.add_flags(command, {"decode": ["--decode"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def tokens(options):
    """List, create, extend, or delete tokens"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.tokens_list(options)

    elif command == "info":
        crud.token_info(options)

    elif command == "new":
        crud.token_create(options)

    elif command == "extend":
        crud.token_extend(options)

    elif command in ["rm", "delete"]:
        crud.token_delete(options)

