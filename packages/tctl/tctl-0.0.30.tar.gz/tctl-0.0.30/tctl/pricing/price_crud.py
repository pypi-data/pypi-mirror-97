#!/usr/bin/env python

import click
from .. import utils
from .. import remote
from datetime import datetime
from decimal import Decimal
import sys

import pandas as pd
pd.options.display.float_format = '{:,}'.format


commands = {
    "last": "    Show asset information: --asset|-a {ASSET} [--asof {DATETIME}]",
    "quote": "   Show asset information: --asset|-a {ASSET}",
    "check": "   Show asset information: --asset|-a {ASSET} --rule|-r {RULE} --start {YYYY-MM-DD} [--end {YYYY-MM-DD}] [--unadjusted|-u]",
    "bar": "     Show asset information: --asset|-a {ASSET} [--start {YYYY-MM-DD}] [--end {YYYY-MM-DD}]",
    "bars": "    Show asset information",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_required(["last", "quote"], {"asset": ["-a", "--asset"]})
rules.add_optional(["last"], {
    "asof": ["--asof"]
})
rules.add_required(["bar"], {
    "asset": ["-a", "--asset"],
    "start": ["--start"],
    "end": ["--end"],
})
rules.add_required(["check"], {
    "asset": ["-a", "--asset"],
    "rule": ["-r", "--rule"],
    "price": ["-p", "--price"],
    "start": ["--start"],
})
rules.add_optional(["check"], {
    "end": ["--end"],
})
rules.add_flags("check", {"unadjusted": ["-u", "--unadjusted"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def last(options):
    asset = options.first("asset").upper()

    endpoint = f"/price/last/{asset}"
    if options.first("asof"):
        date, _ = utils.parse_date(options.first("asof"))
        endpoint += f"/{date}"

    data, _ = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    data["price"] = "{:,.8f}".format(Decimal(data['price']))
    data["size"] = "{:,.0f}".format(Decimal(data['size']))
    df = pd.DataFrame(data, index=[0])
    df.columns = [col.title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))


def quote(options):
    asset = options.first("asset").upper()
    data, _ = remote.api.get(f"/price/quote/{asset}")

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    for col in ["price", "ask", "bid", "mid"]:
        data[col] = "{:,.2f}".format(Decimal(data[col]))
    for col in ["size", "ask_size", "bid_size"]:
        data[col] = "{:,.0f}".format(Decimal(data[col]))

    df = pd.DataFrame(data, index=[0])
    df.columns = [col.title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))


def bar(options):
    asset = options.first("asset").upper()

    start, start_dt = utils.parse_date(options.first("start"))
    if start_dt > datetime.now():
        click.echo("\nERROR: Start date cannot be in the future")
        sys.exit()

    end, end_dt = utils.parse_date(options.first("end"))
    if end_dt > datetime.now():
        end = datetime.now().strftime("%Y-%m-%d")

    data, _ = remote.api.get(f"/price/bar/{asset}/{start}/{end}")

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    for col in ["o", "h", "l", "c", "w"]:
        data[col] = "{:,.2f}".format(Decimal(data[col]))
    for col in ["v", "t"]:
        data[col] = "{:,.0f}".format(Decimal(data[col]))

    df = pd.DataFrame(data, index=[0])
    df.rename(columns={
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "w": "vwap",
        "v": "volume",
        "t": "trades",
        "date_from": "start date",
        "date_to": "end date"
    }, inplace=True)

    df1 = df[[
        "asset",
        "start date",
        "end date",
    ]]
    df1.columns = [col.title() for col in df1.columns]
    click.echo(utils.to_table(df1.T, showindex=True, showheaders=False, tablefmt="plain"))

    click.echo("\nBar data:")
    df2 = df[[
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "trades"
    ]]
    df2.columns = [col.title() for col in df2.columns]
    click.echo(utils.to_table(df2.T, showindex=True, showheaders=False))


def check(options):
    rules = ["above", "above_or_equal", "below", "below_or_equal"]
    rule = options.first("rule").lower()
    if rule not in rules:
        click.echo(f"\nERROR: Invalid rule (can only be `{'`, `'.join(rules)}`)")
        sys.exit()

    price = options.first("price").lower()
    try:
        price = float(price)
    except ValueError:
        click.echo(f"\nERROR: Invalid price ({price})")
        sys.exit()

    asset = options.first("asset").upper()

    start, start_dt = utils.parse_date(options.first("start"))
    if start_dt > datetime.now():
        click.echo("\nERROR: Start date cannot be in the future")
        sys.exit()

    end, end_dt = utils.parse_date(options.first("end", datetime.now().strftime("%Y-%m-%d")))
    if end_dt > datetime.now():
        end = datetime.now().strftime("%Y-%m-%d")

    endpoint = f"/price/check/{asset}/{rule}/{price}/{start}/{end}"
    if options.first("unadjusted"):
        endpoint += '?adjusted=false'

    data, _ = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    match = "was" if data["match"] else "was not"
    price = "{:,.2f}".format(Decimal(data['price']))
    rule = data['rule'].replace('_or_equal', ' or at')

    click.echo("")
    click.echo("YES 👍" if data["match"] else "NO 👎")
    res = click.style(f"{data['asset']} {match} {rule} {price}", fg="red")
    if data["match"]:
        res = click.style(f"{data['asset']} {match} {rule} {price}", fg="green")

    click.echo(f"\n{res}")
    click.echo(f"({data['date_from']} - {data['date_to']})")


def bars(options):
    click.echo(click.style("\nNOT ALLOWED", fg="red") + " (code 422)")
    click.echo("Due to licensing restrictions, you can only access US equity data from Tradologics servers (Tradelets, research instances, etc)")

