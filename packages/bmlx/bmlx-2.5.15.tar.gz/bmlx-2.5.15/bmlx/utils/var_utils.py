import re
from typing import List, Text


def parse_var(s):
    """
    Parse a key, value pair, separated by '='
    That's the reverse of ShellArgs.

    On the command line (argparse) a declaration will typically look like:
        foo=hello
    or
        foo="hello world"
    """
    items = s.split("=")
    key = items[0].strip()  # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = "=".join(items[1:])
    return (key, value)


def parse_vars(items):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    d = {}

    if items:
        for item in items:
            key, value = parse_var(item)
            d[key] = value
    return d


def wildcard_vars(
    vars: List[Text], include_vars: List[Text], exclude_vars: List[Text] = []
):
    ret = []
    exclude_vars = set(exclude_vars)
    for var in include_vars:
        m = re.compile(var)
        ret.extend(
            [
                xdl_var.name
                for xdl_var in vars.keys()
                if xdl_var.name not in exclude_vars and m.match(xdl_var.name)
            ]
        )

    return ret
