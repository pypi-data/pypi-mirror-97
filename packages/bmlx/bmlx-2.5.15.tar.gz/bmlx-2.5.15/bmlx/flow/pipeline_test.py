import unittest
from bmlx.flow import (
    Artifact,
    Channel,
    Component,
    ComponentSpec,
    ChannelParameter,
    Pipeline,
    Executor,
    ExecutorClassSpec,
    DriverClassSpec,
)

from bmlx.execution.driver import Driver


from typing import Text, Any, Dict


class MockArtifact_A(Artifact):
    TYPE_NAME = "MockArtifactA"


class MockArtifact_B(Artifact):
    TYPE_NAME = "MockArtifactB"


class ComponentSpec_A(ComponentSpec):
    PARAMETERS: Dict[Text, Any] = {}
    INPUTS: Dict[Text, Any] = {}
    OUTPUTS = {"mock_a": ChannelParameter(type=MockArtifact_A, optional=False)}


class MockComponent_A(Component):
    SPEC_CLASS = ComponentSpec_A
    EXECUTOR_SPEC = ExecutorClassSpec(Executor)
    DRIVER_SPEC = DriverClassSpec(Driver)

    def __init__(self):
        mock_a = MockArtifact_A()
        output = Channel(artifact_type=MockArtifact_A, artifacts=[mock_a])
        spec = ComponentSpec_A(mock_a=output)

        super(MockComponent_A, self).__init__(spec, instance_name="component_a")


class ComponentSpec_B(ComponentSpec):
    PARAMETERS: Dict[Text, Any] = {}
    OUTPUTS: Dict[Text, Any] = {}
    INPUTS = {
        "mock_a_input": ChannelParameter(type=MockArtifact_A, optional=False)
    }


class MockComponent_B(Component):
    SPEC_CLASS = ComponentSpec_B
    EXECUTOR_SPEC = ExecutorClassSpec(Executor)
    DRIVER_SPEC = DriverClassSpec(Driver)

    def __init__(self, mock_a_input: MockArtifact_A):
        spec = ComponentSpec_B(mock_a_input=mock_a_input)

        super(MockComponent_B, self).__init__(spec, instance_name="component_b")


class ComponentSpec_C(ComponentSpec):
    INPUTS = {
        "input_a": ChannelParameter(type=MockArtifact_A),
    }
    OUTPUTS = {
        "output_b": ChannelParameter(type=MockArtifact_B),
    }
    PARAMETERS = {}


class ComponentSpec_D(ComponentSpec):
    INPUTS = {
        "input_b": ChannelParameter(type=MockArtifact_B),
    }
    OUTPUTS = {
        "output_a": ChannelParameter(type=MockArtifact_A),
    }
    PARAMETERS = {}


# C and D is circle
class MockComponent_C(Component):
    SPEC_CLASS = ComponentSpec_C
    EXECUTOR_SPEC = ExecutorClassSpec(Executor)
    DRIVER_SPEC = DriverClassSpec(Driver)


class MockComponent_D(Component):
    SPEC_CLASS = ComponentSpec_D
    EXECUTOR_SPEC = ExecutorClassSpec(Executor)
    DRIVER_SPEC = DriverClassSpec(Driver)


class PipelineTest(unittest.TestCase):
    def testSequence(self):
        """
        A->B
        """
        com_a = MockComponent_A()
        com_b = MockComponent_B(mock_a_input=com_a.outputs["mock_a"])
        pipeline = Pipeline(
            name="test-sequence-pipeline", components=[com_a, com_b]
        )

        self.assertEqual(pipeline.meta.namespace, "default")
        self.assertEqual(pipeline.meta.name, "test-sequence-pipeline")

    def testCircle(self):
        A = Channel(artifact_type=MockArtifact_A, artifacts=[MockArtifact_A()])
        B = Channel(artifact_type=MockArtifact_B, artifacts=[MockArtifact_B()])
        spec_c = ComponentSpec_C(input_a=A, output_b=B)
        spec_d = ComponentSpec_D(input_b=B, output_a=A)

        com_c = MockComponent_C(spec_c, instance_name="com_c")
        com_d = MockComponent_D(spec_d, instance_name="com_d")

        with self.assertRaisesRegex(RuntimeError, "cycle exists.*"):
            _ = Pipeline(name="test-circle", components=[com_c, com_d])
