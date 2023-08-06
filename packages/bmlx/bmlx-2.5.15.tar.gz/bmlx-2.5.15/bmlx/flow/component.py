from six import with_metaclass
import abc
import itertools

from typing import Text, Optional, Dict, Any, Type
from bmlx.flow.node import Node
from bmlx.flow.channel import Channel
from bmlx.flow.artifact import Artifact
from bmlx.flow.executor_spec import ExecutorSpec


class _ComponentParameter(object):
    pass


class ExecutionParameter(_ComponentParameter):
    __slots__ = ["type", "optional", "description"]

    def __init__(self,
                 type=None,
                 optional: Optional[Text]=False,
                 description: Optional[Text] = ""):
        self.type = type
        self.optional = optional
        self.description = description

    def __repr__(self):
        return "ExecutionParameter: type:%s, optional:%s" % (
            self.type,
            self.optional,
        )

    def __eq__(self, other):
        return isinstance(other.__class__, self.__class__) and (
            other.type == self.type and other.optional == self.optional
        )

    def type_check(self, key: Text, value: Any):
        # TODO add type check further
        if not self.optional and value is None:
            raise ValueError(
                "Invalid ExecutionParameter %s, non-optional parameter with None value"
                % key
            )


class ChannelParameter(_ComponentParameter):
    __slots__ = ["type", "optional", "description"]

    def __init__(
        self,
        type: Optional[Type[Artifact]],
        optional: Optional[bool] = False,
        description: Optional[Text] = "",
    ):
        if not issubclass(type, Artifact):
            raise TypeError(
                "ChannelParameter only support Artifact type now"
                ", got %r" % type
            )

        self.type = type.TYPE_NAME
        self.optional = optional
        self.description = description

    def __eq__(self, other):
        return isinstance(other.__class__, self.__class__) and (
            other.type == self.type and other.optional == self.optional
        )

    def type_check(self, key: Text, value: Any):
        # TODO add type check further
        if not self.optional and value is None:
            raise ValueError(
                "Invalid ChannelParameter %s, non-optional parameter with None value"
                % key
            )


class ComponentSpec(with_metaclass(abc.ABCMeta)):
    PARAMETERS: Dict[str, _ComponentParameter]

    INPUTS: Dict[str, _ComponentParameter]

    OUTPUTS: Dict[str, _ComponentParameter]

    def __init__(self, **kwargs):
        self._raw_args = kwargs

        self._validate()
        self._parse_args()

    def _validate(self):
        assert isinstance(
            self.PARAMETERS, dict
        ), "PARAMETERS type should be dict"
        assert isinstance(self.INPUTS, dict), "INPUTS type should be dict"
        assert isinstance(self.OUTPUTS, dict), "OUTPUTS type should be dict"

        seen_args = set()
        for name, arg in self.PARAMETERS.items():
            if not isinstance(arg, ExecutionParameter):
                raise ValueError(
                    "%s's PARAMETERS type must be instance "
                    "of ExecutionParameter,"
                    "we got %s (for %s) instead" % (self.__class__, arg, name)
                )

            if name in seen_args:
                raise ValueError(
                    "duplicated parameter %s seen for %s"
                    % (name, self.__class__)
                )
            seen_args.add(name)

        for name, arg in itertools.chain(
            self.INPUTS.items(), self.OUTPUTS.items()
        ):
            if not isinstance(arg, ChannelParameter):
                raise ValueError(
                    "%s's INPUTS, OUTPUS type must be "
                    "instance of ChannelParameter,"
                    "we got %s (for %s) instead" % (self.__class__, arg, name)
                )
            if name in seen_args:
                raise ValueError(
                    "duplicated parameter %s seen for %s"
                    % (name, self.__class__)
                )
            seen_args.add(name)

    def _parse_args(self):
        unparsed = set(self._raw_args)
        self.exec_properties = {}

        for name, arg in itertools.chain(
            self.PARAMETERS.items(), self.INPUTS.items(), self.OUTPUTS.items()
        ):
            if name not in unparsed:
                if not arg.optional:
                    raise ValueError(
                        "Missing arguments %r to %s" % (name, self.__class__)
                    )

                continue

            unparsed.remove(name)
            v = self._raw_args[name]
            if arg.optional and not v:
                continue
            arg.type_check(name, v)

        for name, arg in self.PARAMETERS.items():
            if arg.optional and name not in self._raw_args:
                continue

            value = self._raw_args[name]
            self.exec_properties[name] = value

        def _get_spec_value(desc):
            d = {}

            for name, arg in desc.items():
                if arg.optional and not self._raw_args.get(name):
                    continue
                d[name] = self._raw_args[name]

            return d

        self.inputs = _get_spec_value(self.INPUTS)
        self.outputs = _get_spec_value(self.OUTPUTS)

    def to_json_dict(self) -> Dict[Text, Any]:
        return {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "exec_properties": self.exec_properties,
        }


class Component(with_metaclass(abc.ABCMeta, Node)):
    SPEC_CLASS: Any = abc.abstractproperty()

    EXECUTOR_SPEC: Any = abc.abstractproperty()

    def __init__(
        self,
        spec: ComponentSpec,
        executor_spec: Optional[ExecutorSpec] = None,
        instance_name: Optional[Text] = None,
        try_limit: int = 1,
    ):
        super(Component, self).__init__(
            instance_name, try_limit
        )  # init node information

        if not isinstance(spec, self.__class__.SPEC_CLASS):
            raise TypeError(
                "passing mismatch sepc type %s to component (expect: %s)"
                % (spec.__class__.__name__, self.__class__.SPEC_CLASS.__name__)
            )
        self.spec = spec
        if executor_spec:
            if not isinstance(executor_spec, ExecutorSpec):
                raise TypeError(
                    "executor spec should be ExecutorSpec or its subclass"
                )

            self.executor_spec = executor_spec
        else:
            self.executor_spec = self.__class__.EXECUTOR_SPEC

        self.driver_class_spec = self.__class__.DRIVER_SPEC

        self._validate()

    def __repr__(self) -> str:
        return (
            "Component: name:%s, id:%s, driver_class: %s, executor_spec: %s"
            % (
                self._instance_name,
                self.id,
                self.driver_class_spec.driver_class.__name__,
                self.executor_spec.executor_class.__name__,
            )
        )

    @classmethod
    def _validate(cls):
        # TODO validate class members
        pass

    @property
    def inputs(self) -> Dict[Text, Channel]:
        return self.spec.inputs

    @property
    def outputs(self) -> Dict[Text, Channel]:
        return self.spec.outputs

    @property
    def exec_properties(self) -> Dict[Text, Any]:
        return self.spec.exec_properties

    def get_launcher_class(self, ctx):
        raise NotImplementedError("component should implment this method")
