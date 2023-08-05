import click

from alfa_sdk.common.exceptions import ResourceNotFoundError
from alfa_cli.common.exceptions import AlfaCliError
from alfa_cli.common.utils import load_or_parse
from alfa_cli.common.click import BaseCliCommand
from alfa_cli.config import algorithm as algorithm_config
from alfa_cli.lib.runner import LocalRunner
from alfa_cli.lib.tester import LocalTester


@click.command(cls=BaseCliCommand)
@click.argument("algorithm-id", type=str)
@click.argument("environment-name", type=str)
@click.argument("problem", type=str)
@click.option(
    "--return-holding-response",
    is_flag=True,
    help="If specified, ALFA will return the identifier of the request but not wait until the algorithm finishes.",
)
@click.option(
    "--include-details",
    is_flag=True,
    help="If specified, ALFA will add additional details to the response in addition to the algorithm result.",
)
@click.option(
    "--can-buffer",
    is_flag=True,
    help="If specified, ALFA will buffer the invocation when busy (instead of returning an error).",
)
@click.pass_obj
def invoke(obj, algorithm_id, environment_name, problem, **kwargs):
    """Invoke a deployed algorithm."""

    client = obj["client"]()

    #

    try:
        algorithm = client.get_algorithm(algorithm_id)
    except ResourceNotFoundError:
        raise AlfaCliError(message="Algorithm {} not found.".format(algorithm_id))

    try:
        environment = algorithm.get_environment(environment_name)
    except ResourceNotFoundError:
        raise AlfaCliError(
            message="Environment {} for algorithm {} not found.".format(
                environment_name, algorithm_id
            )
        )

    #

    try:
        problem = open(problem, "r").read()
    except:
        pass

    res = environment.invoke(problem, **kwargs)
    return obj["logger"].result(res)


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
    "--algorithm-id",
    "-a",
    type=str,
    help="If specified, the provided algorithm id will be set in the context; defaults to the algorithm id in the specification file.",
)
@click.option(
    "--environment-name",
    "-e",
    type=str,
    help="If specified, the provided environment name will be set in the context; defaults to the environment name in the specification file.",
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
def invoke_local(obj, problem, spec, algorithm_id, environment_name, profile_sort, **kwargs):
    """
    Invoke the algorithm with the problem in the working directory locally. The problem
    can be a json formatted string (needs to be enclosed by single quotes) or the location
    of a file that contains the problem.
    """
    problem = load_or_parse(problem)
    runner = LocalRunner(obj, spec, algorithm_id, environment_name)
    res = runner.run(problem, kwargs["profile"], profile_sort)
    return obj["logger"].result(res)


#


@click.command(cls=BaseCliCommand)
@click.option(
    "--spec",
    type=str,
    default=algorithm_config.defaults.specification.path,
    show_default=True,
    help="Path of the specification file.",
)
@click.option(
    "--algorithm-id",
    "-a",
    type=str,
    help="If specified, the provided algorithm id will be set in the context; defaults to the algorithm id in the specification file.",
)
@click.option(
    "--environment-name",
    "-e",
    type=str,
    help="If specified, the provided environment name will be set in the context; defaults to the environment name in the specification file.",
)
@click.pass_obj
def invoke_tests(obj, spec, algorithm_id, environment_name):
    """Invoke the algorithm tests in the working directory locally.

    The test cases must be put inside the 'tests' directory of the algorithm, and must be valid json files.
    Each test case json should contain at least an 'input' and 'output' field. The tests will invoke the algorithm
    using the test case 'input', and then compare the output with the test case 'output'."""

    #

    runner = LocalRunner(obj, spec, algorithm_id, environment_name)
    tester = LocalTester(runner, environment_name)

    #

    res = tester.start()
    return obj["logger"].result(res)
