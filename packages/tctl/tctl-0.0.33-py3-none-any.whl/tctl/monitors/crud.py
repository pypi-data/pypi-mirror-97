#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import inputs
from .. import remote
from decimal import Decimal
import re
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def monitors_list(options):
    endpoint = "/monitors"
    strategy = options.first("strategy")
    if strategy:
        endpoint += f"/{endpoint}"
    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo monitors found.")
        return

    table_data = []
    with_ids = options.first('ids', False)
    for item in data:
        if with_ids:
            record = {
                "id": item["id"],
                "asset": item["asset"],
            }
        else:
            record = {
                "asset": item["asset"],
            }
        rule = item["rule"]
        if item["type"] == "price":
            record["trigger"] = 'Price '+ rule["type"].replace('_or_equal', '=').replace('above', '>').replace('below', '<')
            record["trigger"] += " {:,.2f}".format(Decimal(rule["target"]))
            record["account"] = "N/A"

        if item["type"] == "position":
            type_numeric = "-" if rule["type"] == "loss" else "+"
            record["trigger"] = f'{type_numeric}{(float(rule["target"])*100)}% on {rule["direction"]} position'
            record["account"] = rule["account_id"]

        record["strategies"] = len(item["strategies"])
        table_data.append(record)

    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def monitor_create(options):
    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    click.echo("")

    asset = ""
    while asset == "":
        asset = inputs.text("Asset to monitor")

    if options.first("type") not in ["price", "position"]:
        kind = inputs.option_selector(
            f"Monitor {asset} for", ["Price target", "Position profit/loss"]
        ).split(' ')[0].lower()


    if kind == "price":
        account = ""
        rule = inputs.option_selector(
            "Trigger when price is", ["Above", "Above or Equal", "Below", "Below or Equal"]
        ).lower().replace(" ", "_")

        num = inputs.text(
            "Target price",
            validate=lambda _, x: re.match(re.compile(r'(\d+(\.\d+)?)'), x))

    elif kind == "position":

        direction = inputs.option_selector(
            "Your position direction", ["Long", "Short"]
        ).lower().replace(" ", "_")

        rule = inputs.option_selector(
            "Monitor for", ["Profit", "Loss"]).lower().replace(" ", "_")

        num = inputs.text(
            "Target Percent (as decimal number)",
            validate=lambda _, x: re.match(re.compile(r'(0+(\.\d+)?)'), x))

        accounts = {}
        supported_accounts, errors = remote.api.get("/accounts")
        for key, account in supported_accounts.items():
            accounts[account['name']] = account["account_id"]
        account = accounts[inputs.option_selector(
            "Monitor position on broker account", list(accounts.keys()))]

    selected_strategies = []
    while not selected_strategies:
        selected_strategies = inputs.checkboxes(
            "Notify strategy(ies)", list(strategies.keys()))
        if not selected_strategies:
            click.echo(click.style("\nFAILED", fg="red"))
            click.echo("Monitor *must* be associated with at least one strategy.")

    strategies = [s for n, s in strategies.items() if n in selected_strategies]

    ttl = inputs.text(
        "Time-to-live (seconds from now to expire) - optional",
        validate=lambda _, x: re.match(re.compile(r'^$|((-?)(\d+))'), x),
        default=-1)

    if ttl == "":
        ttl = "-1"

    payload = {
        "type": kind,
        "asset": asset,
        "strategies": strategies,
        "ttl": ttl
    }

    if kind == "price":
        payload["rule"] = {
            "type": rule,
            "target": float(num),
        }
    elif kind == "position":
        payload["rule"] = {
            "type": rule,
            "target": float(num),
            "direction": direction,
            "account_id": account
        }

    data, errors = remote.api.post(f"/monitor", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The monitor was created with the id `{data['id']}`.")
    click.echo("\nThe following strategies will be notified when it triggers:")
    click.echo(" - "+"\n - ".join(data["strategies"]))


def monitor_delete(options):
    monitor = options.first("monitor")
    remote.api.delete("/monitor/{monitor}".format(
        monitor=options.first("monitor")))

    utils.success_response(
        f"The monitor `{monitor}` was removed from your account")
