#!/usr/bin/env python

import click
import sys
from .. import utils
from .. import remote
from datetime import datetime
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def customer(options):
    """Show my account's info """
    data, errors = remote.api.get("/me")

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))


def usage(options):
    """Show my account's usage """
    if options.get("log") and options.get("breakdown"):
        click.echo("\nError: Cannot use both --log and --breakdown")
        sys.exit()

    endpoint = "/me/usage"
    if options.get("log"):
        endpoint += "/log"
    elif options.get("breakdown"):
        endpoint += "/breakdown"

    payload = {}
    if options.first("start"):
        start, start_dt = utils.parse_date(options.first("start"))
        if start_dt > datetime.now():
            click.echo("\nError: Start date cannot be in the future")
            sys.exit()
        payload["date_from"] = start
    if options.first("end"):
        end, end_dt = utils.parse_date(options.first("end"))
        if end_dt > datetime.now():
            end = datetime.now().strftime("%Y-%m-%d")
        payload["date_to"] = end

    data, errors = remote.api.get(endpoint, json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    click.echo(f"\nPeriod Start:  {data['period_start']}")
    click.echo(f"Period End:    {data['period_end']}")
    click.echo("Total Actions: {:,.0f}".format(data['total_actions']))

    if options.get("log"):
        df = pd.DataFrame([data["summary"]]).T.reset_index()
        df.columns = ['endpoint', 'methods']
        methods = pd.json_normalize(df['methods'])
        df = pd.concat([df['endpoint'], methods], axis=1)
        df.columns = ['Endpoint', 'GET', 'POST', 'PATCH', 'DELETE', 'Total']
        click.echo(utils.to_table(
            df, showindex=False, showheaders=True))
        sys.exit()

    if options.get("breakdown"):
        df = pd.DataFrame([data["summary"]["api_calls"]])
        df.columns = [col.replace("_", " ").title() for col in df.columns]
        click.echo("\n* API Calls:", nl=False)
        click.echo(utils.to_table(
            df, showindex=False, showheaders=True, floatfmt=".0f"))

        df = pd.DataFrame([data["summary"]["tradehooks"]])
        df.columns = [col.replace("_", " ").title() for col in df.columns]
        click.echo("\n* Tradehooks:", nl=False)
        click.echo(utils.to_table(
            df, showindex=False, showheaders=True, floatfmt=".0f"))

        for item in ["order", "positions", "price"]:
            df = pd.DataFrame([data["summary"]["monitors"][item]])
            df.columns = [col.replace("_", " ").title() for col in df.columns]
            click.echo(f"\n* Monitor minutes - {item.title()}:", nl=False)
            click.echo(utils.to_table(
                df, showindex=False, showheaders=True, floatfmt=".0f"))

        sys.exit()

    df = pd.DataFrame([data["summary"]])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(
        df, showindex=False, showheaders=True, floatfmt=".0f"))
    sys.exit()
