import re

# ^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$ is for normal checking
# notice that we changed 63->30, because some component like volcano
# would add some suffix to name, so ,we limit pipeline with shorter length
_NAMING_RE = re.compile(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,30}(?<!-)$")
# for argo naming
_ARGO_NAMING_PATTERN = (
    r"[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*"
)
_ARGO_NAMING_RE = re.compile(_ARGO_NAMING_PATTERN)

_BMLX_NODE_NAMING_PATTERN = r"^[a-z]([_a-z0-9]*[a-z0-9])*$"
_BMLX_NODE_NAMING_RE = re.compile(_BMLX_NODE_NAMING_PATTERN)


def is_name_valid(name):
    global _NAMING_RE
    return _NAMING_RE.match(name)


def is_valid_argo_name(name):
    global _ARGO_NAMING_RE
    return _ARGO_NAMING_RE.match(name)


def argo_name_pattern():
    global _ARGO_NAMING_PATTERN
    return _ARGO_NAMING_PATTERN


def is_valid_bmlx_node_name(name):
    global _BMLX_NODE_NAMING_RE
    return _BMLX_NODE_NAMING_RE.match(name)


def bmlx_node_name_pattern():
    global _BMLX_NODE_NAMING_PATTERN
    return _BMLX_NODE_NAMING_PATTERN
