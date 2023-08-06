from typing import Text, Optional, List, Dict, Any
from bmlx.proto.metadata import execution_pb2
from bmlx.cli.handlers.utils import format_time, list_action


def list(
    format: Text,
    page_size: int,
    page_token: str,
    filters: Optional[Dict[Text, Any]] = {},
    local_mode: bool = False,
    env: Optional[Text] = None,
):
    def _f(executions):
        return (
            [
                "id",
                "run_name",
                "experiment_id",
                "status",
                "ctime",
                "stime",
                "ftime",
            ],
            [
                (
                    exe.id,
                    exe.name,
                    exe.experiment_id,
                    execution_pb2.State.Name(exe.state),
                    format_time(exe.create_time),
                    format_time(exe.schedule_time),
                    format_time(exe.finish_time),
                )
                for exe in executions
            ],
        )

    list_action(
        resources="pipeline_executions",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        filters=filters,
        local_mode=local_mode,
        env=env,
    )
