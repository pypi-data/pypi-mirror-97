import abc
from six import with_metaclass
from bmlx.proto.metadata import execution_pb2
from typing import Optional, Text


class DriverArgs(object):
    def __init__(
        self,
        pipeline_execution: execution_pb2.Execution,
        artifact_storage_base: Optional[Text] = None,
        enable_cache: Optional[bool] = False,
        prepare_output_uri: Optional[bool] = True,
        local_mode: Optional[bool] = False,
        project_name: Optional[Text] = "",
        owner: Optional[Text] = "",
    ):
        self.pipeline_execution = pipeline_execution
        self.enable_cache = enable_cache
        # whether create a new uri for output
        self.prepare_output_uri = prepare_output_uri
        self.artifact_storage_base = artifact_storage_base
        self.local_mode = local_mode
        self.project_name = project_name
        self.owner = owner


class Driver(object):
    def __init__(self):
        raise RuntimeError(
            "you should not init 'Driver' class, choose bmlx.execution.driver.BaseDriver instead"
        )


class DriverSpec(with_metaclass(abc.ABCMeta)):
    pass


class DriverClassSpec(DriverSpec):
    def __init__(self, driver_class):
        if not driver_class:
            raise ValueError("driver_class must be set")
        self.driver_class = driver_class
