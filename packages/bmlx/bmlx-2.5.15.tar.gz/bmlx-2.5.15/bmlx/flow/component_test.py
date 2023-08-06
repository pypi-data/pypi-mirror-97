import unittest
from typing import Optional
from bmlx.flow import (
    Artifact,
    Component,
    ComponentSpec,
    ChannelParameter,
    ExecutionParameter,
    DriverClassSpec,
    ExecutorClassSpec,
    Executor,
)
from bmlx.execution.driver import Driver


class FakeArtifact(Artifact):
    TYPE_NAME = "Fake"


class ComponentTest(unittest.TestCase):
    def testNormalComponent(self):
        class NormalOptionalInputsComponentSpec(ComponentSpec):
            INPUTS = {
                "input_a": ChannelParameter(type=FakeArtifact, optional=True)
            }
            OUTPUTS = {}
            PARAMETERS = {}

        class NormalOptionalInputsComponent(Component):
            SPEC_CLASS = NormalOptionalInputsComponentSpec
            EXECUTOR_SPEC = ExecutorClassSpec(Executor)
            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self, input_a: Optional[FakeArtifact] = None):
                spec = NormalOptionalInputsComponentSpec(input_a=input_a)
                super(NormalOptionalInputsComponent, self).__init__(spec)

        NormalOptionalInputsComponent(
            input_a=None
        )  # None input_a will work well

    def testIllegalComponent(self):
        class IllegalParameterComponentSpec(ComponentSpec):
            INPUTS = {}
            OUTPUTS = {}
            PARAMETERS = {
                "illegal_type": ChannelParameter(type=FakeArtifact),
            }

        class IllegalDupParameterComponentSpec(ComponentSpec):
            INPUTS = {
                "key_a": ChannelParameter(type=FakeArtifact),
            }
            OUTPUTS = {}
            PARAMETERS = {
                "key_a": ExecutionParameter(),
            }

        class IllegalInputsComponentSpec(ComponentSpec):
            INPUTS = {"illegal": ExecutionParameter()}
            OUTPUTS = {}
            PARAMETERS = {}

        class IllegalOptionalInputsComponentSpec(ComponentSpec):
            INPUTS = {
                "illegal": ChannelParameter(type=FakeArtifact, optional=False)
            }
            OUTPUTS = {}
            PARAMETERS = {}

        class IllegalParameterComponent(Component):
            SPEC_CLASS = IllegalParameterComponentSpec
            EXECUTOR_SPEC = ExecutorClassSpec(Executor)
            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self):
                spec = IllegalParameterComponentSpec()
                super(IllegalParameterComponent, self).__init__(spec)

        class IllegalDupParameterComponent(Component):
            SPEC_CLASS = IllegalDupParameterComponentSpec

            EXECUTOR_SPEC = ExecutorClassSpec(Executor)

            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self):
                spec = IllegalDupParameterComponentSpec()
                super(IllegalDupParameterComponent, self).__init__(spec)

        class IllegalInputsComponent(Component):
            SPEC_CLASS = IllegalInputsComponentSpec

            EXECUTOR_SPEC = ExecutorClassSpec(Executor)

            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self):
                spec = IllegalInputsComponentSpec()
                super(IllegalInputsComponent, self).__init__(spec)

        class A_NormalComponentSpec(ComponentSpec):
            INPUTS = {}
            OUTPUTS = {}
            PARAMETERS = {}

        class B_NormalComponentSpec(ComponentSpec):
            INPUTS = {}
            OUTPUTS = {}
            PARAMETERS = {}

        class IllegalMismatchSpecComponent(Component):
            SPEC_CLASS = A_NormalComponentSpec
            EXECUTOR_SPEC = ExecutorClassSpec(Executor)
            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self):
                spec = B_NormalComponentSpec()
                super(IllegalMismatchSpecComponent, self).__init__(spec)

        class IllegalOptionalInputsComponent(Component):
            SPEC_CLASS = IllegalOptionalInputsComponentSpec
            EXECUTOR_SPEC = ExecutorClassSpec(Executor)
            DRIVER_SPEC = DriverClassSpec(Driver)

            def __init__(self, illegal_input: Optional[FakeArtifact] = None):
                spec = IllegalOptionalInputsComponentSpec(illegal=illegal_input)
                super(IllegalOptionalInputsComponent, self).__init__(spec)

        self.assertRaisesRegex(
            ValueError, "duplicated.*", IllegalDupParameterComponent
        )
        self.assertRaisesRegex(
            ValueError, "INPUTS.*ChannelParameter.*", IllegalInputsComponent
        )
        self.assertRaises(ValueError, IllegalParameterComponent)
        self.assertRaisesRegex(
            TypeError,
            "passing mismatch sepc type.*",
            IllegalMismatchSpecComponent,
        )

        self.assertRaisesRegex(
            ValueError,
            "Invalid ChannelParameter",
            IllegalOptionalInputsComponent,
        )
