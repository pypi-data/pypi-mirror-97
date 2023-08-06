from six import with_metaclass
import abc
from typing import Set, Type, Dict, Text
from bmlx.flow.channel import Channel
from bmlx.flow.executor_spec import ExecutorClassSpec, ExecutorSpec, Executor
from bmlx.flow.driver_spec import DriverClassSpec
from bmlx.utils import naming_utils


class Node(with_metaclass(abc.ABCMeta)):
    """
    basic execution node of graph
    """

    EXECUTOR_SPEC: ExecutorSpec = ExecutorClassSpec(Executor)

    DRIVER_SPEC = abc.abstractproperty()

    # 允许 node 失败重试，try_limit 规定了 node 在一次pipeline run中最多执行次数。
    def __init__(self, instance_name: str, try_limit: int = 1):
        if instance_name and not naming_utils.is_valid_bmlx_node_name(
            instance_name
        ):
            raise ValueError(
                "Invalid instance name, valid pattern: %s"
                % naming_utils.bmlx_node_name_pattern()
            )

        self._instance_name: str = instance_name
        self._try_limit = try_limit
        self.executor_spec: ExecutorSpec = self.__class__.EXECUTOR_SPEC
        self.driver_spec: Type[DriverClassSpec] = self.__class__.DRIVER_SPEC

        self._preoders: Set[Node] = set()
        self._postorders: Set[Node] = set()

    @property
    def type(self) -> Text:
        return "%s.%s" % (self.__class__.__module__, self.__class__.__name__)

    @property
    def id(self) -> Text:
        return self._instance_name

    @property
    @abc.abstractmethod
    def inputs(self) -> Dict[str, Channel]:
        pass

    @property
    @abc.abstractmethod
    def outputs(self) -> Dict[str, Channel]:
        pass

    @property
    @abc.abstractmethod
    def exec_properties(self) -> Dict[str, str]:
        pass

    @property
    def preorders(self):
        return self._preoders

    def add_preorder(self, node):
        self._preoders.add(node)

    @property
    def postorders(self):
        return self._postorders

    def add_postorder(self, node):
        self._postorders.add(node)

    @property
    def try_limit(self) -> int:
        return self._try_limit

    def skip_execution(self, pipeline_execution, exec_properties) -> bool:
        return False