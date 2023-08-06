#!/usr/bin/env python

import click
from .. import utils
from .. import remote
import pandas as pd
pd.options.display.float_format = '{:,}'.format


commands = {
    "list": "Retreive supported brokers list",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def brokers_list(list=None, ls=None, raw=False):
    """List supported brokers list"""
    data, errors = remote.api.get("/brokers")

    if raw:
        click.echo(utils.to_json(data, errors))
        return

    click.echo(utils.to_table(data))
