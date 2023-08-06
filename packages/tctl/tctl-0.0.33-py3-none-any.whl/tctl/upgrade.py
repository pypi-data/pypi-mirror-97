#!/usr/bin/env python

import click
import sys
import subprocess
import requests
from xml.etree import ElementTree

from . import version
from . import inputs

from .env import ENVIRONMENT

from . import __env_path__
from datetime import datetime
import os
import dotenv
dotenv.load_dotenv(__env_path__)


def get_pip_newest_version(package):
    r = requests.get('https://pypi.org/rss/project/tctl/releases.xml')
    root = ElementTree.fromstring(r.content)
    for child in root.find('channel').find('item').iter('*'):
        if child.tag == 'title':
            return child.text
    return version.version


@click.group()
def cli():
    pass


@cli.command()
def upgrade():
    """ Upgrade tctl to the latest version """

    package = "git+https://github.com/tradologics/tctl.git@dev"

    if ENVIRONMENT != "dev":
        package = "tctl"
        has_update, latest_version = _has_new_version()
        if not has_update:
            click.echo("\nYou're using the latest version (tctl v. {v})".format(
                v=version.version))
            sys.exit(0)

        click.echo("""\nYou're running tctl version:  {curr}
Latest version available is:  {v}\n""".format(
            curr=version.version, v=latest_version))

        # if version.version == latest_version
    up = inputs.confirm("Upgrade?", default=False)

    if not up:
        raise click.Abort()

    click.echo("\nUpgrading... ", nl=False)

    process = subprocess.Popen(
        ['pip', 'install', '--upgrade', '--no-cache-dir', package],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    stdout = stdout.decode()
    stderr = stderr.decode()

    dotenv.set_key(__env_path__, "VERSION_CHECK",
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not stderr or "already up-to-date" in stdout:
        click.echo(click.style("SUCCESS", fg="green"))
        click.echo(f"\ntctl was upgraded to version {latest_version}")
        sys.exit()

    click.echo(click.style("FAILED\n", fg="red"))
    click.echo(stderr.replace("ERROR: ", "").strip())


def _has_new_version():
    latest_version = get_pip_newest_version("tctl")
    curr_version = version.version.replace('.', '')
    new_version = latest_version.replace('.', '')
    return new_version > curr_version, latest_version


def check_for_new_version():
    checked = os.getenv("VERSION_CHECK", "2020-10-19 00:00:00")
    checked = datetime.strptime(checked, "%Y-%m-%d %H:%M:%S")
    hours_since_check = (datetime.now() - checked).seconds // 3600

    if hours_since_check >= 12:
        has_update, latest_version = _has_new_version()
        if has_update:
            click.echo("\n------------------")
            click.echo(f"A new version of tctl is available (v {latest_version}). To upgrade run:")
            click.echo("   tctl upgrade")
            click.echo("------------------\n")

    dotenv.set_key(__env_path__, "VERSION_CHECK",
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

