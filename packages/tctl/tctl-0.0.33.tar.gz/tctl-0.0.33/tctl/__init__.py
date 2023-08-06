import click
import sys

from pathlib import Path
__env_path__ = Path.home() / ".tradologics"

from .env import ENVIRONMENT

if ENVIRONMENT == "dev":
    __env_path__ = Path.home() / ".tradologics-dev"

# internals
from . import version
from . import config
from . import accounts
from . import pricing
from . import universe
from . import strategies
from . import tradehooks
from . import monitors
from . import orders
from . import trading
from . import tokens
from . import upgrade
from . import me
from . import remote


if "--version" in sys.argv or "-V" in sys.argv:
    data, errors = remote.api.get("/version", halt_on_error=False)
    slug = "-dev" if ENVIRONMENT == "dev" else ""
    if data:
        click.echo(f"\nTctl {version.version}{slug} / System {data['version']}")
    else:
        click.echo(f"\nTctl {version.version}{slug}")

    click.echo("Copyrights (c) Tradologics, Inc.")
    click.echo("https://tradologics.com")
    sys.exit()


cli = click.CommandCollection(sources=[
    config.cli,
    accounts.cli,
    pricing.cli,
    universe.cli,
    strategies.cli,
    tradehooks.cli,
    monitors.cli,
    orders.cli,
    trading.cli,
    tokens.cli,
    upgrade.cli,
    me.cli,
])


__version__ = version.version
__author__ = "Tradologics, Inc"

__all__ = ['cli']
