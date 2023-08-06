#!/usr/bin/env python

import click
from . import price_crud
from . import rates_crud


@click.group()
def cli():
    pass


# rates router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=rates_crud.options_validator)
def rates(options):
    """Retreive currency exchange rates"""
    command, options = options

    if command in ["ls", "list"]:
        rates_crud.rates_list(options)

    if command in ["info"]:
        rates_crud.rates_pair(options)


# rates router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=price_crud.options_validator)
def price(options):
    """Retreive asset's price-related information"""
    command, options = options

    if command in ["last"]:
        price_crud.last(options)

    if command in ["quote"]:
        price_crud.quote(options)

    if command in ["check"]:
        price_crud.check(options)

    if command in ["bar"]:
        price_crud.bar(options)

    if command in ["bars"]:
        price_crud.bars(options)
