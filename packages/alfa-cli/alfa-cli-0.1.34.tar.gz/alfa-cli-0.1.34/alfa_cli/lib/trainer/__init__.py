import json
from alfa_sdk.common.exceptions import AlfaConfigError
from alfa_sdk.common.session import Session, parse_response
from alfa_cli.common.exceptions import AlfaCliError
from alfa_cli.common.utils import load_or_parse
from alfa_cli.lib.runner import LocalRunner
from alfa_cli.lib.trainer.build_configuration import fetch_build_configuration


def initialize_runners(obj, spec_path, algorithm_id, environment_name):
    """
    Initializes the runners (based upon the specification in the specification file) that
    are used to execute the training locally. Returns one runner per function that needs
    to be executed.
    """
    search_runner = None
    try:
        search_runner = LocalRunner(obj, spec_path, algorithm_id, environment_name, "search")
    except AlfaConfigError:
        pass

    score_runner = None
    try:
        score_runner = LocalRunner(obj, spec_path, algorithm_id, environment_name, "score")
    except AlfaConfigError:
        pass

    build_runner = None
    build_runner = LocalRunner(obj, spec_path, algorithm_id, environment_name, "build")

    return {
        "search": search_runner,
        "score": score_runner,
        "build": build_runner,
    }


def fetch_data(data, build_configuration):
    """
    Loads the data if it is provided by the client. Otherwise, tries to fetch it from
    the data request that is specified in the build configuration.
    """
    if data:
        return load_or_parse(data)

    data_request = build_configuration.get("dataRequest")
    if not data_request:
        raise AlfaCliError(message="Failed to fetch data.")

    session = Session()
    return parse_response(
        session.http_session.request(
            data_request.get("method"),
            data_request.get("url"),
            params=_jsonify_query_string(data_request.get("qs")),
            json=data_request.get("body"),
        )
    )


def validate_build_configuration(build_configuration):
    """
    Validates whether the required fields are specified in the build configuration.
    """
    required_fields = ["tag", "algorithmEnvironmentId"]
    if not all(field in build_configuration.keys() and build_configuration[field] is not None for field in required_fields):
        raise AlfaCliError(message="Invalid build configuration.")

#

def _jsonify_query_string(qs):
    if not qs:
        return qs
    return {k: v if not isinstance(v, dict) else json.dumps(v) for k, v in qs.items()}
