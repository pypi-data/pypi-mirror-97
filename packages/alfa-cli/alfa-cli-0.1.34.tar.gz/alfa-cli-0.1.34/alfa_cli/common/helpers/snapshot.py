import json
from collections.abc import Mapping
from alfa_cli.common.exceptions import TestError


TESTS_WILDCARD = "*"


def compare_output(output, expected):
    if output is None:
        raise TestError(message="Algorithm result is empty")
    if expected is None:
        raise TestError(message="Expected output is not provided")

    if not isinstance(expected, Mapping):
        output = {"value": output}
        expected = {"value": expected}

    #

    mismatch = match_objects(expected, output)
    total = len(match_objects(expected, output, True))
    similarity = 1 if total == 0 else (1 - len(mismatch) / total)
    diff = [
        {"path": path, "expected": get(expected, path), "received": get(output, path)}
        for path in mismatch
    ]

    return {
        "success": len(mismatch) == 0,
        "similarity": similarity,
        "matches": total - len(mismatch),
        "mismatches": len(mismatch),
        "diff": diff,
    }


def match_objects(obj1, obj2, total=False):
    keys = [find_mismatch(entry, obj2, total) for entry in obj1.items()]
    flattened = [item for sublist in keys for item in sublist]
    return flattened


def find_mismatch(entry, obj, total):
    (key, val) = entry

    if isinstance(val, list):
        val = list_to_dict(val)
    if isinstance(obj, list):
        obj = list_to_dict(obj)

    # ITERATION

    if isinstance(val, Mapping):
        if len(val.keys()) != 0:
            keys = match_objects(val, obj.get(key), total)
            return [f"{key}.{x}" for x in keys]

    # CONDITION

    if total is True:
        return [key]

    if obj is None or key not in obj:
        return [key]

    exception = val == TESTS_WILDCARD
    if exception:
        return []

    # COMPARE

    out = obj.get(key)
    if (isinstance(out, list)):
        out = list_to_dict(out)
    if isinstance(val, Mapping) and size(val) == 0:
        val = json.dumps(val)
    if isinstance(out, Mapping) and size(out) == 0:
        out = json.dumps(out)

    if out != val:
        return [key]

    return []


#


def get(obj, path):
    keys = path.split(".")
    value = obj

    for key in keys:
        try:
            if isinstance(value, list):
                value = value[int(key)]
            else:
                value = value.get(key)
        except:
            return None

    return value


def size(obj):
    if isinstance(obj, list):
        return len(obj)
    if isinstance(obj, Mapping):
        return
    return 0


def list_to_dict(arr):
    return {str(i): x for i, x in enumerate(arr)}
