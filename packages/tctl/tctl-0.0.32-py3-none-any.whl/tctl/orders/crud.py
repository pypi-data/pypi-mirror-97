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


def _format_order(order):
    order["description"] = order['asset']['name']
    order["currency"] = order['asset']['currency']
    asset = f"{order['asset']['ticker']}"
    if "region" in order['asset']:
        asset += f":{order['asset']['region']}"
    order["asset"] = asset

    order["filled_qty"] = "{:,.0f}".format(Decimal(order["filled_qty"]))
    order["qty"] = "{:,.0f}".format(Decimal(order["qty"]))
    for col in ['avg_fill_price', 'limit_price', 'stop_price']:
        order[col] = utils.to_decimal(order[col])

    return order


def orders_list(options):
    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}

    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return
    endpoint = "/orders"
    payload = {}

    if account:
        endpoint = "/account/{account}/orders".format(account=account)
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
        click.echo("\nNo orders found.")
        return

    table_data = []

    if not account:
        # display count
        for act, orders in data.items():
            table_data.append({
                "account": act,  # accounts.get(act, act),
                "orders": len(orders)
            })

    else:
        # display  order list
        if not data:
            click.echo("\nNo orders found for account {}".format(account))
            return

        rows = []
        for row in data:
            for col in ['qty', 'filled_qty', 'avg_fill_price']:
                row[col] = utils.to_decimal(row[col])

            row["currency"] = row['asset']['currency']
            row["asset"] = f"{row['asset']['ticker']}:{row['asset']['region']}"

            rows.append(row)

        cols = [
            'asset', 'qty', 'filled_qty',
            'side', 'type', 'tif',
            'limit_price', 'stop_price'
            'avg_fill_price', 'status',
            'created_at', 'updated_at',
            'comment', 'strategy_id',
            'account_id', 'currency']

        if options.first('ids', False):
            cols = ['order_id'] + cols

        table_data = pd.DataFrame(rows)
        table_data = table_data[[col for col in cols if col in table_data.columns]]
        # print(table_data.columns)

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def order_create(options):
    click.echo("")

    side = ""
    while side == "":
        side = inputs.option_selector("Order side", [
            "Buy", "Sell"]).lower().replace(" ", "_")

    asset = ""
    while asset == "":
        asset = inputs.text(f"Asset to {side}").upper()

    qty = inputs.text(
        "Quantity",
        validate=lambda _, x: re.match(re.compile(r'(\d+)'), x))

    order_type = inputs.option_selector("Order type", [
        "Market", "Limit", "Stop", "Stop Limit"]).lower().replace(" ", "_")

    price = None
    if "limit" in order_type:
        price = inputs.text(
            "Price (leave blank for market order)",
            validate=lambda _, x: re.match(re.compile(r'(\d+(\.\d+)?)'), x))

    tif = inputs.option_selector("Time in force", [
        "DAY", "GTC", "OPG", "CLS", "IOC", "FOK"]).lower()

    extended_hours = not inputs.confirm(
        "Execute during regular market hours?", default=True)

    payload = {
        "asset": asset,
        "qty": int(qty),
        "side": side,
        "order_type": order_type,
        "tif": tif,
        "extended_hours": extended_hours,
    }
    if order_type == "limit":
        payload["limit_price"] = price
    elif order_type == "stop_limit":
        payload["stop_price"] = price

    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    selected_strategy = strategies[inputs.option_selector(
        "Associate with strategy", list(strategies.keys()))]

    if not selected_strategy:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("You *must* be associate this order with a strategy.")

    accounts = {}
    supported_accounts, errors = remote.api.get("/accounts")
    for key, account in supported_accounts.items():
        accounts[account['name']] = account["account_id"]
    selected_account = accounts[inputs.option_selector(
        "Execute on broker", list(accounts.keys()))]

    payload["strategy_id"] = selected_strategy
    payload["account_id"] = selected_account

    payload["comment"] = inputs.text("Comment (optional)")

    payload["submit"] = inputs.confirm(
        "Submit order? (no will create an order that you can submit later)", default=True)

    print(utils.to_json(payload))
    # return
    data, errors = remote.api.post(f"/orders", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    and_submitted = " and submitted" if payload["submit"] else ""
    utils.success_response(
        f"The order was created{and_submitted} successfully.")

    click.echo(f"Order Id: {data['order_id']}")

    df = pd.DataFrame([_format_order(data)])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(
            df.T, missingval="-", showindex=True, showheaders=False))


def order_info(options):
    data, errors = remote.api.get("/order/{order}".format(
        order=options.first("order")))

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    df = pd.DataFrame([_format_order(data)])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def order_delete(options):
    order = options.first("order")
    remote.api.delete("/order/{order}".format(
        order=options.first("order")))

    utils.success_response(
        f"The order `{order}` was cancelled successfully.")


def order_update(options):
    click.echo("")

    order_id = options.first("order")
    order, errors = remote.api.get(f"/order/{order_id}")

    if order.get("status") not in ["submitted", "accepted"]:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("You cannot update already-processed orders.")
        return

    click.echo(f"Modify order for {order.get('ticker')} on {order.get('account_id')}:\n")

    side = ""
    while side == "":
        side = inputs.option_selector(f"Order side [{order.get('side')}]", [
            "Buy", "Sell"]).lower().replace(" ", "_")

    qty = inputs.text(
        f"Quantity [{order.get('qty')}]",
        validate=lambda _, x: re.match(re.compile(r'(\d+)'), x))

    order_type = inputs.option_selector("Order type", [
        "Market", "Limit", "Stop", "Stop Limit"]).lower().replace(" ", "_")

    price = None
    if "limit" in order_type:
        price = inputs.text(
            "Price (leave blank for market order)",
            validate=lambda _, x: re.match(re.compile(r'(\d+(\.\d+)?)'), x))

    tif = inputs.option_selector("Time in force", [
        "DAY", "GTC", "OPG", "CLS", "IOC", "FOK"]).lower()

    extended_hours = not inputs.confirm(
        "Execute during regular market hours?", default=True)

    payload = {
        "asset": order.get("ticker"),
        "qty": int(qty),
        "side": side,
        "order_type": order_type,
        "tif": tif,
        "extended_hours": extended_hours,
    }
    if order_type == "limit":
        payload["limit_price"] = price
    elif order_type == "stop_limit":
        payload["stop_price"] = price

    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    selected_strategy = strategies[inputs.option_selector(
        "Associate with strategy", list(strategies.keys()))]

    if not selected_strategy:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("You *must* be associate this order with a strategy.")

    payload["strategy_id"] = selected_strategy

    payload["comment"] = inputs.text("Comment (optional)")

    payload["submit"] = not inputs.confirm(
        "Submit order? (no will create an order that you can submit later)", default=True)

    data, errors = remote.api.patch(f"/orders/{order_id}", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    and_submitted = " and submitted" if payload["submit"] else ""
    utils.success_response(
        f"The order was updated{and_submitted} successfully.")

    click.echo(f"Order Id: {data['id']}")

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(
            df.T, missingval="-", showindex=True, showheaders=False))


def order_submit(options):
    order = options.first("order")
    remote.api.post("/order/{order}".format(
        order=options.first("order")))

    utils.success_response(
        f"The order `{order}` was submitted successfully.")

