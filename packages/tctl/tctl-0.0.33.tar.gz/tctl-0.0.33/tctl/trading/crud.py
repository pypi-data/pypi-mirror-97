#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import remote
from decimal import Decimal
import itertools
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def positions_list(options):

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/positions"
    payload = {}

    if account:
        endpoint = "/account/{account}/positions".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo positions found.")
        return

    if not account:
        # display count
        count = 0
        rows = []
        for act, positions in data.items():
            ln = len(positions)
            count += ln
            rows.append({
                "account": act,  # accounts.get(act, act),
                "positions": ln
            })
        if count == 0:
            click.echo("\nNo positions found.")
            return

        click.echo(utils.to_table(rows))

    else:
        rows = []
        for item in data:
            item['currency'] = item['asset']['currency']
            item['asset'] = f"{item['asset']['ticker']}:{item['asset']['region']}"
            rows.append(item)

        df = pd.DataFrame(rows)
        df = df[[
            'start_date', 'end_date', 'asset', 'qty',
            'avg_fill_price', 'last_price',
            'pnl', 'pnl_pct', 'day_pnl', 'day_pnl_pct', 'currency'
        ]]

        for col in df.columns:
            if "_pct" in col:
                df[col] = df[col].astype(float) * 100

        if not options.get("start") and not options.get("end"):
            df.drop(columns=['end_date'], inplace=True)
        else:
            df.drop(columns=['day_pnl', 'day_pnl_pct'], inplace=True)

        df['qty'] = df['qty'].apply(lambda x: "{:,.0f}".format(int(x)))
        df.columns = [col.replace("_", " ").title() for col in df.columns]

        if len(df) > 20:
            click.echo_via_pager(utils.to_table(df))
        else:
            click.echo(utils.to_table(df))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def trades_list(options):

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/trades"
    payload = {}

    if account:
        endpoint = "/account/{account}/trades".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    # print(endpoint, payload)
    # return
    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)


    """
    errors = []
    data = [
    {
        "trade_id": "8efc7b9-8b2b-4000-9955-d36e7db0df74",
        "start_date": "2019-12-31T14:27:02.145282Z",
        "end_date": None,
        "min_qty": 50,
        "max_qty": 100,
        "avg_qty": 90,
        "side": "long",
        "avg_buy_price": "100",
        "avg_sell_price": None,
        "last_price": "106.05",
        "pnl": "6.05",
        "pnl_pct": "0.0605",
        "mae": "1.08152149",
        "mfe": "-0.935483870967742",
        "asset": {
        "ticker": "AAPL",
        "name": "Apple, Inc",
        "region": "US",
        "exchange": "NASDAQ",
        "currency": "USD",
        "security_type": "Common Stock",
        "tuid": "TXU000BB2K0H",
        "tsid": "TXS0005PKIKN",
        "figi": "BBG000B9Y2J5"
        }
    }]
    # data = {"alpaca": data}
    """

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo trades found.")
        return

    # display  order list
    if not data:
        click.echo("\nNo trades found for account {}".format(account))
        return

    if not account:
        # display count
        count = 0
        rows = []
        for act, positions in data.items():
            ln = len(positions)
            count += ln
            rows.append({
                "account": act,  # accounts.get(act, act),
                "trades": ln
            })
        if count == 0:
            click.echo("\nNo positions found.")
            return

        click.echo(utils.to_table(rows))

    else:
        rows = []
        for row in data:
            for col in ['max_qty', 'min_qty', 'avg_qty']:
                row[col] = "{:,.0f}".format(Decimal(row[col]))

            row["currency"] = row['asset']['currency']
            row["asset"] = f"{row['asset']['ticker']}:{row['asset']['region']}"

            rows.append(row)

        cols = [
            'asset', 'side', 'start_date', 'end_date',
            'max_qty', 'min_qty', 'avg_qty', 'avg_buy_price',
            'avg_sell_price', 'pnl', 'pnl_pct',
            'account', 'strategy', 'currency'
        ]
        df = pd.DataFrame(rows)
        df = df[[col for col in cols if col in df.columns]]

        for col in df.columns:
            if "_pct" in col:
                df[col] = df[col].astype(float) * 100

        df.columns = [col.replace("_", " ").title() for col in df.columns]

        if len(df) > 20:
            click.echo_via_pager(utils.to_table(df))
        else:
            click.echo(utils.to_table(df))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


