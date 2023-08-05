import click
from alfa_sdk import AlgorithmClient
from alfa_cli.common.factories import create_session
from alfa_cli.commands.algorithm import deploy, invoke, train, initialize


@click.group()
@click.pass_context
def algorithm(ctx):
    """Manage algorithms deployed in ALFA."""
    ctx.obj["client"] = get_client


def get_client():
    session = create_session()
    return AlgorithmClient(session=session)


algorithm.add_command(deploy.deploy)
algorithm.add_command(invoke.invoke)
algorithm.add_command(invoke.invoke_local)
algorithm.add_command(invoke.invoke_tests)
algorithm.add_command(train.train_local)
algorithm.add_command(initialize.init)
