DEFAULT_EXCLUDES = [".git/**/*", ".gitignore", ".DS_Store"]


#


def extract_ignore_rules(*, conf=None, excludes=None, includes=None):
    if excludes is None:
        excludes = []
    if includes is None:
        includes = []

    if conf is not None:
        to_exclude, to_include = extract_ignore_rules_from_conf(conf)
        excludes.extend(to_exclude)
        includes.extend(to_include)

    excludes, includes = parse_ignore_rules(excludes, includes)
    return excludes, includes


def parse_ignore_rules(excludes, includes):
    for glob in excludes:
        if glob.startswith("!"):
            excludes.remove(glob)
            includes.append(glob[1:])

    excludes = list(set(excludes + DEFAULT_EXCLUDES))
    includes = list(set(includes))

    # convert dir/** to dir/**/* (adds files instead of dirs)
    excludes = [x + "/*" if x.endswith("/**") else x for x in excludes]
    includes = [x + "/*" if x.endswith("/**") else x for x in includes]

    return excludes, includes


#


def extract_ignore_rules_from_conf(conf):
    (to_exclude, to_include) = extract_ignore_rules_from_section(conf)
    excludes = to_exclude
    includes = to_include

    functions = conf.get("functions", [])
    for function in functions:
        if type(function) is dict:
            name = list(function.keys())[0]
            data = function.get(name)
        else:
            name = function
            data = functions.get(name)

        to_exclude, to_include = extract_ignore_rules_from_section(data, root=name)
        excludes.extend(to_exclude)
        includes.extend(to_include)

    return excludes, includes


def extract_ignore_rules_from_section(conf, *, root=None):
    package = conf.get("package")
    if package is None:
        return ([], [])

    to_exclude = package.get("exclude", [])
    to_include = package.get("include", [])

    if root is not None:
        to_exclude = ["{}/{}".format(root, x) for x in to_exclude]
        to_include = ["{}/{}".format(root, x) for x in to_include]

    return to_exclude, to_include
