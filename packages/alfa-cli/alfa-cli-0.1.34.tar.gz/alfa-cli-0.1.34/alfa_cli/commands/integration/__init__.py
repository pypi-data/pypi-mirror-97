import click
from alfa_sdk import IntegrationClient
from alfa_cli.common.factories import create_session
from alfa_cli.commands.integration import deploy, initialize, invoke


@click.group()
@click.pass_context
def integration(ctx):
    """Manage integrations deployed in ALFA."""
    ctx.obj["client"] = get_client


def get_client():
    session = create_session()
    return IntegrationClient(session=session)


integration.add_command(initialize.init)
integration.add_command(invoke.invoke)
integration.add_command(invoke.invoke_local)
integration.add_command(deploy.deploy)
