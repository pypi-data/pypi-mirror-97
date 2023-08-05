from alfa_cli.lib.trainer.response import handle_build_response
from alfa_cli.common.exceptions import AlfaCliError


def build(build_configuration, runners, data):
    search_result = _get_search_result(runners["search"], build_configuration, data)
    score_result, scores_log = _compute_scores(
        runners["search"], runners["score"], build_configuration, search_result
    )

    built_instance = _build_instance(runners["build"], build_configuration, score_result)
    built_instance["scores"] = scores_log

    return built_instance


def _get_search_result(runner, build_configuration, data, *, scores=None):
    search_options = build_configuration.get("searchOptions")
    build_arguments = build_configuration.get("arguments")

    payload = {
        "searchOptions": search_options,
        "buildArguments": build_arguments,
        "data": data,
        "scores": scores,
    }
    return runner.run(payload)


def _compute_scores(search_runner, score_runner, build_configuration, search_result):
    count = 0
    scores_log = []

    while not "build" in search_result.keys() and count < 5:
        scores = _compute_score(score_runner, build_configuration, search_result)
        if not scores:
            raise AlfaCliError(message="No scores computed.")

        scores_log = scores_log + [
            {
                "options": _extract_options_from_parameters(
                    score["parameters"], build_configuration.get("arguments")
                ),
                "result": score["result"],
            }
            for score in scores
        ]

        search_result = _get_search_result(search_runner, build_configuration, None, scores=scores)
        count = count + 1

    if not search_result.get("build"):
        raise AlfaCliError(message="No best build options found after 5 iterations.")

    return search_result["build"], scores_log


def _compute_score(runner, build_configuration, search_result):
    result = []
    for payload in search_result["score"]:
        if "arguments" in build_configuration:
            payload = {**build_configuration["arguments"], **payload}
        result.append({"result": runner.run(payload), "parameters": payload})
    return result


def _build_instance(runner, build_configuration, score_result):
    payload = {
        **score_result,
        "algorithmEnvironmentId": build_configuration["algorithmEnvironmentId"],
        "tag": build_configuration["tag"],
    }
    if "arguments" in build_configuration:
        payload = {**build_configuration["arguments"], **payload}

    instance = runner.run(payload)
    built_instance = handle_build_response(payload, instance)
    built_instance["buildOptions"] = _extract_options_from_parameters(
        payload, build_configuration.get("arguments")
    )
    return built_instance


def _extract_options_from_parameters(parameters, build_arguments):
    parameters_to_filter = ["data", "algorithmEnvironmentId", "tag"]

    if not build_arguments:
        build_arguments = {}
    return {
        key: value
        for key, value in parameters.items()
        if key not in parameters_to_filter and key not in build_arguments.keys()
    }
