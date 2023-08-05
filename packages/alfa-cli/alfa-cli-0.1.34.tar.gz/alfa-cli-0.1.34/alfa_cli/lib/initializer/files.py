import os
import yaml

from alfa_cli.config import algorithm

ARGUMENTS = algorithm.initialization.specification.arguments


def generate_files(specification, obj_type="algorithm"):
    main_folder = _create_main_folder(specification)
    for function in specification["functions"]:
        _generate_function_files(main_folder, function, obj_type)
    if obj_type == "integration" and len(specification.get("functions", [])) > 0:
        runtime = list(specification["functions"][0].values())[0]["provider"]["runtime"]
        _generate_dependency_file(os.path.join(main_folder, "app"), runtime, specification["name"])
    _generate_configuration_file(main_folder, specification)


#


def _create_main_folder(specification):
    main_folder_name = specification["name"].replace(" ", "-").lower()
    cwd_name = os.path.basename(os.getcwd())
    if main_folder_name == cwd_name:
        return "."

    os.mkdir(main_folder_name)
    return os.path.join(".", main_folder_name)


def _generate_function_files(main_folder, function, obj_type):
    for function_name, function_spec in function.items():
        function_folder = os.path.join(main_folder, function_name)
        if obj_type == "integration":
            function_folder = os.path.join(main_folder, "app")
        try:
            os.mkdir(function_folder)
        except FileExistsError:
            pass

        handler = function_spec["function"]["handler"]
        handler_filename, handler_function = handler.split(".")
        os.makedirs(os.path.join(function_folder, os.path.dirname(handler_filename)), exist_ok=True)
        runtime = function_spec["provider"]["runtime"]
        function_arguments = _generate_function_arguments(function_name, runtime)

        if obj_type == "algorithm":
            _generate_dependency_file(function_folder, runtime, function_name)
        _generate_function_file(
            runtime, function_folder, handler_filename, handler_function, function_arguments
        )


def _generate_configuration_file(main_folder, specification):
    with open(os.path.join(main_folder, algorithm.defaults.specification.path), "w") as output:
        specification.pop("name", None)
        functions = {"functions": specification.pop("functions")}

        output.writelines(yaml.dump(specification, sort_keys=False))
        output.write("\n")
        output.writelines(yaml.dump(functions, sort_keys=False))


def _generate_dependency_file(path, runtime, name):
    if runtime == "python":
        with open(os.path.join(path, "requirements.txt"), "w") as req_file:
            pass
    elif runtime == "node":
        with open(os.path.join(path, "package.json"), "w") as req_file:
            req_file.write(
                f'{{\n  "name": "{name}",\n  "version": "1.0.0",\n  "dependencies": {{\n  }}\n}}'
            )


def _generate_function_file(runtime, folder, filename, function, arguments):
    if runtime == "python":
        filename += ".py"
        with open(os.path.join(folder, filename), "w") as handler_file:
            handler_file.write(f"def {function}({arguments}):\n    # define logic here")
    elif runtime == "node":
        filename += ".js"
        with open(os.path.join(folder, filename), "w") as handler_file:
            handler_file.write(
                f"exports.{function} = function({arguments}) {{\n    // define logic here\n}};"
            )


#


def _generate_function_arguments(function_name, runtime):
    if not ARGUMENTS[function_name]:
        return ""

    function_arguments = ""
    for i, argument in enumerate(ARGUMENTS[function_name]):
        function_arguments += argument.key
        runtime_default = argument.get(f"default_{runtime}")
        space = "" if runtime == "python" else " "
        if runtime_default:
            function_arguments += f"{space}={space}{runtime_default}"
        elif argument.default:
            function_arguments += f"{space}={space}{argument.default}"
        if i < len(ARGUMENTS[function_name]) - 1:
            function_arguments += ", "
    return function_arguments
