import unittest
from bmlx.flow import (
    Artifact,
    Executor,
    Component,
    ComponentSpec,
    ExecutorClassSpec,
    DriverClassSpec,
)
from bmlx.execution.driver import BaseDriver
from bmlx.execution.launcher import Launcher
import tempfile
import shutil
from bmlx.metadata.metadata import Metadata
from unittest.mock import Mock
from bmlx.flow import Pipeline
from bmlx.context import BmlxContext
from bmlx.execution.runner import Runner
from bmlx.config import Configuration


class Artifact_A(Artifact):
    TYPE_NAME = "artifact_a"


class MockComponentSeq1Spec(ComponentSpec):
    INPUTS = {}

    PARAMETERS = {}

    OUTPUTS = {}


class MockComponentSeq2Spec(ComponentSpec):
    INPUTS = {}

    PARAMETERS = {}

    OUTPUTS = {}


class MockSeq1Component(Component):
    SPEC_CLASS = MockComponentSeq1Spec

    EXECUTOR_SPEC = ExecutorClassSpec(Executor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(self):
        spec = MockComponentSeq1Spec()
        super(MockSeq1Component, self).__init__(spec, instance_name="seq1")

    def get_launcher_class(self, ctx):
        return Launcher


class MockSeq2Component(Component):
    SPEC_CLASS = MockComponentSeq2Spec

    EXECUTOR_SPEC = ExecutorClassSpec(Executor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(self):
        spec = MockComponentSeq2Spec()
        super(MockSeq2Component, self).__init__(spec, instance_name="seq2")

    def get_launcher_class(self, ctx):
        return Launcher


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.artifact_base = tempfile.mkdtemp()

        self.context = BmlxContext()
        self.context.local_mode = True
        self.context._store = Metadata(
            local_mode=True, local_storage_path=self.test_dir
        )

        self.seq1 = MockSeq1Component()
        self.seq2 = MockSeq2Component()

        self.pipeline = Pipeline(
            name="test-pipeline", components=[self.seq1, self.seq2]
        )
        # mock artifact storage base
        self.context.project = Mock()
        self.context.project.configure_mock(
            artifact_storage_base=self.artifact_base,
            configs=Configuration(default={}),
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.artifact_base)

    def testExecutionCreation(self):
        runner = Runner(pipeline=self.pipeline, ctx=self.context)

        runner.run(execution_name="test-exe", execution_description="exe desc")
        # get pipeline execution state
        exe, _ = self.context.metadata.store.get_pipeline_executions(
            page_size=100
        )
        self.assertEqual(len(exe), 1, exe)
        exe = exe[0]
        self.assertEqual(exe.name, "test-exe")
        self.assertEqual(exe.description, "exe desc")

        component_executions = self.context.metadata.store.get_component_executions_of_pipeline(
            pipeline_execution=exe,
        )
        self.assertEqual(len(component_executions), 2)
