from functools import wraps
import json
from pathos.multiprocessing import ProcessingPool
from alfa_sdk.common.exceptions import ValidationError


#


def get_short_environment_name(environment):
    """
    Returns the short version of the environment name that matches the format that they
    are defined in the alfa sdk.
    """
    if _contains(environment, "dev"):
        return "dev"
    if _contains(environment, "test"):
        return "test"
    if _contains(environment, "acc"):
        return "acc"
    if _contains(environment, "prod"):
        return "prod"

    raise ValidationError(error="Invalid alfa environment.")


def _contains(string, substring, case_sensitive=False):
    if not case_sensitive and string and substring:
        string = string.lower()
        substring = substring.lower()
    return string and substring in string


def load_or_parse(data):
    try:
        data = open(data, "r").read()
    except:
        pass
    return json.loads(data)


#


def processify(func):
    """
    Decorator to run a function as a process. Be sure that every argument and the return value
    is serializable. The created process is joined, so the code does not run in parallel.
    Based on: https://github.com/dgerosa/processify.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        processing_pool = ProcessingPool(1)
        arguments = ([arg] for arg in args)
        result = None
        try:
            result = processing_pool.map(func, *arguments)
        finally:
            processing_pool.close()
            processing_pool.join()
            processing_pool.clear()
        return result[0]

    return wrapper
