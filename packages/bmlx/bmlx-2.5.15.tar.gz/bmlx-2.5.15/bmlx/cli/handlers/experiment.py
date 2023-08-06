from typing import Text, Optional, List, Dict, Any
from bmlx.cli.handlers.utils import format_time, list_action


def list(
    format: Text,
    page_size: int,
    page_token: str,
    filters: Optional[Dict[Text, Any]] = {},
    local_mode: bool = False,
    env: Optional[Text] = None,
):
    def _f(experiments):
        return (
            [
                "id",
                "name",
                "pipeline_version_id",
                "resource_group",
                "namespace",
                "trigger_type",
                "package_uri",
                "ctime",
                "description",
            ],
            [
                (
                    experiment.id,
                    experiment.name,
                    experiment.pipeline_version_id,
                    experiment.resource_group,
                    experiment.namespace,
                    experiment.trigger_type,
                    experiment.package_uri,
                    format_time(experiment.create_time),
                    experiment.description,
                )
                for experiment in experiments
            ],
        )

    list_action(
        resources="experiments",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        filters=filters,
        local_mode=local_mode,
        env=env,
    )
