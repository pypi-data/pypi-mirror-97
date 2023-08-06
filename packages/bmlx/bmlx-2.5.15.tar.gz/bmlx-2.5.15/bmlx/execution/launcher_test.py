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
from bmlx.execution.driver import DriverArgs, BaseDriver
from bmlx.execution.launcher import Launcher
from bmlx.context import BmlxContext
from ml_metadata.proto import metadata_store_pb2 as mlpb
from unittest.mock import Mock
from bmlx.config import Configuration


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


class LaucnherTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.context = BmlxContext()
        self.context.local_mode = True
        self.context._store = Metadata(
            local_mode=True, local_storage_path=self.test_dir
        )

        # first we create a fake output
        self.artifact = Artifact_A()
        self.artifact.meta.uri = "hdfs://mock_a"
        self.artifact.meta.name = "i"
        self.artifact.meta.type = Artifact_A.TYPE_NAME

        chl = Channel(artifact_type=Artifact_A, artifacts=[self.artifact],)

        self.producer_component = MockProducerComponent(output=chl)
        self.consumer_component = MockComponent(
            input=self.producer_component.outputs["output"]
        )
        self.pipeline = Pipeline(
            name="test-pipeline",
            components=[self.producer_component, self.consumer_component],
        )

        self.pipeline_execution = self.context.metadata.get_or_create_pipeline_execution(
            pipeline=self.pipeline,
        )
        self.artifact_base = tempfile.mkdtemp()
        # mock artifact storage base
        self.context.project = Mock()
        self.context.project.configure_mock(
            artifact_storage_base=self.artifact_base,
            configs=Configuration(default={}),
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def testLaunchOutputComponents(self):
        launcher = Launcher(
            context=self.context,
            component=self.producer_component,
            pipeline=self.pipeline,
            driver_args=DriverArgs(
                pipeline_execution=self.pipeline_execution,
                prepare_output_uri=False,  # essential for testing
            ),
        )
        launcher.launch()

        # after launcher, there would create three main record
        # 1. artifacts
        saved_artifact = self.context.metadata.get_artifacts_by_uri(
            "hdfs://mock_a"
        )
        self.assertTrue(len(saved_artifact) > 0)
        self.assertEqual(saved_artifact[0].uri, "hdfs://mock_a")
        self.assertEqual(saved_artifact[0].type, "artifact_a")

        # 2. a component execution
        saved_component_execution = self.context.metadata.store.get_component_execution(
            pipeline_execution=self.pipeline_execution,
            component_id=self.producer_component.id,
        )

        self.assertIsNotNone(saved_component_execution)

        # 3. output events
        saved_events = self.context.metadata.store._ml_store.get_events_by_execution_ids(
            [saved_component_execution.id]
        )
        self.assertIsNotNone(saved_events)
        self.assertEqual(saved_events[0].type, mlpb.Event.OUTPUT)
        self.assertEqual(saved_events[0].artifact_id, saved_artifact[0].id)

    def testLaunchTwice(self):
        launcher = Launcher(
            context=self.context,
            component=self.producer_component,
            pipeline=self.pipeline,
            driver_args=DriverArgs(
                pipeline_execution=self.pipeline_execution,
                prepare_output_uri=False,  # essential for testing
            ),
        )
        launcher.launch()
        launcher.launch()
        saved_component_execution = self.context.metadata.store.get_component_executions_of_pipeline(
            pipeline_execution=self.pipeline_execution,
        )

        self.assertIsNotNone(saved_component_execution)
        self.assertEqual(len(saved_component_execution), 1)

    def testLaunchInputComponents(self):
        # prepare artifacts, depends on last test for convienence
        launcher = Launcher(
            context=self.context,
            component=self.producer_component,
            pipeline=self.pipeline,
            driver_args=DriverArgs(
                pipeline_execution=self.pipeline_execution,
                prepare_output_uri=False,  # essential for testing
            ),
        )
        launcher.launch()

        launcher = Launcher(
            context=self.context,
            component=self.consumer_component,
            pipeline=self.pipeline,
            driver_args=DriverArgs(
                pipeline_execution=self.pipeline_execution,
                prepare_output_uri=False,  # essential for testing
            ),
        )
        launcher.launch()

        # 1. check only one artifact
        saved_artifacts = self.context.metadata.get_artifacts_by_types()
        self.assertEqual(len(saved_artifacts), 1)

        # 2. check use same artifact
        saved_events = self.context.metadata.store._ml_store.get_events_by_artifact_ids(
            [saved_artifacts[0].id]
        )
        self.assertTrue(len(saved_events), 2)
        self.assertSetEqual(
            set([e.type for e in saved_events]),
            set([mlpb.Event.OUTPUT, mlpb.Event.INPUT]),
        )
