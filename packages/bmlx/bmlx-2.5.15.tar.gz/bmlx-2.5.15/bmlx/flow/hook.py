import abc
import enum
from typing import Any


class Hook(object):
    class Status(enum.Enum):
        SUCCESS = 0
        FAIL = 1

    class HookResult:
        def __init__(self, status, msg):
            self.status = status
            self.message = msg

    @abc.abstractmethod
    def onComponentDone(self, context, pipeline, component, result: HookResult):
        pass

    @abc.abstractmethod
    def onPipelineDone(
        self, context, pipeline, pipeline_execution, result: HookResult
    ):
        pass
