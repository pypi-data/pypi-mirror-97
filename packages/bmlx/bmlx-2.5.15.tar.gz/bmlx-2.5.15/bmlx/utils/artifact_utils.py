"""mlx Artifact utilities."""
import json

from typing import Dict, List, Text

from bmlx.flow import Artifact


def parse_artifact_dict(json_str: Text) -> Dict[Text, List[Artifact]]:
    """Parse a dict from key to list of Artifact from its json format."""
    bmlx_artifacts = {}
    for k, l in json.loads(json_str).items():
        bmlx_artifacts[k] = [Artifact.from_json_dict(v) for v in l]
    return bmlx_artifacts


def jsonify_artifact_dict(artifact_dict: Dict[Text, List[Artifact]]) -> Text:
    """Serialize a dict from key to list of Artifact into json format."""
    d = {}
    for k, l in artifact_dict.items():
        d[k] = [repr(v) for v in l]
    return json.dumps(d)


def get_single_instance(artifact_list: List[Artifact]) -> Artifact:
    """Get a single instance of Artifact from a list of length one.

    Args:
      artifact_list: A list of Artifact objects whose length must be one.

    Returns:
      The single Artifact object in artifact_list.

    Raises:
      ValueError: If length of artifact_list is not one.
    """
    if len(artifact_list) != 1:
        raise ValueError(
            "expected list length of one but got {}".format(len(artifact_list))
        )
    return artifact_list[0]


def get_single_uri(artifact_list: List[Artifact]) -> Text:
    """Get the uri of Artifact from a list of length one.

    Args:
      artifact_list: A list of Artifact objects whose length must be one.

    Returns:
      The uri of the single Artifact object in artifact_list.

    Raises:
      ValueError: If length of artifact_list is not one.
    """
    return get_single_instance(artifact_list).meta.uri
