import csv
from io import BytesIO, StringIO
import json
import re
import zipfile
import requests
from alfa_cli.config import settings


def evaluate_reference(ref):
    ref_string = _stringify(ref)
    regex = r'{"' + re.escape(settings.reference.key) + r'":\s?"https:\/\/[^}]*"}'
    references = re.findall(regex, ref_string)
    for reference in references:
        parsed_reference = json.loads(reference)
        data = _fetch_data(parsed_reference)
        recursive_data = evaluate_reference(data)
        ref_string = re.sub(re.escape(reference), _stringify(recursive_data), ref_string)
    return json.loads(ref_string)


def _stringify(obj):
    if isinstance(obj, str):
        return obj
    return json.dumps(obj)


def _fetch_data(reference):
    res = requests.get(reference[settings.reference.key])
    res.raise_for_status()
    data = _decompress_data(res.content)
    return _convert_data(data)


def _decompress_data(compressed_data):
    try:
        with BytesIO(compressed_data) as file:
            file.seek(0)
            with zipfile.ZipFile(file, mode="r") as zip_file:
                if settings.reference.compression.file_name not in zip_file.namelist():
                    raise Exception("Invalid zip file found. Failed to unpack payload.")
                data = zip_file.open(settings.reference.compression.file_name).readlines()
                decoded_data = [entry.decode("utf-8") for entry in data]
                if len(decoded_data) == 1:
                    return decoded_data[0]
                return "".join(decoded_data)
    except zipfile.BadZipFile:
        return compressed_data.decode("utf-8")


def _convert_data(data):
    if _is_json(data):
        return data
    try:
        return _convert_csv(data)
    except:
        return data


def _is_json(data):
    try:
        json.loads(data)
        return True
    except TypeError:
        return False
    except json.JSONDecodeError:
        return False


def _convert_csv(data):
    converted_data = [
        {k: _num(v) for k, v in row.items()}
        for row in csv.DictReader(StringIO(data), skipinitialspace=True)
    ]
    return _stringify(converted_data)


def _num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s
