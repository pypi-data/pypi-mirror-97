#!/usr/bin/env python

import click
from .. import utils
from .. import remote
import pandas as pd
pd.options.display.float_format = '{:,}'.format


commands = {
    "list": "Retreive supported assets list: [--delisted|-d]",
    "info": "Show asset information: --asset|-a {ASSET} [--asof {YYYY-MM-DD}] [--history|-h]"
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_flags("list", {"delisted": ["-d", "--delisted"]})
rules.add_flags("info", {"history": ["-h", "--history"]})
rules.add_required("info", {"asset": ["-a", "--asset"]})
rules.add_optional("info", {"asof": ["--asof"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def assets_list(options):
    endpoint = "/assets"
    if options.first("exchange"):
        endpoint += f"/{options.first('exchange')}"

    if options.first("delisted", False):
        endpoint += '?delisted=true'

    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo_via_pager(utils.to_json(data))
        return

    df = pd.DataFrame(data)[[
        "ticker", "name", "exchange", "security_type",
        "delisted", "tuid", "tsid", "figi", "region", "currency"
    ]]

    if options.first("delisted", False):
        df.drop(columns=["delisted"], inplace=True)

    df.rename(columns={
        "currency": "curr",
        "security_type": "type"
    }, inplace=True)

    df.sort_values("ticker", inplace=True)
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo_via_pager(utils.to_table(df))


def asset_info(options):
    endpoint = "/asset/{identifier}".format(
        identifier=options.first("asset").upper())

    if options.first("asof"):
        date, _ = utils.parse_date(options.first("asof"))
        endpoint += f"/{date}"

    if options.first("history", False):
        endpoint += '?history=true'

    # print(endpoint)
    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    history = data.get('history')
    if history:
        del data['history']

    df = pd.DataFrame(data)[:1]

    if options.first("asof") and data['delisted']:
        # df["identifiers"] = df["tuid"]
        df.drop(columns=["identifiers"], inplace=True)
    else:
        df["identifiers"] = ", ".join(data["identifiers"])

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if history:
        click.echo("\nTicker history:")
        history.reverse()
        df = pd.DataFrame(history)
        df.columns = [col.replace("_", " ").title() for col in df.columns]
        df = df.T
        df.columns = [f"#{col+1}" for col in df.columns]
        click.echo(utils.to_table(df, showindex=True, showheaders=True))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

