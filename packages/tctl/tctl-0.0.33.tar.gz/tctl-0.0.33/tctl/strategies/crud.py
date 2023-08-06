#!/usr/bin/env python

import click
import re
import sys
from .. import utils
from .. import inputs
from .. import remote

# temp: for strategy status
from .. import __env_path__
from datetime import datetime
import os
import pandas as pd
import dotenv

dotenv.load_dotenv(__env_path__)
pd.options.display.float_format = '{:,}'.format

MODES = {
    "backtest": "run simutation using historical data",
    "paper": "by Tradologics - orders will not be routed to the broker",
    "broker": "live or demo/paper, depending on your credentials"
}

PAPER_MSG = """Strategies running in Paper mode needs to have
a dedicated \"paper\" account associated with them in order
to calculate strategy's performance and determine its
capabilities (such as start balance and shorting/margin).
"""

regex = re.compile(
    r'^https?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def strategies_list(options):
    data, errors = remote.api.get("/strategies")
    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    strategies = pd.DataFrame(data)
    strategies = strategies[[col for col in strategies.columns if col not in ['url', 'uuid']]]
    strategies['status'] = strategies['status'].str.replace('_', ' ').str.title()
    strategies['mode'] = strategies['mode'].str.replace('_', ' ').str.title()
    click.echo(utils.to_table(strategies, hide=["urls"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_info(options):
    data, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    if data.get("as_tradelet", True):
        del data["url"]

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_status(options):
    data, errors = remote.api.get("/strategy/{strategy}/status".format(
        strategy=options.first("strategy")))

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    click.echo("\nStatus: {status}".format(status=data["status"].replace('_', ' ').title()))


def strategy_log(options):
    data, errors = remote.api.get("/strategy/{strategy}/logs".format(
        strategy=options.first("strategy")))

    lines = abs(int(options.first("lines", 10)))
    data["logs"] = data["logs"][-lines:]

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data["logs"]:
        click.echo("\n[no logs]")
        return

    if lines > 15:
        click.echo_via_pager("\n" + "\n".join(data["logs"]))
    else:
        click.echo("\n" + "\n".join(data["logs"]))


def strategy_update(options):

    strategy, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    click.echo()
    name = inputs.text(f"Name [{strategy['name']}]")
    description = inputs.text(f"Description [{strategy['description']}]")
    mode = inputs.option_selector(
        "Mode", [
            f"{mode.title()} ({desc})" for mode, desc in MODES.items()
        ]).split(' ')[0].lower()

    data, errors = remote.api.patch(
        "/strategy/{strategy}".format(strategy=options.first("strategy")),
        json={
            "name": name,
            "description": description,
            "mode": mode.split(' ')[0].lower()
        })

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy `{name}` was updated")

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_delete(options):
    strategy = options.first("strategy")
    remote.api.delete("/strategy/{strategy}".format(strategy=strategy))

    utils.success_response(
        f"The strategy `{strategy}` was removed from your account")


def strategy_set_mode(options):

    strategy, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    mode = options.first("mode")

    if mode not in ["backtest", "paper", "broker"]:
        click.echo("\nCurrent mode: {mode}".format(mode=strategy["mode"]))
        click.echo()
        mode = inputs.option_selector(
            "New mode", [strategy["mode"].title() + f' ({MODES[strategy["mode"]]})'] + [
                f"{mode.title()} ({desc})" for mode, desc in MODES.items() if mode != strategy["mode"]
            ]).split(' ')[0].lower()

    if mode.lower() == strategy["mode"]:
        click.echo(f"Aborted! The strategy mode was unchanged ({mode}).")
        return

    data, errors = remote.api.patch(
        "/strategy/{strategy}".format(strategy=options.first("strategy")),
        json={
            "mode": mode.lower()
        })

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy's mode was chaned to `{mode}`")


def strategy_start(options):
    strategy = options.first("strategy")

    data, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    # --- do not allow re-run for 1 minute
    started = os.getenv(f"start_{strategy}")
    if started:
        started = datetime.strptime(started, "%Y-%m-%d %H:%M:%S")
        min_since_started = (datetime.now() - started).seconds // 60
        if min_since_started < 1:
            click.echo("Strategy is being deployed...")
            sys.exit()
    # ---

    if data.get("status") == "Running":
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo(f"The strategy '{strategy}' is already running in {data.get('mode')} mode.")
        sys.exit()

    if data.get("mode") != "broker":
        click.echo(click.style("\n>>> NOTE:  ", fg="yellow"), nl=False)
        click.echo(PAPER_MSG)

    payload = utils.virtual_account_payload(data.get("mode"))

    data, errors = remote.api.post(f"/strategy/{strategy}/start", json=payload)

    data, _ = remote.api.get(f"/strategy/{strategy}")

    if data["as_tradelet"]:
        dotenv.set_key(__env_path__, f"start_{strategy}",
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        data["message"] = [
            "Tradelet deploy initialized...",
            click.style("\nNOTE: ", fg="yellow") +
            "Strategies can take a few minutes to be deployed.",
            "\nYou can check your strategy status using:",
            f"$ tctl strategies status --strategy {strategy}",
            f"\nDeploy log is available via:\n$ tctl strategies log --strategy {strategy}",
        ]
    else:
        data["message"] = ["Strategy starting.."]

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response("\n".join(data["message"]))


def strategy_stop(options, _response=True):
    strategy = options.first("strategy")
    _, error = remote.api.post(f"/strategy/{strategy}/stop", halt_on_error=False)

    if _response:
        if error:
            click.echo(click.style("\nFAILED", fg="red"))
            click.echo(error[0]["message"])
            return

        utils.success_response(f"The strategy `{strategy}` was stopped.")


def strategy_set_public(options):
    strategy = options.first("strategy")

    remote.api.post(
        "/strategy/{strategy}/public".format(strategy=strategy))

    utils.success_response(f"The strategy `{strategy}` is now public.")

    data, _ = remote.api.get(f"/strategy/{strategy}")

    click.echo("\nThe public url of the strategy is:")
    click.echo(f"https://tearsheet.report/{strategy}/{data.get('uuid', '')}")


def strategy_set_private(options):
    strategy = options.first("strategy")
    remote.api.post(
        "/strategy/{strategy}/private".format(strategy=strategy))

    utils.success_response(f"The strategy `{strategy}` is now private.")


def strategy_create(options):
    click.echo()
    name = ""
    while name == "":
        name = inputs.text("Strategy name")
    description = inputs.text("Description (leave blank for none)")
    mode = inputs.option_selector(
        "Mode", [
            f"{mode.title()} ({desc})" for mode, desc in MODES.items()
        ]).split(' ')[0].lower()

    as_tradelet = inputs.confirm(
        "Run strategy on Tradologics (via Tradelets)?", default=True)
    url = None
    if not as_tradelet:
        while url is None:
            url = inputs.text(
                "Strategy URL", validate=lambda _, x: re.match(regex, x))

    payload = {
        "name": name,
        "description": description,
        "mode": mode,
        "as_tradelet": as_tradelet,
    }
    if url:
        payload["url"] = url

    data, errors = remote.api.post("/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy `{name}` was successully created with `{mode.split(' ')[0]}` mode")

    cols = ['name', 'strategy_id', 'description', 'as_tradelet', 'mode']
    if not as_tradelet:
        cols.append("url")
    df = pd.DataFrame([data])[cols]
    df['mode'] = df['mode'].str.title()

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_report(options):
    error = {
        "id": "unprocessable_request",
        "message": "Not supported yet via tctl"
    }
    click.echo(click.style("\nFAILED", fg="red"), nl=False)
    click.echo(" (status code 422):")
    click.echo(utils.to_json(error))

