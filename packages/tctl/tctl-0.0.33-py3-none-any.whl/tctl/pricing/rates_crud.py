#!/usr/bin/env python

import click
from .. import utils
from .. import remote
from decimal import Decimal
import pandas as pd
import sys

pd.options.display.float_format = '{:,}'.format

commands = {
    "list": "    Retreive currency rates: [--asof {YYYY-MM-DD}]",
    "info": "    Show currency pair exchange rate --pair|-p {PAIR} [--asof {YYYY-MM-DD}]"
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_required("info", {"pair": ["-p", "--pair"]})
rules.add_optional(["list", "ls", "info"], {
    "asof": ["--asof"]
})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def rates_list(options):
    endpoint = "/rates"
    if options.first("asof"):
        date, _ = utils.parse_date(options.first("asof"))
        endpoint = f"/rates/{date}"

    data, _ = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    df = pd.DataFrame(data["rates"], index=['Rate (v. USD)']).T
    df.index.name = "Currency"
    click.echo(f"\nCurrency rates for: {data['date']}")
    click.echo(utils.to_table(df, showindex=True, showheaders=True, floatfmt=".8f"))


def rates_pair(options):
    pair = options.first("pair").upper().replace(':', '')
    if len(pair) == 3:
        pair += "USD"

    if len(pair) != 6:
        click.echo("ERROR: Currency pair needs to be `BASE:QUOTE`")
        sys.exit()

    if pair[:3] == pair[-3:]:
        click.echo(f"\n1 {pair[:3]} = 1 {pair[:3]}")
        return

    endpoint = "/rates/pair/{pair}".format(pair=f"{pair[:3]}:{pair[-3:]}")
    if options.first("asof"):
        date, _ = utils.parse_date(options.first("asof"))
        endpoint += f"/{date}"

    data, _ = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    if data['base'] in ['ETH', 'XRP', 'LTC', 'BTC', 'BCH', 'ZEC', 'EOS', 'BNB', 'ADA']:
        rate = "{:,.8f}".format(Decimal(data['rate']))
    else:
        rate = "{:,.5f}".format(Decimal(data['rate']))

    click.echo(f"\n1 {data['base']} = {rate} {data['quote']}")
    click.echo(f"(as of {data['date']})")
