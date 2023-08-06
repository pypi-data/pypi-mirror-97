#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import inputs
from .. import remote
from decimal import Decimal

import pandas as pd
pd.options.display.float_format = '{:,}'.format

NUMERIC_COLS = ["regt_buying_power", "equity", "daytrading_buying_power",
                "buying_power", "cash", "unrealized_pnl", "realized_pnl",
                "initial_margin", "maintenance_margin", "sma"]


def accounts_list(options):
    data, errors = remote.api.get("/accounts")

    for x in data:
        if "realized_pnl" not in data[x]:
            data[x]["realized_pnl"] = 0
        if "unrealized_pnl" not in data[x]:
            data[x]["unrealized_pnl"] = 0
        if "equity" not in data[x]:
            data[x]["equity"] = 0

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo accounts found.")
        return

    table_data = []
    for x in data:
        item = {
            "name": data[x]["name"],
            "id": data[x]["account_id"],
            "broker": "{broker} ({currency})".format(
                broker=data[x]["broker"].title(),
                currency=data[x]["currency"]
            ),
            "is_paper": data[x]["paper"],
            "equity": utils.fillna(data[x]["equity"], True),
            "realized_pnl": utils.fillna(data[x]["realized_pnl"], True),
            "unrealized_pnl": utils.fillna(data[x]["unrealized_pnl"], True),
        }

        table_data.append(item)

    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def account_info(options):
    data, errors = remote.api.get("/account/{account}".format(
        account=options.first("account")))

    if "realized_pnl" not in data:
        data["realized_pnl"] = 0
    if "unrealized_pnl" not in data:
        data["unrealized_pnl"] = 0
    if "equity" not in data:
        data["equity"] = 0

    data["broker"] = data["broker"].title()

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = utils.fillna(df[col].fillna(0).astype(str).values[0], True)

    # order cols
    df = df[[
        'name',
        'account_id',
        'broker',
        'account',
        'cash',
        'equity',
        'currency',
        'paper',
        'unrealized_pnl',
        'realized_pnl',
        'status',
        'blocked',
        'buying_power',
        'initial_margin',
        'maintenance_margin',
        'pattern_day_trader',
        'regt_buying_power',
        'daytrading_buying_power',
        'daytrade_count',
        'shorting_enabled',
        'multiplier',
        'sma',
    ]]

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def account_create(options):

    brokers = {}
    supported_brokers, errors = remote.api.get("/brokers?tctl=true")
    for broker in supported_brokers:
        brokers[broker['name']] = broker

    click.echo("")
    name = ""
    while name == "":
        name = inputs.text("Account name")

    broker = inputs.option_selector(
        "Please select broker", list(brokers.keys()))
    broker = brokers.get(broker)

    paper_mode = False
    auth = {}
    payload = {}

    if broker["name"] == "tradologics":
        paper_mode = True
        payload = utils.virtual_account_payload("paper")

    else:
        if broker.get("has_paper", False):
            paper_mode = inputs.confirm(
                "Use broker's paper account", default=True)

        if broker["name"] == "ib":
            while not auth.get("key"):
                auth["key"] = inputs.text("Username")
            while not auth.get("secret"):
                auth["secret"] = inputs.hidden("Password")
            while not auth.get("account_id"):
                auth["account_id"] = inputs.hidden("Account ID")
        else:
            for key in broker["auth"]:
                while not auth.get(key):
                    auth[key] = inputs.hidden(
                        key.replace("_", " ").title().replace("Id", "ID"))

    payload = {**payload, **{
        "name": name,
        "paper": paper_mode,
        "auth": auth,
        "broker": broker["broker_id"]
    }}

    data, errors = remote.api.post("/accounts", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The broker account `{name}` ({broker['name']}) was added to your account.")

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col])

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if broker["name"] == "ib":
        click.echo("\nNOTE:\nIB accounts can take up to 5 minutes to be deployed.")
        click.echo("\nCheck your account status in a few minutes using")
        click.echo(f"  tctl accounts info --account {data['account_id']}")


def account_update(options):

    account, errors = remote.api.get("/account/{account}".format(
        account=options.first("account")))

    supported_brokers, errors = remote.api.get("/brokers")
    for broker in supported_brokers:
        if broker["broker_id"] == account["broker"]:
            break

    click.echo(f"\nAccount's Broker: {broker['name']}\n")
    name = ""
    while name == "":
        name = inputs.text("New account name")

    paper_mode = False
    key = secret = account_id = None

    if broker["broker_id"] == "tradologics":
        paper_mode = True
    else:
        if broker["broker_id"] != "paper":
            if broker.get("has_paper", True):
                paper_mode = inputs.confirm(
                    "Use broker's paper account", default=True)

            click.echo(
                "\nTo update credentials, enter new information (leave blank otherwise):\n")

            if broker["broker_id"] == "ib":
                key = inputs.text("Username")
                secret = inputs.hidden("Password")
                account_id = inputs.hidden("Account ID")
            else:
                key = inputs.hidden("Key (API key or Token)")
                secret = inputs.hidden("Secret (leave blank if using a token)")

    payload = {
        "name": name,
        "paper": paper_mode
    }

    if key or secret or account_id:
        payload["auth_info"] = {}
        if key:
            payload["auth_info"]["key"] = key
        if secret:
            payload["auth_info"]["secret"] = secret
        if account_id:
            payload["auth_info"]["account_id"] = account_id

    click.echo(utils.to_json(payload))
    # return

    data, errors = remote.api.patch(f"/account/{account['account_id']}", json=payload)

    if "realized_pnl" not in data:
        data["realized_pnl"] = 0
    if "unrealized_pnl" not in data:
        data["unrealized_pnl"] = 0
    if "equity" not in data:
        data["equity"] = 0

    data["broker"] = data["broker"].title()

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The broker account `{name}` ({broker['name']}) was updated")

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = utils.fillna(df[col].fillna(0).astype(str).values[0], True)

    # order cols
    df = df[[
        'name',
        'account_id',
        'broker',
        'account',
        'cash',
        'equity',
        'currency',
        'paper',
        'unrealized_pnl',
        'realized_pnl',
        'status',
        'blocked',
        'buying_power',
        'initial_margin',
        'maintenance_margin',
        'pattern_day_trader',
        'regt_buying_power',
        'daytrading_buying_power',
        'daytrade_count',
        'shorting_enabled',
        'multiplier',
        'sma',
    ]]

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def account_delete(options):
    account = options.first("account")
    remote.api.delete("/account/{account}".format(
        account=options.first("account")))

    utils.success_response(
        f"The broker account `{account}` was removed succesfully.")
