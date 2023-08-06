
import ujson
import click
import sys
import re
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from tabulate import tabulate
import pandas as pd
from numpy import nan as npnan
from datetime import datetime, timedelta
import platform
from base64 import b64encode as _b64encode, b64decode as _b64decode
from uuid import getnode
from decimal import Decimal
from . import remote
from . import inputs


def fillna(x, as_decimal=False):
    if x in ["", None, "NaT", "NaN", pd.NaT, npnan]:
        return 0.00 if as_decimal else 0
    if as_decimal:
        return "{:,.2f}".format(Decimal(x))
    return x


def success_response(msg):
    if platform.system() == "Darwin":
        click.echo(click.style("\nSUCCESS 🎉\n", fg="green"))
    else:
        click.echo(click.style("\nSUCCESS ✔\n", fg="green"))
    click.echo(msg.strip())


def to_decimal(num):
    if not num:
        return num
    parts = str(num).split('.')
    fmt = '{:,.0f}'
    if len(parts) > 1:
        fmt = "{" + f':,.{len(parts[1])}f' +"}"
    return fmt.format(Decimal(num))


def to_table(data, tablefmt="psql", missingval="-",
             showindex=False, hide=[], showheaders=True, floatfmt=".2f"):
    def tabulate_rename(string):
        dictionary = {
            "Daytrade Count ": "Day Trade Count",
            "Daytrading Buying Power ": "Day Trade Buying Power  ",
            "Regt": "RegT",
            "Sma": "SMA",
            "Pnl": "P&L",
            " Id": " Id",
            "True": "Yes ",
            "False": "No   ",
            "Ecn": "ECN",
            "Tuid": "TUID",
            "Tsid": "TSID",
            "Figi": "FIGI",
            "Sic": "SIC",
            "Mic ": "MIC ",
            " nan ": " -   ",
            " Tif ": " TIF ",
            "Day P&L Pct": "  Day P&L %",
            "P&L Pct": "  P&L %",
            "Broker replied with: null": "Broker: bad credentials  ",
        }
        for k, v in dictionary.items():
            string = string.replace(k, v)

        return string.replace("IDentifiers", "Identifiers")

    def draw(values, headers, missingval, tablefmt, showindex, showheaders):
        if showheaders:
            return "\n" + tabulate_rename(tabulate(
                values, headers=headers,
                missingval=missingval, tablefmt=tablefmt, showindex=showindex,
                floatfmt=floatfmt))

        return "\n" + tabulate_rename(tabulate(
                values,
                missingval=missingval, tablefmt=tablefmt, showindex=showindex,
                floatfmt=floatfmt))

    if isinstance(data, dict):
        clean_data = {}
        for k, v in data.items():
            if k not in hide:
                clean_data[k] = v
        data = clean_data
        return draw(
            data.values(), headers=data.keys(),
            missingval=missingval, tablefmt=tablefmt,
            showindex=showindex, showheaders=showheaders
        )
    elif isinstance(data, pd.DataFrame):
        return draw(
            data, headers="keys",
            missingval=missingval, tablefmt=tablefmt,
            showindex=showindex, showheaders=showheaders
        )

    headers = []
    if isinstance(data, list):
        clean_data = []
        for item in data:
            tmp = {}
            for k, v in item.items():
                if k not in ["url"]:
                    tmp[k] = v
            clean_data.append(tmp)
        data = clean_data

        headers = data[0].keys()
        values = [item.values() for item in data if item not in hide]
    elif isinstance(data, dict):
        clean_data = {}
        for k, v in data.items():
            if k not in hide:
                clean_data[k] = v
        data = clean_data
        headers = data.keys()
        values = data.values()

    headers = [col.replace("_", " ").title() for col in headers]
    return draw(
            values, headers=headers,
            missingval=missingval, tablefmt=tablefmt,
            showindex=showindex, showheaders=showheaders
        )


def to_json(obj, errors=None):
    if isinstance(errors, list):
        obj = {
            "errors": errors,
            "data": obj
        }
    json_str = ujson.dumps(obj, indent=4, sort_keys=True)
    return "\n" + highlight(
        json_str.replace("\/", "/"), JsonLexer(), TerminalFormatter()
    ).strip().replace(
            "Broker replied with: null",
            "Broker replied with: null / bad credentials")


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class dictx(dict):
    def first(self, key, default=None):
        value = self.get(key)
        if not value:
            return default
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return value

    def last(self, key, default=None):
        value = self.get(key)
        if not value:
            return default
        if isinstance(value, list) and len(value) > 0:
            return value[-1]
        return value

    def nth(self, key, loc, default=None):
        value = self.get(key)
        if not value:
            return default
        if isinstance(value, list) and len(value) > loc:
            return value[loc]
        return value


class args_actions(dict):
    def __init__(self, root=False):
        super().__init__()
        self[":root:"] = root

    @staticmethod
    def add_symlinks(commands):
        # add shortcuts
        if "list" in commands:
            commands["ls"] = commands["list"]
        if "update" in commands:
            commands["patch"] = commands["update"]
        if "delete" in commands:
            commands["rm"] = commands["delete"]
        return commands

    def _add(self, commands, rule, new_val):
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            if command not in self:
                self[command] = {}
            self[command][rule] = new_val

    def add_required(self, commands, new_val):
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            if command not in self:
                self[command] = {}
            self[command]["required"] = new_val

    def add_optional(self, commands, new_val):
        if isinstance(commands, str):
            commands = [commands]

        for command in commands:
            if command not in self:
                self[command] = {}
            self[command]["optional"] = new_val

    def add_flags(self, commands, new_val):
        if isinstance(commands, str):
            commands = [commands]

        for command in commands:
            if command not in self:
                self[command] = {}
            self[command]["flags"] = new_val


def options_validator(args, command, rules={}):
    if len(args) == 0 or args[0] not in command:
        if not rules.get(":root:"):

            uniques = {}
            for k, v in command.items():
                v = v.strip()
                if not uniques.get(v):
                    uniques[v] = []
                uniques[v].append(k)

            maxlen = 0
            cmds = {}
            for k, v in uniques.items():
                v = '|'.join(sorted(v, key=len, reverse=True))
                cmds[v] = k
                if len(v) > maxlen:
                    maxlen = len(v)
            cmd = []
            for k, v in cmds.items():
                kk = k
                for x in range(maxlen - len(k)):
                    kk += ' '
                cmd.append(f"{kk}  {v}")

            if len(args) > 0:
                click.echo(f"Invalid option (`{args[0]}`)")

            click.echo("Usage: tctl {command} ACTION [OPTIONS]...".format(
                command=sys.argv[1]))
            click.echo("\nAvailable actions:\n\n - {commands}".format(
                    commands='\n - '.join(cmd)))
            sys.exit(0)

    if not args and rules.get(":root:"):
        rules = {}
        args = [":root:"]

    args = list(args)
    command = args[0]
    del args[0]

    optional = {}
    required = {}
    flags = {}

    if "list" in rules:
        rules["ls"] = rules.get("list")
    if "delete" in rules:
        rules["rm"] = rules.get("delete")

    for rule, options in rules.items():
        if command == rule:
            required = options.get("required", {})
            optional = options.get("optional", {})
            flags = options.get("flags", {})
            return command, args_parser(args, required, optional, flags)

    return command, args_parser(args, required, optional, flags)


def args_parser(args, required={}, optional={}, flags={}):
    args = " " + " ".join(args)
    flags["raw"] = ["--raw"]

    _flags = {}
    for key, flag_opt in flags.items():
        _flags[key] = []
        for flag in flag_opt:
            flag = f" {flag}"
            _flags[key].append(flag in args)
            args = args.replace(flag, "")
        _flags[key] = any(_flags[key])

    regex = []
    if required:
        for key, options in required.items():
            if len(options) > 1:
                args = args.replace(f' {options[0]} ', f' {options[1]} ')
                regex.append(options[1])
            regex.append(options[0])

    if optional:
        for key, options in optional.items():
            if len(options) > 1:
                args = args.replace(f' {options[0]} ', f' {options[1]} ')
                regex.append(options[1])
            regex.append(options[0])

    regex = "|".join(regex)
    pattern = f'(\s({regex})[=|\s]([:.a-zA-Z0-9_-]+))'
    pairs = re.findall(pattern, args, re.MULTILINE)

    options = {}
    for k, v in [pair[1:3] for pair in pairs]:
        options.setdefault(k.replace('-', ''), []).append(v)

    missing = []
    for item in required:
        if item not in options:
            missing.append(item)

    if missing:
        raise click.UsageError(
            "Missing required options: `--{missing}`".format(
                missing='`, `--'.join(missing)))

    for k, v in _flags.items():
        options[k] = v

    return dictx(options)


def parse_date(timestamp):
    timestamp = str(timestamp)

    if timestamp.isdigit():
        timestamp_int = int(timestamp)
        if len(timestamp) == 19:
            timestamp = datetime.utcfromtimestamp(timestamp_int / 1e9)
        elif len(timestamp) == 16:
            timestamp = datetime.utcfromtimestamp(timestamp_int / 1e6)
        elif len(timestamp) == 13:
            timestamp = datetime.utcfromtimestamp(timestamp_int / 1e3)
        elif len(timestamp) == 8:
            try:
                timestamp = datetime.strptime(timestamp, '%Y%m%d')
            except ValueError:
                click.echo("ERROR: Unrecognizable date/time format")
                sys.exit()
        else:
            timestamp = datetime.utcfromtimestamp(timestamp_int)
    else:
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except ValueError:
            return None, None

    if timestamp.year == 1970:
        click.echo("ERROR: Unrecognizable date/time format")
        sys.exit()

    return timestamp.strftime(
        "%Y-%m-%d %H:%M:%S.%f").replace(" 00:00:00.000000", ""), timestamp


def obfuscate(byt, password):
    mask = password.encode()
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))


def encrypt(txt):
    hash_str = hex(getnode())
    return _b64encode(obfuscate(txt.encode(), hash_str)).decode()


def decrypt(txt):
    hash_str = hex(getnode())
    return obfuscate(_b64decode(txt.encode()), hash_str).decode()


def track(anon=False):
    headers = {} if anon else remote.bearer_token()
    remote.post("/sdk/installed", json={
        "sdk": "tctl",
        "mac": getnode(),
        "os": {
            "name": platform.system(),
            "version": platform.release()
        }
    }, headers=headers)


def virtual_account_payload(mode):
    if mode == "broker":
        return {}

    payload = {}

    if mode in ["backtest", "fwdtest"]:
        click.echo(click.style("NOTE: ", fg="green"), nl=False)
        click.echo("Your strategy is in backtest mode.")
        click.echo(
            'Please provide "account" information to start a backtest:\n')
    elif mode == "paper":
        click.echo(
            'Please set up your paper account information:\n')

    payload["currency"] = "USD"
    # payload["currency"] = inputs.option_selector(
    #     "Account base currency", [
    #         "USD", "EUR", "GBP", "INR", "CHF", "JPY", "RMB", "RUB", "BTC"])

    default_balance = {
        "USD": ["$", 1000000],
        "EUR": ["€", 1000000],
        "GBP": ["£", 1000000],
        "INR": ["₹", 1000000],
        "CHF": ["₣", 1000000],
        "JPY": ["¥", 100000000],
        "RMB": ["$", 1000000],
        "RUB": ["₽", 1000000],
        "BTC": ["BTC", 100]
    }.get(payload["currency"], ["$", 1000000])

    pretty_default_balance = "{:,.0f}".format(default_balance[1])

    payload["start_balance"] = inputs.number(
        f"Starting balance ({pretty_default_balance} {payload['currency']})",
        validate=lambda _, x: re.match(re.compile(r'((\d+(\.\d+)?)|)'), x),
        default=default_balance[1])

    initial_margin = 1 if payload["currency"] == "BTC" else 4

    margin = inputs.confirm("Is this a margin account?", default=True)
    if not margin:
        payload["initial_margin"] = 1
        payload["shorting_enabled"] = False
    else:
        payload["initial_margin"] = inputs.integer(
            f"Allowed margin ({initial_margin})",
            validate=lambda _, x: re.match(re.compile(r'((\d+)|)'), x),
            default=initial_margin)

        payload["shorting_enabled"] = inputs.confirm(
            "Shorting Allowed?", default=True)

    # --- start date ---
    if mode != "paper":
        start_date = "2010-01-03"
        payload["start_date"] = inputs.text(
            f"Backtest start date ({start_date})",
            validate=lambda _, x: re.match(re.compile(r'((\d{4}-\d{2}-\d{2})|)'), x),
            default=start_date)

        # --- end date ---
        todayDate = datetime.today()
        if todayDate.day < 25:
            todayDate -= timedelta(days=7)
        end_date = todayDate.replace(day=1).strftime("%Y-%m-%d")

        payload["end_date"] = inputs.text(
            f"Backtest end date ({end_date})",
            validate=lambda _, x: re.match(re.compile(r'((\d{4}-\d{2}-\d{2})|)'), x),
            default=end_date)

    return payload
