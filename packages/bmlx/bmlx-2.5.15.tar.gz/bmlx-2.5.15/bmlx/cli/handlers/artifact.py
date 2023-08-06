from typing import Text, Optional, List, Dict, Any
from bmlx.cli.handlers.utils import format_time, list_action
from bmlx.proto.metadata import artifact_pb2


def list(
    format: Optional[Text] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    filters: Optional[Dict[Text, Any]] = {},
    local_mode: Optional[bool] = False,
    env: Optional[Text] = None,
):
    def _f(artifacts):
        return (
            [
                "id",
                "uri",
                "type",
                "ctime",
                "execution_id",
                "producer_component",
                "state",
            ],
            [
                (
                    artifact.id,
                    artifact.uri,
                    artifact.type,
                    format_time(artifact.create_time),
                    artifact.execution_id,
                    artifact.producer_component,
                    artifact_pb2.Artifact.State.Name(artifact.state),
                )
                for artifact in artifacts
            ],
        )

    list_action(
        resources="artifacts",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        filters=filters,
        local_mode=local_mode,
        env=env,
    )
