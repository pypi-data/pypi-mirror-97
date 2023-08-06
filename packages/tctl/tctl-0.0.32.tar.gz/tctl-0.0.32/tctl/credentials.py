#!/usr/bin/env python

import dotenv
import click
import uuid
import os
import sys

import uuid as _uuid

from datetime import datetime
from pathlib import Path
import platform

# internals
from . import remote
from . import terminal
from . import inputs
from . import utils
from . import __env_path__

_token = {
    "id": _uuid.getnode(),
    "name": "auto-generated--tctl-{uuid}".format(uuid=_uuid.getnode())
}

if not Path.exists(__env_path__):
    Path.touch(__env_path__)

dotenv.load_dotenv(__env_path__)


def delete():
    Path.unlink(__env_path__)
    click.echo("\n")
    confirm = inputs.confirm(
        "Are you sure you want to delete your credentials?", default=False)
    if not confirm:
        raise click.Abort()

    click.echo("\nDeleting... ", nl=False)
    click.echo(click.style("SUCCESS", fg="green"))
    click.echo("NOTE: tctl will need to be re-configured in order to work.")
    sys.exit(0)


def config(source=None):
    click.echo(terminal.prompt)

    dotenv.load_dotenv(__env_path__)
    no_token = not os.getenv("TOKEN")

    if no_token:
        if platform.system() == "Darwin":
            click.echo("HELLO 👋")
        else:
            click.echo("HELLO ツ")

        if source != "config":
            click.echo("""
tctl isn't configured on this machine yet.

Please have your API Key and Secret Key handy in
order to configure tctl.

Let's get started...

-----------------------------------------------------
""")
        else:
            click.echo("""
tctl (Tradologics' Controller) helps you access
and control various aspects of your account.

To get started, make sure you have your API Key
and Secret Key handy in order to configure tctl.

Let's get started...

-----------------------------------------------------

""")

    else:
        click.echo("Current configuration: {custoemr_name}".format(
            custoemr_name=os.getenv("NAME")))
        click.echo("(Customer ID: {customer_id})\n".format(
            customer_id=os.getenv("CUSTOMER_ID")))

        update = inputs.confirm("Replace it with a new one?", default=False)
        if not update:
            raise click.Abort()

    api_key = ""
    while api_key == "":
        api_key = inputs.text("API Key     ")

    api_secret = ""
    while api_secret == "":
        api_secret = inputs.hidden("API Secret  ")

    click.echo("\nValidating... ", nl=False)

    headers = {
        "TGX-API-KEY": api_key,
        "TGX-API-SECRET": api_secret
    }

    tokens, errors = remote.api.get(
        "/tokens?obfuscated=false&tctl=true", headers=headers)

    tctl_token = None
    for token in tokens:
        if token["name"] == _token["name"]:
            tctl_token = token.get("token")
            break

    if not tctl_token:
        res, errors = remote.api.post(
            "/token?tctl=true",
            json={"name": _token['name'], "ttl": -1},
            headers=headers)

        tctl_token = res.get("token")

    # write token
    dotenv.set_key(__env_path__, "TOKEN", utils.encrypt(tctl_token))
    dotenv.set_key(__env_path__, "VERSION_CHECK",
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # get custoemer data
    res, errors = remote.api.get("/me", headers={
        "Authorization": "Bearer {token}".format(token=tctl_token)
    })

    for key in ["name", "email", "customer_id"]:
        dotenv.set_key(__env_path__, key.upper(), res.get(key))

    # update system
    # utils.track()

    utils.success_response("tctl is now configured!")
    if source != "config":
        click.echo("\nPlease run your command again")
        sys.exit()
