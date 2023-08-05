import click

from alfa_cli.common.click import BaseCliCommand
from alfa_cli.common.utils import load_or_parse
from alfa_cli.config import algorithm as algorithm_config
from alfa_cli.lib.runner import LocalRunner

@click.command(cls=BaseCliCommand)
@click.argument("integration-id", type=str)
@click.argument("environment-name", type=str)
@click.argument("function-name", type=str)
@click.argument("payload", type=str)
@click.pass_obj
def invoke(obj, integration_id, environment_name, function_name, payload):
    """Invoke a deployed algorithm."""

    client = obj["client"]()

    #

    try:
        payload = open(payload, "r").read()
    except:
        pass

    res = client.invoke(integration_id, environment_name, function_name, payload)
    return obj["logger"].result(res)


#


@click.command(cls=BaseCliCommand)
@click.argument("problem", type=str)
@click.option(
    "--spec",
    type=str,
    default=algorithm_config.defaults.specification.path,
    show_default=True,
    help="Path of the specification file.",
)
@click.option(
    "--integration-id",
    "-i",
    type=str,
    help="If specified, the provided integration id will be set in the context.",
)
@click.option(
    "--environment-name",
    "-e",
    type=str,
    help="If specified, the provided environment name will be set in the context; defaults to the environment name in the specification file.",
)
@click.option(
    "--function-name",
    "-f",
    type=str,
    required=True,
    help="The provided function name will be set in the context; defaults to the environment name in the specification file.",
)
@click.option(
    "--profile",
    is_flag=True,
    help="If specified, a profiler will run and the results will be displayed.",
)
@click.option(
    "--profile-sort",
    "-ps",
    type=str,
    help="Specifies the sorting of the results displayed by the profiler; defaults to sorting by internal time. The sort options need to be provided as a comma-separated string where each option is a valid argument used by the pstats library (https://docs.python.org/3.8/library/profile.html#pstats.Stats.sort_stats)",
)
@click.pass_obj
def invoke_local(obj, problem, spec, integration_id, environment_name, function_name, profile_sort, **kwargs):
    """
    Invoke an integration function with the payload in the working directory locally. The payload
    can be a json formatted string (needs to be enclosed by single quotes) or the location
    of a file that contains the payload.
    """
    problem = load_or_parse(problem)
    runner = LocalRunner(obj, spec, integration_id, environment_name, function_name, "integration")
    res = runner.run(problem, kwargs["profile"], profile_sort)
    return obj["logger"].result(res)
