#!/usr/bin/env python

import click
from .. import utils
from .. import inputs
from .. import remote
from ..strategies.crud import strategy_stop
import ujson as json
import yaml
import sys
from pathlib import Path

import pandas as pd
pd.options.display.float_format = '{:,}'.format


def _format_tradehook(tradehook):
    when = tradehook.get("when", {})
    schedule = when.get("schedule", {})
    on_days = schedule.get("on_days", "*")
    if isinstance(on_days, list):
        on_days = ", ".join(schedule.get("on_days"))
        on_days = on_days.title()

    o = format_offset("open", schedule.get("session", {}).get("open"))
    c = format_offset("close", schedule.get("session", {}).get("close"))
    session = f'{o} to {c} ({schedule.get("exchange")} time)'
    on = schedule.get("on", schedule.get("true", "close"))
    return {
        "id": tradehook["tradehook_id"],
        "schedule": f"Every: {on_days}\n{session}\nTiming: {schedule.get('timing')} (on bar {on})",
        "conditions": len(when.get("condition", [])),
        "strategies": len(tradehook["strategies"]),
        "invocations": tradehook["invocations"],
        "comment": tradehook["comment"],
    }


def format_offset(item, offset):
    offset = str(offset).replace("+", "")
    try:
        offset = int(offset)
        if offset > 0:
            return f'[{item.title()}+{offset}min]'
        elif offset < 0:
            return f'[{item.title()}-{abs(offset)}min]'
        else:
            return item.title()
    except Exception:
        pass
    return offset


def tradehooks_list(options):
    data, errors = remote.api.get("/tradehooks")

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo Tradehooks found.")
        return

    table_data = []
    for item in data:
        table_data.append(_format_tradehook(item))

    table = utils.to_table(table_data, tablefmt="grid")
    if len(table_data) > 10:
        click.echo_via_pager(table)
    else:
        click.echo(table)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_info(options):
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    # data["when"]["condition"] = [{
    #  "asset": "AAPL:US",
    #  "trigger": "price",
    #  "rule": {
    #    "type": "above",
    #    "price": 200.00
    #  }}]

    tradehook = _format_tradehook(data)

    click.echo(f"\nTradeook information for `{tradehook['id']}`:")

    tradehook['invocations'] = 62137
    if tradehook['invocations']:
        since = tradehook.get("created_at", "creation")
        click.echo(f"\nInvocations: \n - {utils.to_decimal(tradehook['invocations'])} since {since}")
    else:
        click.echo("\nNo invocations yet")

    if data['strategies']:
        click.echo(f"\nAttached to:")
        click.echo(' - ' + '\n - '.join(data['strategies']))
    else:
        click.echo(f"\n Not attached to any strategy")

    schedule = tradehook['schedule'].replace('\n', '\n - ')
    click.echo(f"\nSchedule:\n - {schedule}")

    if 'condition' in data['when']:
        click.echo(f"\nConditions:")
        conditions = []
        for condition in data['when']['condition']:
            if "rule" in condition:
                condition["rule"] = f'{condition["rule"]["type"]} {utils.to_decimal(condition["rule"]["price"])}'
            conditions.append(' '.join(condition.values()))
        click.echo(' - ' + '\n - '.join(conditions))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_create(options, from_update=False):
    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    click.echo("")
    name = ""
    if from_update:
        name = inputs.text("Tradehook name [{s}]".format(
            s=options.first("tradehook")))
    else:
        while name == "":
            name = inputs.text("Tradehook name")

    config_file_found = False
    while not config_file_found:
        config_file = inputs.path(
            "Path to Tradehook configuration file", validator="file")
        config_file_found = Path(config_file).exists() and utils.reversed_in(
            [".json", ".yaml"], config_file, match="any")
        if not config_file_found:
            click.echo("Invalid file format")

    selected_strategies = inputs.checkboxes(
        "Attach to (optional, can be done later)", list(
            strategies.keys()))

    # if not selected_strategies:
    #     click.echo(click.style("\nFAILED", fg="red"))
    #     click.echo("Tradehook *must* be associated with at least one strategy.")

    strategies = [s for n, s in strategies.items() if n in selected_strategies]

    payload = {}
    if ".json" in config_file:
        with open(Path(config_file), encoding="utf-8") as f:
            try:
                payload = json.load(f)
            except ValueError:
                click.echo(click.style("\nFAILED", fg="red"))
                click.echo("Cannot parse JSON. Is this a valid JSON file?")
                sys.exit()
    else:
        with open(Path(config_file), encoding="utf-8") as f:
            try:
                payload = yaml.load(f, Loader=yaml.SafeLoader)
            except yaml.parser.ParserError:
                click.echo(click.style("\nFAILED", fg="red"))
                click.echo("Cannot parse YAML. Is this a valid YAML file?")
                sys.exit()

    if not payload:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Tradehook configuration file appears to be empty.")

    if strategies:
        payload["strategies"] = strategies
    payload["name"] = name
    payload["comment"] = inputs.text("Comment (optional)")

    # print(utils.to_json(payload))
    # return

    if from_update:
        return payload
    data, errors = remote.api.post("/tradehooks", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The Tradehook `{name}` was created successfuly.")
    if strategies:
        click.echo("It was attached to:")
        click.echo(" - "+"\n - ".join(strategies))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_update(options):
    tradehook = options.first("tradehook")

    payload = tradehook_create(options, from_update=True)
    tradehook, errors = remote.api.get(f"/tradehook/{tradehook}")

    if payload["name"] == "":
        payload["name"] = tradehook["name"]

    if payload["comment"] == "":
        payload["comment"] = tradehook["comment"]

    if not payload.get("strategies"):
        payload["strategies"] = tradehook["strategies"]

    data, errors = remote.api.patch(
        f"/tradehook/{tradehook}", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The tradehook `{tradehook}` was updated successfully.")
    if payload["strategies"]:
        click.echo("It it attached to:")
        click.echo(" - "+"\n - ".join(payload["strategies"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_attach(options):
    tradehook = options.first("tradehook")
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=tradehook))

    payload = {"strategies": data['strategies']}

    strategy = options.first("strategy")
    if strategy:
        payload["strategies"].append(strategy)
    else:
        strategies = {}
        supported_strategies, errors = remote.api.get("/strategies")
        for strategy in supported_strategies:
            strategies[strategy['strategy_id']] = strategy["name"]

        curr_strategies = {}
        for strat in data['strategies']:
            curr_strategies[strat] = strategies[strat]

        if curr_strategies:
            click.echo(click.style("\nWARNING: ", fg="red"), nl=False)
            click.echo("This will reset your existing settings!")
            click.echo("\nTo attach the Tradehook to a strategy without changing existing settings, use:")
            click.echo(f"$ tctl tradehooks attach --tradehook {tradehook} --strategy " + click.style("<STRATEGY_ID>", fg="yellow"))
            click.echo("")

            proceed = inputs.confirm("Continue?", default=False)
            if not proceed:
                click.echo("Aborted")
                return
            click.echo("")

        # return
        payload['strategies'] = inputs.checkboxes(
            "Assign Tradehook to", list(strategies.keys()))

    payload["strategies"] = list(set(payload["strategies"]))

    if not payload["strategies"]:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Select at least one strategy.")

    data, errors = remote.api.post(
        f"/tradehook/{tradehook}/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if strategy:
        utils.success_response(
            f"The Tradehook `{tradehook}` was attached to the `{strategy}` strategy.")
        click.echo("\nIt is now assigned to the following strategies:")
    else:
        utils.success_response(
            f"The Tradehook `{tradehook}` is now attached to:")
    click.echo(" - "+"\n - ".join(payload["strategies"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_detach(options):
    tradehook = options.first("tradehook")
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=tradehook))

    payload = {"strategies": data['strategies']}

    strategy = options.first("strategy")
    if strategy:
        if strategy in payload["strategies"]:
            payload["strategies"] = [s for s in payload["strategies"] if s != strategy]
        else:
            click.echo(click.style("\nFAILED", fg="red"))
            click.echo(f"The tradeook is not attached to {strategy}.")
            return
    else:
        strategies = {}
        supported_strategies, errors = remote.api.get("/strategies")
        for strategy in supported_strategies:
            strategies[strategy['strategy_id']] = strategy["name"]

        curr_strategies = {}
        for strat in data['strategies']:
            curr_strategies[strat] = strategies[strat]

        if curr_strategies:
            click.echo(click.style("\nWARNING: ", fg="red"), nl=False)
            click.echo("This will reset your existing settings!")
            click.echo("\nTo detach the Tradehook to a strategy without changing existing settings, use:")
            click.echo(f"$ tctl tradehooks detach --tradehook {tradehook} --strategy " + click.style("<STRATEGY_ID>", fg="yellow"))
            click.echo("")

            proceed = inputs.confirm("Continue?", default=False)
            if not proceed:
                click.echo("Aborted")
                return
            click.echo("")

        # return
        payload['strategies'] = inputs.checkboxes(
            "Assign Tradehook to", list(strategies.keys()))

    payload["strategies"] = list(set(payload["strategies"]))

    if not payload["strategies"]:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Select at least one strategy.")

    data, errors = remote.api.post(
        f"/tradehook/{tradehook}/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if strategy:
        utils.success_response(
            f"The Tradehook `{tradehook}` was removed from the `{strategy}` strategy.\nIt is now assigned to:")
    else:
        utils.success_response(
            f"The Tradehook `{tradehook}` is now attached to:")
    click.echo(" - "+"\n - ".join(payload["strategies"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_delete(options):
    tradehook = options.first("tradehook")
    remote.api.delete("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    utils.success_response(
        f"The tradehook `{tradehook}` was removed from your account")
