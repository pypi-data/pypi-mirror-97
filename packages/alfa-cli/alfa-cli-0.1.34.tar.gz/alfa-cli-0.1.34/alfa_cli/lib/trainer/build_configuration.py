from alfa_sdk.resources.meta import MetaUnit
from alfa_cli.common.exceptions import AlfaCliError
from alfa_cli.common.utils import load_or_parse


def fetch_build_configuration(
    build_configuration=None, algorithm_environment_id=None, tag=None, search_runner=None
):
    """
    Loads the build configuration if it has been provided; otherwise, it will fetch the build
    configuration from ALFA. Returns the build configuration with tag and algorithmEnvironmentId
    included in it.
    """
    build_configuration = _load_build_configuration(
        build_configuration, algorithm_environment_id, tag
    )
    return _format_build_configuration(
        build_configuration, algorithm_environment_id, tag, search_runner
    )


def _load_build_configuration(build_configuration, algorithm_environment_id, tag):
    """
    Loads the build configuration if it is specified. Otherwise, it tries to fetch the
    build configuration for the meta unit that is defined. If that is not possible, an
    empty dictionary is returned so that the local training can continue with the specified
    data.
    """
    if build_configuration:
        return load_or_parse(build_configuration)

    build_configuration = {}
    if not algorithm_environment_id or not tag:
        raise AlfaCliError(message="Failed to fetch build configuration.")

    meta_unit = MetaUnit(algorithm_environment_id, tag)
    if not meta_unit:
        return {}

    build_configurations = meta_unit.build_configurations
    if not build_configurations:
        return {}

    return build_configurations[0]


def _format_build_configuration(build_configuration, algorithm_environment_id, tag, search_runner):
    """
    Fills the build configuration with values that are defined by the client and formats the search
    option so that only the search options that need to be attempted are defined in the build
    configuration.
    """
    if "algorithmEnvironmentId" not in build_configuration:
        build_configuration["algorithmEnvironmentId"] = algorithm_environment_id
    if "tag" not in build_configuration:
        if tag is not None:
            build_configuration["tag"] = tag
        if "unitId" in build_configuration:
            build_configuration["tag"] = build_configuration["unitId"].split(":")[-1]
    if not search_runner or "searchOptions" in build_configuration:
        return build_configuration
    return _format_search_options(build_configuration, search_runner)


def _format_search_options(build_configuration, search_runner):
    """
    Loads the search options based on the definition in the specification file. When include and/or
    exclude search options are defined, the search options are updated to account for those.
    """
    build_configuration["searchOptions"] = search_runner.function_config["function"].get(
        "options", {}
    )
    for option_name in build_configuration["searchOptions"]:
        if option_name in build_configuration.get("includeSearchOptions", {}):
            build_configuration["searchOptions"][option_name] = build_configuration[
                "includeSearchOptions"
            ][option_name]
        elif option_name in build_configuration.get("excludeSearchOptions", {}):
            for option_value in build_configuration["excludeSearchOptions"][option_name]:
                try:
                    build_configuration["searchOptions"][option_name].remove(option_value)
                except ValueError:
                    pass
    return build_configuration
