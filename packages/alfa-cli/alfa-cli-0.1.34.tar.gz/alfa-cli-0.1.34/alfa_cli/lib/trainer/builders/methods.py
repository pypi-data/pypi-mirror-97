import operator

from alfa_cli.lib.trainer.response import handle_build_response
from alfa_cli.common.exceptions import AlfaCliError

def build(build_configuration, runners, data):
    scores = None
    method = None
    methods = build_configuration.get("methods")
    if methods and len(methods) > 0:
        scores = _compute_scores(build_configuration, runners.get("score"), data, methods)
    body, instance = _build_instance(build_configuration, runners["build"], data, scores, method)
    return handle_build_response(body, instance)


def _compute_scores(build_configuration, runner, data, methods):
    if not runner:
        if len(methods) == 1:
            return {}
        raise AlfaCliError(message="Cannot compute scores without a score function defined.")
    scores = []
    for method in methods:
        scores.append(_compute_score(build_configuration, runner, data, method))
    return {score["method"]: score["score"] for score in scores}

def _compute_score(build_configuration, runner, data, method):
    payload = {"data": data, "method": method}
    if build_configuration.get("arguments"):
        payload = {**payload, **build_configuration.get("arguments")}
    score = runner.run(payload)

    if isinstance(score, dict) and "score" in score:
        score = score["score"]
    return {"method": method, "score": score}


def _build_instance(build_configuration, runner, data, scores, method):
    score = None
    best_method = method
    if scores:
        best_method = max(scores.items(), key=operator.itemgetter(1))[0]
        score = scores[best_method]

    payload = {
        "data": data,
        "method": best_method,
        "score": score,
        "algorithmEnvironmentId": build_configuration.get("algorithmEnvironmentId"),
        "tag": build_configuration.get("tag"),
        "instanceBucket": build_configuration.get("instanceBucket"),
        "instanceKey": build_configuration.get("instancePath"),
        "instanceRegion": "eu-central-1",
        "dataRequest": build_configuration.get("dataRequest"),
        "scores": score,
    }
    if build_configuration.get("arguments"):
        payload = {**payload, **build_configuration.get("arguments")}

    instance = runner.run(payload)
    return payload, instance
