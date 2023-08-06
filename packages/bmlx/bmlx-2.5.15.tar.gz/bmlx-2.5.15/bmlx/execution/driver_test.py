from bmlx.flow import (
    Artifact,
    Executor,
    Component,
    ComponentSpec,
    ChannelParameter,
    ExecutorClassSpec,
    DriverClassSpec,
    Channel,
)
import unittest
import tempfile
import shutil
from bmlx.metadata.metadata import Metadata
from bmlx.flow import Pipeline
from bmlx.proto.metadata import execution_pb2
from bmlx.execution.driver import DriverArgs, BaseDriver
import bmlx.metadata.local_store as ks


class Artifact_A(Artifact):
    TYPE_NAME = "artifact_a"


class MockComponentSpec(ComponentSpec):
    INPUTS = {
        "input": ChannelParameter(Artifact_A),
    }

    PARAMETERS = {}

    OUTPUTS = {}


class MockProducerComponentSpec(ComponentSpec):
    INPUTS = {}

    PARAMETERS = {}

    OUTPUTS = {
        "output": ChannelParameter(Artifact_A),
    }


class MockProducerComponent(Component):
    SPEC_CLASS = MockProducerComponentSpec

    EXECUTOR_SPEC = ExecutorClassSpec(Executor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(self, output):

        spec = MockProducerComponentSpec(output=output,)
        super(MockProducerComponent, self).__init__(
            spec, instance_name="mock_producer"
        )


class MockComponent(Component):
    SPEC_CLASS = MockComponentSpec

    EXECUTOR_SPEC = ExecutorClassSpec(Executor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(self, input: Artifact_A):
        spec = MockComponentSpec(input=input)
        super(MockComponent, self).__init__(
            spec, instance_name="mock_component"
        )


class DriverTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.metadata = Metadata(
            local_mode=True, local_storage_path=self.test_dir
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def testArtifactPassing(self):
        # first we create a fake output
        a = Artifact_A()
        a.meta.uri = "hdfs://mock_a"
        a.meta.name = "i"
        a.meta.type = Artifact_A.TYPE_NAME

        chl = Channel(artifact_type=Artifact_A, artifacts=[a],)

        producer_component = MockProducerComponent(output=chl)
        test_component = MockComponent(producer_component.outputs["output"])

        pipeline = Pipeline(
            name="test-pipeline",
            components=[producer_component, test_component],
        )

        exe = execution_pb2.Execution()
        exe.name = "Test_A"
        exe.description = "desc"

        ctx = self.metadata.store._make_mlpb_context(
            context_type=ks._PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=ks._PIPELINE_EXECUTION_SPEC,
            context_name=exe.name,
            bmlx_pb_msg=exe,
        )
        [ctx.id] = self.metadata.store._ml_store.put_contexts([ctx])
        exe.context_id = ctx.id

        # mock a fake component execution
        component_execution = execution_pb2.ComponentExecution(
            name="fake_exection",
            type=producer_component.id,  # type is producer component
        )

        self.metadata.store.create_or_update_component_execution(
            exe, component_execution, output_artifacts=[a.meta]
        )

        driver_args = DriverArgs(pipeline_execution=exe)
        driver = BaseDriver(metadata=self.metadata)
        execution_info = driver.pre_execution(
            input_dict={"input": chl,},
            output_dict={},
            exec_properties={},
            pipeline=pipeline,
            component=test_component,
            driver_args=driver_args,
        )

        self.assertEqual(len(execution_info.input_dict["input"]), 1)
        resolved = execution_info.input_dict["input"][0]
        self.assertEqual(resolved.meta.uri, a.meta.uri)
