import re
import os
import click
import PyInquirer
from alfa_cli.config import algorithm

FUNCTIONS = algorithm.initialization.functions
OPTIONS = algorithm.initialization.specification
VALID_OBJ_TYPES = ["algorithm", "integration"]


def generate_specification(obj_type="algorithm"):
    if obj_type not in VALID_OBJ_TYPES:
        raise ValueError(f"Cannot generate specification for {obj_type}")

    specification = {}
    specification["name"] = _prompt_field(
        f"{obj_type.title()} name", default=os.path.basename(os.getcwd())
    )
    if obj_type == "algorithm":
        specification["id"] = _prompt_field(f"{obj_type.title()} ID")
    specification["environment"] = _prompt_field("Environment name", default="production")
    specification["version"] = "0.1.0"
    specification["description"] = _prompt_field("Description")
    specification["functions"] = _generate_functions_specification(obj_type)
    return specification


#


def _generate_functions_specification(obj_type):
    return [
        _generate_function_specification(obj_type, function_type)
        for function_type in _get_function_types_to_generate(obj_type)
    ]


def _get_function_types_to_generate(obj_type):
    if obj_type == "algorithm":
        for function_type in FUNCTIONS.keys():
            to_generate = FUNCTIONS[function_type].required or _prompt_commit(
                f"Do you want to define a {_pprint_func(function_type)} function?"
            )
            if to_generate:
                yield function_type
    else:
        while _prompt_commit("Do you want to add a new function to the integration?"):
            yield _prompt_field("Function name")


def _generate_function_specification(obj_type, function_type):
    provider_spec = {}
    provider_spec["architecture"] = _prompt_list(
        f"Architecture of the {_pprint_func(function_type)} function", OPTIONS.architectures.keys()
    )
    provider_spec["runtime"] = _prompt_list(
        f"Runtime of the {_pprint_func(function_type)} function", OPTIONS.runtimes
    )
    provider_spec["timeout"] = _round_timeout(
        _prompt_field(
            f"Timeout of the {_pprint_func(function_type)} function", type=int, default=900
        ),
        provider_spec["architecture"],
    )
    provider_spec["instance"] = _generate_instance_specification(
        function_type, provider_spec["architecture"]
    )

    handler = "main.run"
    if obj_type == "integration":
        handler = _prompt_field("Function handler", default="handlers/{}.run".format(function_type))
    function_spec = {"handler": handler}

    if obj_type == "algorithm" and function_type == "search":
        search_options = {}
        while True:
            key = _prompt_field("Search option name")
            if not key:
                break
            search_options[key] = []
            while True:
                value = _prompt_field(f"{key.title()} search option value")
                if not value:
                    break
                search_options[key].append(value)
        print("")  # Add whiteline after the "search option" prompts and the next function prompt
        if search_options:
            function_spec["options"] = search_options

    package_spec = {"exclude": []}
    if function_type == "build":
        package_spec["exclude"].append("**/.instances/**")
    if provider_spec["runtime"] == "python":
        package_spec["exclude"].append("**/venv/**")
        package_spec["exclude"].append("**/__pycache__/**")
    if provider_spec["runtime"] == "node":
        package_spec["exclude"].append("**/node_modules/**")

    return {
        function_type: {
            "provider": provider_spec,
            "function": function_spec,
            "package": package_spec,
        }
    }


def _generate_instance_specification(function_type, architecture):
    instance_spec = {}
    for setting, values in OPTIONS.architectures[architecture].settings.items():
        if isinstance(values, dict):
            values = _get_setting_values(values, instance_spec)
        instance_spec[setting] = _prompt_list(
            f"{setting.title()} for the {function_type} function", values
        )

    return instance_spec


#


def _prompt_field(text, type=str, default=""):
    """Prompt the user to fill in the values in a field and return the value"""
    return click.prompt(text, type=type, default=default)


def _prompt_list(text, choices):
    """Prompt the user to select one item from a list of options and return the selected value"""
    # PyInquirer only accepts strings, so we store the types of the choices, convert every choice to
    # a string and convert the selected value back to its type.
    types = {str(choice): type(choice) for choice in choices}
    choices = [str(choice) for choice in choices]
    questions = [{"type": "list", "name": "value", "message": text, "choices": choices}]
    value = PyInquirer.prompt(questions)["value"]
    return types[value](value)


def _prompt_commit(text):
    return click.confirm(text)


#


def _round_timeout(timeout, architecture):
    return min(max(0, timeout), OPTIONS.architectures[architecture].timeout.max)


def _get_setting_values(settings, instance_spec):
    for setting, values in settings.items():
        key, value = setting.split("==")
        if str(instance_spec[key]) == value:
            return values

    raise ValueError("Invalid instance specification.")


#


def _pprint_func(function_type):
    return "-".join(re.sub(r"([A-Z])", r" \1", function_type).split()).lower()
