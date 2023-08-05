import os
import json
import timeit

from alfa_cli.common.helpers.file import extract_dir
from alfa_cli.common.helpers.snapshot import compare_output
from alfa_cli.common.exceptions import AlfaCliError

DEFAULT_TESTS_TOLERANCE = 1.0
DEFAULT_TESTS_DIR = "tests"


class LocalTester:
    def __init__(self, runner, environment_name):
        self.runner = runner

        if environment_name is None:
            environment_name = '//only-get-root-files//'

        tests_path = os.path.join(".", DEFAULT_TESTS_DIR)
        self.files = extract_dir(tests_path, prefix=environment_name, ext=".json")

    def start(self):
        res = []
        for testcase in self.files:
            res.append(self._execute(testcase))
        
        errors = len([x for x in res if x['success'] is False])
        return {
            "success": errors == 0,
            "passed": len(res) - errors,
            "failed": errors,
            "result": res,
        }

    def _execute(self, testcase):
        res = {}
        name = "Unnamed test"
        start = timeit.default_timer()

        try:
            testcase = json.loads(testcase)
            name = testcase.get("name", name)
            if "input" not in testcase or "output" not in testcase:
                raise AlfaCliError(message="Input/output missing from testcase json.")

            res = self.runner.run(testcase['input'])
            res = getattr(res, "result", res)
        except Exception as err:
            err = getattr(err, "message", repr(err))
            return {"name": name, "success": False, "error": err}

        runtime = (timeit.default_timer() - start) * 1000
        tolerance = testcase.get("tolerance", DEFAULT_TESTS_TOLERANCE)
        match = compare_output(res, testcase["output"])

        match['success'] = True
        if match['similarity'] < min(tolerance, 1):
            match['success'] = False
            match['error'] = f"Similarity less than {tolerance}"

        return { "name": name, "runtime": runtime, **match }