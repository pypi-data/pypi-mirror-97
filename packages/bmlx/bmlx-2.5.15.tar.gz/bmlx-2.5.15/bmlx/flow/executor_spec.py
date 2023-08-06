import abc
import logging

from six import with_metaclass
from bmlx.flow import Artifact
from typing import Dict, Text, Type, List, Any
from bmlx.utils import artifact_utils


class Executor(object):
    def __init__(self, context):
        self._ctx = context

    @abc.abstractmethod
    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ) -> int:
        return 0

    def _log_startup(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ) -> None:
        logging.info("start %s execution" % self.__class__.__name__)
        logging.info(
            "input for %s is %s"
            % (
                self.__class__.__name__,
                artifact_utils.jsonify_artifact_dict(input_dict),
            )
        )
        logging.info(
            "output for %s is %s"
            % (
                self.__class__.__name__,
                artifact_utils.jsonify_artifact_dict(output_dict),
            )
        )
        logging.info("exec properties: %s", exec_properties)


class ExecutorSpec(with_metaclass(abc.ABCMeta)):
    def __init__(self):
        pass


class ExecutorClassSpec(ExecutorSpec):
    def __init__(self, executor_class: Type[Executor]):
        if not executor_class:
            raise ValueError("'executor_class must be set'")
        self.executor_class = executor_class
        super(ExecutorClassSpec, self).__init__()
