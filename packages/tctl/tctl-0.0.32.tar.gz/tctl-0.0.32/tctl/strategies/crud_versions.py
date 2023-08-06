
import click
import sys
import ujson
from base64 import b64encode as _b64encode
from pathlib import Path
from .. import utils
from .. import inputs
from .. import remote

from base64 import b64decode as _b64decode
import numpy as np
import pandas as pd
pd.options.display.float_format = '{:,}'.format


STRATEGY_FILES = {
    "python2": "strategy.py",
    "python3": "strategy.py",
    "node": "strategy.js",
    "php": "strategy.php",
    "go": "strategy.go",
    "ruby": "strategy.rb",
    "java11": "strategy.java",
    "java8": "strategy.java",
    "csharp": "strategy.cs"
}

LANGS = {
    "python3": "Python 3",
    "python2": "Python 2",
    "node": "Node JS",
    "go": "Go land",
    "csharp": "C-Sharp",
    "php": "PHP 7",
    "ruby": "Ruby",
    "java8": "Java 8",
    "java": "Java 11"
}
LANGUAGES = list(LANGS.values())
LANGUAGE_KEYS = list(LANGS.keys())

def strategy_deploy(options):
    strategy = options.first("strategy")
    db_strategy = remote.api.get("/strategy/{strategy}".format(
        strategy=strategy))
    click.echo("")

    lang = options.get("lang")
    show_lang_selector = (lang is None) or (
        isinstance(lang, list) and
        lang[0] in LANGUAGES and
        lang[0] not in ["python3", "python2", "node"])

    if not show_lang_selector:
        lang = lang[0]
    else:
        if db_strategy[0].get("mode").lower() == "backtest":
            click.echo("-----------------------------")
            click.echo(click.style("PLEASE NOTE:", fg="red"))
            click.echo(
                "Currently, only Python and Node are supported by the backtester.")
            click.echo("-----------------------------\n")
        lang = inputs.option_selector(
            "Language", LANGUAGES
        ).replace(" ", "").replace("-", "").lower()

    # --- future ---
    # path = inputs.path("Path to code directory", validator="directory")

    # --- now ---
    strategy_file_found = False
    while not strategy_file_found:
        strategy_file = inputs.path(
            "Path to `{file}`".format(file=STRATEGY_FILES[lang]), validator="file")
        strategy_file_found = Path(strategy_file).exists()

    path = Path(strategy_file).parents[0]
    dependencies = []
    if "python" in lang:
        dep_file = 'requirements.txt'
        req_file = path / dep_file
    elif "node" in lang:
        dep_file = 'package.json'
        req_file = path / dep_file

    if req_file and req_file.is_file():
        if inputs.confirm(
                f"Found dependencies file `{dep_file}`. Import it?",
                default=True):
            dependencies = _read_dependencies(lang, str(path))

    # --- continue ---
    comment = inputs.text("Comment (optional)")
    active = inputs.confirm("Activate this version?", default=True)

    payload = {
        # "code": _prepare_deploy(lang, path),
        "code": _read_file(strategy_file),
        "dependencies": dependencies,
        "lang": lang,
        "comment": comment,
        "active": active,
    }

    # print(utils.to_json(payload))
    # return

    data, errors = remote.api.post(
        "/strategy/{strategy}/versions".format(strategy=strategy),
        json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"Strategy code v.{data['version']} was deployed successfully.")

    if active:
        click.echo(f"""
NOTE: If you haven't already, attach a Tradehook
to this strategy and start your strategy using:

$ tctl strategies start --strategy {strategy}""")


def _prepare_deploy(lang, directory):
    files = _read_files(directory, STRATEGY_FILES[lang])
    dependencies = _read_dependencies(lang, directory)
    return {
        # "files": files,
        "code": files[STRATEGY_FILES[lang]],
        "dependencies": dependencies,
        "lang": lang
    }


def _read_files(directory, required):
    ignore_list = """
        node_modules
        .git
        __pycache__
        tests
        docs
        examples
        demo
        .sql
        .md
        .DS_Store
        .env
        requirements.txt
        package.json
        .sh
        .loc
        vendor/
        """.strip().split()

    files = {}
    for path in Path(directory).glob("*"):
        if path.is_file():
            include = True
            for ignore in ignore_list:
                if ignore in str(path):
                    include = False
                    break
            if include:
                files[path.name] = _read_file(path)

    if required not in files.keys():
        click.echo(click.style("\nERROR: ", fg="red"), nl=False)
        click.echo("Cannot find a file named `{file}`".format(file=required))
        sys.exit()

    return files


def _read_file(file):
    # import chardet
    # rawdata = open(file).read()
    # encoding = chardet.detect(rawdata).get("encoding", "utf-8")
    with open(file, encoding="utf-8") as f:
        return _b64encode(f.read().encode()).decode()
    return ""


def _read_dependencies(lang, path):
    path = Path(path)
    dependencies = []

    # python
    if "python" in lang:
        req_file = path / 'requirements.txt'
        if req_file.is_file():
            with open(req_file, encoding="utf-8") as f:
                lines = [line.rstrip() for line in f]
                for line in lines:
                    line = line.replace('>', '=').replace(
                        '<', '=').replace('==', '=')
                    package, version = line.split('=')
                    dependencies.append({
                        "package": package,
                        "version": version
                    })
        return dependencies

    # node
    if "node" in lang:
        req_file = path / 'package.json'
        if req_file.is_file():
            with open(req_file, encoding="utf-8") as f:
                lines = ujson.load(f).get('dependencies', [])
                for package, version in lines.items():
                    dependencies.append({
                        "package": package,
                        "version": version.strip('^')
                    })
        return dependencies

    return dependencies










def strategy_list_versions(options):
    strategy = options.first("strategy")
    strategy_data, errors = remote.api.get(f"/strategy/{strategy}")

    data, errors = remote.api.get(f"/strategy/{strategy}/versions")
    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    click.echo(f"\nVersion history for `{strategy_data['name']}` strategy`:")

    versions = pd.DataFrame(data)
    versions["Active"] = np.where(versions["active"], '✓', '-')
    versions = versions[["Active", "version", "comment", "lang"]]

    versions["lang"] = versions["lang"].apply(lambda x: LANGS[x])
    versions["comment"] = versions["comment"].apply(lambda x: "-" if x == "" else x)
    versions.columns = [col.title() for col in versions.columns]
    click.echo(utils.to_table(versions))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_version(options):
    strategy = options.first("strategy")
    version = options.first("version")
    code = options.first("decode", False)

    strategy_data, errors = remote.api.get(f"/strategy/{strategy}")
    data, errors = remote.api.get(f"/strategy/{strategy}/version/{version}?code={str(code).lower()}")

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    if "code" in data:
        click.echo_via_pager(_b64decode(data["code"].encode()).decode())
    else:
        active = 'active' if data['active'] else 'inactive'
        click.echo(f"\n{strategy_data['name']} v.{version} ({active})")

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_activate_version(options):
    strategy = options.first("strategy")
    version = options.first("version")

    strategy_data, errors = remote.api.get(f"/strategy/{strategy}")
    data, errors = remote.api.post(f"/strategy/{strategy}/version/{version}")

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    active = 'active' if data['active'] else 'inactive'
    utils.success_response(f"{strategy_data['name']} v.{version} is now {active}!")

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

