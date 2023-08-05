import click
from alfa_sdk import AlgorithmClient
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.common.factories import create_session


@click.group()
@click.pass_context
def resource(ctx):
    """Retrieve information on resources in ALFA."""
    ctx.obj["client"] = get_client


def get_client():
    session = create_session()
    return AlgorithmClient(session=session)


#


@resource.command(cls=BaseCliCommand)
@click.pass_obj
def algorithm_list(obj):
    """List available algorithms"""
    algorithms = obj["client"]().list_algorithms()
    res = [{"id": x["id"], "name": x["name"]} for x in algorithms]
    return obj["logger"].result(res)


@resource.command(cls=BaseCliCommand)
@click.argument("id", type=str)
@click.pass_obj
def algorithm(obj, id):
    """Retrieve information on an algorithm"""
    res = obj["client"]().get_algorithm(id)
    return obj["logger"].result(res)


#


@resource.command(cls=BaseCliCommand)
@click.argument("algorithm_id", type=str)
@click.pass_obj
def environment_list(obj, algorithm_id):
    """List environment names for a specific algorithm"""
    environments = obj["client"]().list_environments(algorithm_id)
    res = [x["id"] for x in environments]
    return obj["logger"].result(res)


@resource.command(cls=BaseCliCommand)
@click.argument("id", type=str)
@click.pass_obj
def environment(obj, id):
    """Retrieve information on an algorithm environment"""
    res = obj["client"]().get_environment(id)
    return obj["logger"].result(res)


#


@resource.command(cls=BaseCliCommand)
@click.argument("environment_id", type=str)
@click.pass_obj
def release_list(obj, environment_id):
    """List releases for an algorithm environment"""
    releases = obj["client"]().list_releases(environment_id)
    res = [
        {"id": x["id"], "version": x["version"], "status": x["status"], "active": x["active"]}
        for x in releases
    ]
    return obj["logger"].result(res)


@resource.command(cls=BaseCliCommand)
@click.argument("id", type=str)
@click.pass_obj
def release(obj, id):
    """Retrieve information on an algorithm release"""
    res = obj["client"]().get_environment(id)
    return obj["logger"].result(res)

