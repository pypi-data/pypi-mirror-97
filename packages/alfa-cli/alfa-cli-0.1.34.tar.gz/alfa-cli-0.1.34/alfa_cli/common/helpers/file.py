import os
import zipfile
from pathlib import Path
from alfa_cli.common.helpers.ignore import extract_ignore_rules


def extract_dir(dirpath, prefix=None, ext=None):
    paths = walk_dir(dirpath)
    filtered_paths = [path for path in paths if not is_filtered(path, prefix, ext)]

    files = []
    for path in filtered_paths:
        fullpath = f"{dirpath}{path}"
        with open(fullpath, "r") as file:
            data = file.read()
            files.append(data)

    return files


def walk_dir(dirpath):
    walk = os.walk(dirpath)
    paths = []
    for (basepath, _, files) in walk:
        base = basepath.replace(dirpath, "")
        paths.extend([f"{base}/{name}" for name in files])

    return paths


def is_filtered(path, prefix, ext):
    path = path.lower()[1:]
    if isinstance(prefix, str):
        prefix = prefix.lower()
    if isinstance(ext, str):
        ext = ext.lower()

    is_root = "/" not in path
    not_prefix = prefix is not None and not path.startswith(prefix)
    not_extension = ext is not None and not path.endswith(ext)

    filtered = not_extension or (not is_root and not_prefix)
    return filtered


#


def resolve_package_files(source, *, excludes=[], includes=[]):
    root = Path(source)
    files = set(root.glob("**/*"))

    flatten = lambda l: [item for sublist in l for item in sublist]
    excluded = set(flatten([root.glob(glob) for glob in excludes]))
    included = set(flatten([root.glob(glob) for glob in includes]))

    files = files - excluded | included
    return files


def package_dir(source, dest, *, excludes=[], includes=[], conf=None):
    excludes, includes = extract_ignore_rules(conf=conf, excludes=excludes, includes=includes)

    files = resolve_package_files(source, excludes=excludes, includes=includes)
    files = [x for x in files if x.is_file()]

    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(file, file.relative_to(source))
