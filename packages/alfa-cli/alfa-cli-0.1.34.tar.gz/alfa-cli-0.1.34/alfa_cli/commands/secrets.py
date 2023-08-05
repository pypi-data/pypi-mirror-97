import click
from alfa_sdk import SecretsClient
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.common.factories import create_session


@click.group()
@click.pass_context
def secrets(ctx):
    """Store and retrieve secrets in ALFA."""
    ctx.obj["client"] = get_client


def get_client():
    session = create_session()
    return SecretsClient(session=session)


#


@secrets.command(cls=BaseCliCommand)
@click.pass_obj
def list_names(obj):
    """Retrieve list of secrets"""
    res = obj["client"]().list_names()
    return obj["logger"].result(res)


@secrets.command(cls=BaseCliCommand)
@click.argument("name", type=str)
@click.pass_obj
def fetch_value(obj, name):
    """Retrieve the value of a secret"""
    res = obj["client"]().fetch_value(name)
    return obj["logger"].result(res)


@secrets.command(cls=BaseCliCommand)
@click.argument("name", type=str)
@click.argument("value", type=str)
@click.option("-d", "--description", type=str, help="Description of the secret", default=None)
@click.pass_obj
def store_value(obj, name, value, description):
    """Save/update the value of a secret"""
    res = obj["client"]().store_value(name, value, description=description)
    return obj["logger"].result(res)


@secrets.command(cls=BaseCliCommand)
@click.argument("name", type=str)
@click.pass_obj
def remove_value(obj, name):
    """Delete a secret"""
    res = obj["client"]().remove_value(name)
    return obj["logger"].result(res)

