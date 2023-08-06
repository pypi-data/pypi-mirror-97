#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "info": "    Show customer info",
    "usage": "   Show API usage: [--start {YYYY-MM-DD}] [--end {YYYY-MM-DD}] [--log|-l] [--breakdown|b]",
    # "billing": " Show billing status",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)
rules.add_optional("usage", {
    "start": ["--start"],
    "end": ["--end"],
})
rules.add_flags("usage", {
    "log": ["--log", "-l"],
    "breakdown": ["--breakdown", "-b"],
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
def me(options):
    """Get customer information, usage and billing"""
    command, options = options
    # print(command, options)

    if command in ["usage"]:
        crud.usage(options)

    # elif command in ["billing"]:
    #     crud.billing(options)

    elif command in ["info"]:
        crud.customer(options)

    # elif command in [":root:"]:
    #     click.echo("Command changed. Please use `tctl me info`")
