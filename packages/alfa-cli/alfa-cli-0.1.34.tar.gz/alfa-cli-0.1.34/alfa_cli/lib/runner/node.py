import json
import os
import re
import subprocess
from alfa_sdk.common.exceptions import AlfaConfigError


class NodeRunner:
    def __init__(self, function_config, function_name="invoke", function_type="algorithm"):
        self.function_config = function_config
        self.function_name = function_name
        self.function_type = function_type

    #

    def run(self, problem, to_profile, profile_sort):
        arguments = self.map_problem_to_arguments(problem)
        node_function = self.generate_node_function(arguments)
        if to_profile:
            pass

        output = subprocess.check_output(["node", "-e", node_function])
        decoded_output = output.decode("utf-8")
        output_lines = [line for line in decoded_output.split("\n") if line != ""]
        for line in output_lines[:-1]:
            print(line)
        return output_lines[-1]

    #

    def extract_function_args(self):
        module_name, _ = self.get_handler_location()
        with open(f"{module_name}.js", "r") as handler_file:
            func = handler_file.read()
            func = re.sub(r"((\/\/.*$)|(\/\*[\s\S]*?\*\/))", "", func)
            func = re.sub(r"(\r\n\t|\n|\r\t)", "", func)
            func = func.strip()
            func = re.findall(r"(?:\w*?\s?function\*?\s?\*?\s*\w*)?\s*(?:\((.*?)\)|([^\s]+))", func)
            arguments = [f[0] for f in func if f[0] != ""]
            if len(arguments) == 0:
                return []
            arguments = arguments[0]
            arguments = arguments.split(",")
            arguments = [arg.strip() for arg in arguments]
            arguments = [parse_argument(arg) for arg in arguments]
            return arguments

    def generate_node_function(self, arguments):
        module_name, function_name = self.get_handler_location()
        dependency_path = os.path.join(os.getcwd(), self.function_name, "node_modules").replace(
            "\\", "\\\\"
        )
        return f"""
            module.paths.push('{dependency_path}');
            const {{ {function_name}: run }} = require('{module_name}');

            if (run.constructor.name === 'AsyncFunction') {{
                run(...{json.dumps(arguments)})
                    .then((res) => console.log(JSON.stringify(res)))
                    .catch((err) => {{
                        console.error(err);
                        process.exit(1);
                    }})
            }} else {{
                res = run(...{json.dumps(arguments)})
                console.log(JSON.stringify(res));
            }}

            process
                .on('unhandledRejection', (err) => {{
                    console.error(err);
                    process.exit(1);
                }})
                .on('uncaughtException', (err) => {{
                    console.error(err);
                    process.exit(1);
                }});
        """.replace(
            "'", '"'
        )

    #

    def get_handler_definition(self, function_config):
        ERROR_MESSAGE = "invoke function handler not defined"

        func = function_config.get("function")
        if not func:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        handler = func.get("handler")
        if not handler:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        return handler

    def get_handler_parameters(self, function_config):
        function_config_function = function_config.get("function")
        if function_config_function:
            function_config_parameters = function_config_function.get("parameters")
            if function_config_parameters:
                return function_config_parameters

        return self.extract_function_args()

    def get_handler_location(self):
        """
        Gets the location (consisting of the module name and the function name) of the handler
        function.
        """
        handler_definition = self.get_handler_definition(self.function_config)
        function_name = handler_definition.split(".")[-1]
        if self.function_type == "algorithm":
            return (
                os.path.join(
                    os.getcwd(), self.function_name, *handler_definition.split(".")[:-1]
                ).replace("\\", "\\\\"),
                function_name,
            )
        if self.function_type == "integration":
            root = self.function_config.get("function").get("root", "app")
            return (
                os.path.join(os.getcwd(), root, *handler_definition.split(".")[:-1]).replace(
                    "\\", "\\\\"
                ),
                function_name,
            )

    def map_problem_to_arguments(self, problem):
        parameters = self.get_handler_parameters(self.function_config)

        if type(problem) is not dict:
            try:
                problem = json.loads(problem)
            except ValueError:
                raise ValueError("Problem must be a valid JSON string or a dict.")

        return self.get_parameter_values(parameters, problem)

    def get_parameter_values(self, parameters, problem):
        arguments = []

        for parameter in parameters:
            if isinstance(parameter, dict):
                for arg, default_value in parameter.items():
                    arguments.append(problem.get(arg, default_value))
            elif problem.get(parameter):
                arguments.append(problem.get(parameter))

        return arguments


def parse_argument(arg):
    name = arg.split("=")[0].strip()
    value = arg.split("=")[1].strip() if len(arg.split("=")) == 2 else None
    return {name: value}
