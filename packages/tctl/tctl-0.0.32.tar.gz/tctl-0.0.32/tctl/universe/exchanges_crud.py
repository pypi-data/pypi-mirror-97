#!/usr/bin/env python

import click
from .. import utils
from .. import remote
import urllib
from datetime import datetime
import pandas as pd
from decimal import Decimal
pd.options.display.float_format = '{:,}'.format


commands = {
    "list": "    Retreive supported exchange list",
    "info": "    Show exchange information: --exchange|-e {EXCHANGE_MIC}",
    "calendar": "Delete exchange calendar: --exchange|-e {EXCHANGE_MIC} [--start {YYYY-MM-DD}] [--end {YYYY-MM-DD}]",
    "assets": "Show supported assets for exchange: --exchange|-e {EXCHANGE_MIC} [--delisted|-d]",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_required(["info", "assets", "calendar"], {"exchange": ["-e", "--exchange"]})
rules.add_flags("assets", {"delisted": ["-d", "--delisted"]})
rules.add_optional("calendar", {
    "start": ["--start"],
    "end": ["--end"],
})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def exchanges_list(options):
    data, errors = remote.api.get("/exchanges")

    if options.get("raw"):
        click.echo_via_pager(utils.to_json(data))
        return

    df = pd.DataFrame(data)

    df.sort_values("name", inplace=True)
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df))


def exchange_info(options):
    endpoint = "/exchange/{identifier}".format(
        identifier=options.first("exchange").upper())

    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame([data])[:1]

    df['listed_assets'] = "{:,.0f}".format(
        Decimal(df['listed_assets'].astype(str).values[0]))
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))


def exchange_calendar(options):
    exchange = options.first("exchange").upper()
    start, _ = utils.parse_date(
        options.first("start", datetime.now().strftime("%Y-%m-%d")))
    end, _ = utils.parse_date(
        options.first("end", datetime.now().strftime("%Y-%m-%d")))

    start = urllib.parse.quote(start)
    end = urllib.parse.quote(end)
    data, errors = remote.api.get(f"/exchange/{exchange}/calendar/{start}/{end}")

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame(data["calendar"]).T

    del data["calendar"]
    exh_df = pd.DataFrame([data])
    exh_df.columns = [col.replace("_", " ").title()+':' for col in exh_df.columns]
    exh_df = exh_df.T
    exh_df.columns = [""]

    click.echo(utils.to_table(exh_df, showindex=True, tablefmt="plain"))
    click.echo("\nCalendar:")

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    df.index.name = 'Date'
    click.echo(utils.to_table(
        df[["Market Open", "Market Close"]], showindex=True).lstrip())
