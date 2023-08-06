#!/usr/bin/env python

import click
from .. import utils
from . import crud
from . import crud_versions


commands = {
    "list": "    Retreive list of strategies",
    "info": "    Show strategy information: --strategy|-s {STRATEGY_ID}",
    "new": "     Create new strategy",
    "update": "  Update existing strategy: --strategy|-s {STRATEGY_ID}",
    "delete": "  Delete strategy: --strategy|-s {STRATEGY_ID}",
    "deploy": "  Deploy code to a strategy --strategy|-s {STRATEGY_ID} [--lang|-l {LANGUAGE}]",
    "set-mode": "Change the mode of the strategy: --strategy|-s {STRATEGY_ID} [--mode|-m {MODE}]",
    "start": "   Starts a strategy: --strategy|-s {STRATEGY_ID}",
    "stop": "    Stops a strategy: --strategy|-s {STRATEGY_ID}",
    "set-public": "   Make a strategy public: --strategy|-s {STRATEGY_ID}",
    "set-private": "   Make a strategy private: --strategy|-s {STRATEGY_ID}",
    "status": "  Display strategy status: --strategy|-s {STRATEGY_ID} [--start {YYYY-MM-DD}] [--end {YYYY-MM-DD}]",
    "log": "     Show strategy deployment logs: --strategy|-s {STRATEGY_ID} [--lines|-l {NO=10}]",
    "report": "   Show strategy statistics: --strategy|-s {STRATEGY_ID}",
    "versions": "   Show strategy versions: --strategy|-s {STRATEGY_ID}",
    "version": "    Display strategy version: --strategy|-s {STRATEGY_ID} --version|-v {VERSION-ID} [--decode]",
    "activate": "   Activate strategy version: --strategy|-s {STRATEGY_ID} --version|-v {VERSION-ID}",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_required([
    "info", "update", "patch", "delete", "status", "log",
    "set-mode", "set-public", "set-private",
    "start", "stop", "report",  "deploy",
    "activate", "version", "versions"
], {"strategy": ["-s", "--strategy"]})
rules.add_required(["activate", "version"], {
    "version": ["-v", "--version"],
    "strategy": ["-s", "--strategy"]
    })
rules.add_flags("version", {
    "decode": ["--decode"]
})

rules.add_optional("deploy", {"lang": ["-l", "--lang"]})
rules.add_optional("set-mode", {"mode": ["-m", "--mode"]})
rules.add_optional("log", {"lines": ["-l", "--lines"]})



def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def strategies(options):
    """List, create, update, delete, deploy, start and stop strategies"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.strategies_list(options)

    elif command == "info":
        crud.strategy_info(options)

    elif command == "status":
        crud.strategy_status(options)

    elif command == "log":
        crud.strategy_log(options)

    elif command in ["update", "patch"]:
        crud.strategy_update(options)

    elif command in ["rm", "delete"]:
        crud.strategy_delete(options)

    elif command == "set-mode":
        crud.strategy_set_mode(options)

    elif command == "set-public":
        crud.strategy_set_public(options)

    elif command == "set-private":
        crud.strategy_set_private(options)

    elif command == "new":
        crud.strategy_create(options)

    elif command == "start":
        crud.strategy_start(options)

    elif command == "stop":
        crud.strategy_stop(options)

    elif command == "report":
        crud.strategy_report(options)

    elif command == "versions":
        crud_versions.strategy_list_versions(options)

    elif command == "version":
        crud_versions.strategy_version(options)

    elif command == "activate":
        crud_versions.strategy_activate_version(options)

    elif command == "deploy":
        crud_versions.strategy_deploy(options)
