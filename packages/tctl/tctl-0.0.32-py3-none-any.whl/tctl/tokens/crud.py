#!/usr/bin/env python

import click
from .. import utils
from .. import inputs
from .. import remote
import sys
import re
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def _get_token(options, decode=False):
    if options.first("decode", decode):
        tokens, errors = remote.api.get("/tokens?obfuscated=false")
    else:
        tokens, errors = remote.api.get("/tokens")

    req_token = options.first("token")
    for token in tokens:
        token["name"] = token.get("name").lower().replace(" ", "-")
        if token["name"] == req_token:
            return token

    if options.get("raw"):
        click.echo(utils.to_json({}))
        sys.exit(0)

    click.echo(f"\nThe token {req_token} wasn't found, was deleted, or has expired.")
    sys.exit(0)


def tokens_list(options):
    data = []
    endpoint = "/tokens"
    if options.get("decode", True):
        endpoint += "?obfuscated=false"
    tokens, errors = remote.api.get(endpoint)

    for token in tokens:
        if "auto-generated" not in token.get("name"):
            data.append(token)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo tokens found.")
        return

    table_data = []
    for item in data:
        table_data.append({
            # "name": item["name"],
            "name": item["name"].lower().replace(" ", "-"),
            "expires_on": item["expiration"].split("T")[0],
            # "active": item["active"],
            "token": item["token"],
        })
    click.echo(utils.to_table(table_data))


def token_info(options):
    token = _get_token(options)
    token["expiration"] = token["expiration"].split("T")[0]

    click.echo("\n--------")
    click.echo(f"Name:       {token.get('name')}")
    click.echo(f"Expiration: {token.get('expiration')}")
    # click.echo(f"Active:     {token.get('active')}")
    if options.first("decode"):
        click.echo(f"Token:      {token.get('token')}")
    else:
        click.echo(f"Token:      {token.get('token')}")
    click.echo("--------")


def token_create(options):
    click.echo("""
To create a new token, please make sure that you
have your API Key and Secret Key handy.
    """)

    api_key = api_secret = name = ""
    while api_key == "":
        api_key = inputs.text("API Key     ")
    while api_secret == "":
        api_secret = inputs.hidden("API Secret  ")

    headers = {
        "TGX-API-KEY": api_key,
        "TGX-API-SECRET": api_secret
    }

    while name == "":
        name = inputs.text("Token name")

    ttl = inputs.text(
        "Time-to-live (seconds from now to expire) - optional",
        validate=lambda _, x: re.match(re.compile(r'^$|((-?)(\d+))'), x))

    if ttl == "":
        ttl = "-1"

    click.echo("Creating token... ")

    data, errors = remote.api.post(
        "/token",
        json={"name": name, "ttl": int(ttl)},
        headers=headers)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response("The token was created successfully!")

    click.echo(f"\nName:       {data.get('name')}")
    click.echo(f"Expiration: {data.get('expiration')}")
    # click.echo(f"Active:     {data.get('active')}")
    click.echo(f"Token:      {data.get('token')}")


def token_delete(options):
    token = _get_token(options, full=True)

    data, errors = remote.api.delete(
        "/token", headers={
            "Authorization": "Bearer {token}".format(token=token.get("token"))})

    utils.success_response(
        f"The token `{token.get('name')}` successfully deactivated.")


def token_extend(options):
    token = _get_token(options, full=True)
    click.echo("")

    ttl = options.first("ttl", inputs.text(
        "New time-to-live (seconds from now to expire)",
        validate=lambda _, x: re.match(re.compile(r'(-?)(\d+)'), x)))

    data, errors = remote.api.patch("/token", json={"ttl": int(ttl)}, headers={
            "Authorization": "Bearer {token}".format(token=token.get("token"))})

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response("The token was updated successfully!")
    click.echo("New expiration date is: ", nl=False)
    click.echo(data.get('expiration').replace("T", " ").rstrip("Z"))
