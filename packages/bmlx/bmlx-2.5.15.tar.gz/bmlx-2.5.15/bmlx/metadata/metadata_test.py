import unittest
import tempfile
import shutil
from bmlx.metadata.metadata import Metadata
from bmlx.proto.metadata import artifact_pb2, execution_pb2
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
from bmlx_openapi_client.dummy_server import setup_api_server


# mock components
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


class MetadataTests(unittest.TestCase):
    def create_mock_pipeline(self) -> Pipeline:
        com_a = MockComponent_A()
        com_b = MockComponent_B(mock_a_input=com_a.outputs["mock_a"])
        pipeline = Pipeline(
            name="test-sequence-pipeline", components=[com_a, com_b]
        )
        return pipeline

    def setUp(self):
        self.metadata = Metadata(
            local_mode=False,
            api_endpoint="http://localhost:8080/api/v1",
            skip_auth=True,
        )

    def tearDown(self):
        pass

    @setup_api_server(8080)
    def testGetOrCreatePipelineExecutionSucc(self):
        # create a light-weighted experiment
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment-ha",
            package_uri="hdfs://bigocluster/user",
            package_checksum="fdsf",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        # create
        ret = self.metadata.get_or_create_pipeline_execution(
            pipeline=self.create_mock_pipeline(),
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(ret.id, 1)
        self.assertEqual(ret.name, "execution_name")
        self.assertEqual(ret.state, execution_pb2.State.RUNNING)
        # get already created
        ret = self.metadata.get_or_create_pipeline_execution(
            pipeline=self.create_mock_pipeline(),
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(ret.id, 1)
        self.assertEqual(ret.name, "execution_name")
        self.assertEqual(ret.state, execution_pb2.State.RUNNING)

    @setup_api_server(8080)
    def testGetPipelineExecutionByIdSucc(self):
        # create a light-weighted experiment
        ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
            package_checksum="fdsf",
        )
        self.assertEqual(int(ret.id), 1)
        ret = self.metadata.get_or_create_pipeline_execution(
            pipeline=self.create_mock_pipeline(),
            experiment_id=ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(ret.id, 1)
        ret = self.metadata.get_pipeline_execution_by_id(1)
        self.assertEqual(ret.id, 1)
        self.assertEqual(ret.name, "execution_name")
        self.assertEqual(ret.state, execution_pb2.State.RUNNING)

    @setup_api_server(8080)
    def testUpdatePipelineExecutionSucc(self):
        # create a light-weighted experiment
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        # create
        ret = self.metadata.get_or_create_pipeline_execution(
            pipeline=self.create_mock_pipeline(),
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(ret.id, 1)
        self.assertEqual(ret.name, "execution_name")
        self.assertEqual(ret.state, execution_pb2.State.RUNNING)
        # update pipeline execution
        updated_execution = ret
        updated_execution.create_time = 123456
        updated_execution.state = execution_pb2.State.SUCCEEDED
        self.assertTrue(
            self.metadata.update_pipeline_execution(updated_execution)
        )

        # get already created
        execution = self.metadata.get_or_create_pipeline_execution(
            pipeline=self.create_mock_pipeline(),
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(execution.id, 1)
        self.assertEqual(execution.name, "execution_name")
        self.assertEqual(execution.state, execution_pb2.State.SUCCEEDED)

    @setup_api_server(8080)
    def testRegisterComponentExecutionSucc(self):
        # create a light-weighted experiment
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        mock_pipeline = self.create_mock_pipeline()
        # create pipeline execution
        ret = self.metadata.get_or_create_pipeline_execution(
            pipeline=mock_pipeline,
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(ret.id, 1)
        self.assertEqual(ret.state, execution_pb2.State.RUNNING)

        # register component execution
        component_a = [
            comp
            for comp in mock_pipeline.components
            if comp.id == "component_a"
        ][0]

        (
            comp_execution,
            inputs,
            outputs,
        ) = self.metadata.register_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=ret,
            component=component_a,
            input_dict={},
        )
        self.assertEqual(comp_execution.id, 1)
        self.assertEqual(comp_execution.type, "component_a")
        self.assertEqual(comp_execution.state, execution_pb2.State.RUNNING)

    @setup_api_server(8080)
    def testUpdateComponentExecutionSucc(self):
        # create a light-weighted experiment
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        mock_pipeline = self.create_mock_pipeline()
        # create pipeline execution
        pip_execution = self.metadata.get_or_create_pipeline_execution(
            pipeline=mock_pipeline,
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(pip_execution.id, 1)
        self.assertEqual(pip_execution.state, execution_pb2.State.RUNNING)

        # register component execution
        component_a = [
            comp
            for comp in mock_pipeline.components
            if comp.id == "component_a"
        ][0]
        (
            comp_execution,
            inputs,
            outputs,
        ) = self.metadata.register_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
        )
        # update component execution
        (
            comp_execution,
            intputs,
            outputs,
        ) = self.metadata.update_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
            output_dict={"mock_a": [MockArtifact_A()]},
            exec_properties={},
        )
        self.assertEqual(comp_execution.id, 1)
        self.assertEqual(comp_execution.type, "component_a")
        self.assertEqual(comp_execution.state, execution_pb2.State.SUCCEEDED)

        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].state, artifact_pb2.Artifact.State.LIVE)
        self.assertEqual(outputs[0].execution_id, "1")
        self.assertEqual(outputs[0].producer_component, "component_a")

    @setup_api_server(8080)
    def testGetPreviousArtifactsSucc(self):
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        mock_pipeline = self.create_mock_pipeline()
        # create pipeline execution
        pip_execution = self.metadata.get_or_create_pipeline_execution(
            pipeline=mock_pipeline,
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(pip_execution.id, 1)
        self.assertEqual(pip_execution.state, execution_pb2.State.RUNNING)

        # register component execution
        component_a = [
            comp
            for comp in mock_pipeline.components
            if comp.id == "component_a"
        ][0]
        self.metadata.register_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
        )
        # update component execution
        self.metadata.update_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
            output_dict={"mock_a": [MockArtifact_A()]},
            exec_properties={},
        )

        previous_artifacts = self.metadata.get_previous_artifacts(
            pipeline_execution=pip_execution
        )
        self.assertTrue("component_a" in previous_artifacts)
        self.assertEqual(len(previous_artifacts["component_a"]), 1)
        self.assertEqual(
            previous_artifacts["component_a"][0].state,
            artifact_pb2.Artifact.State.LIVE,
        )

    @setup_api_server(8080)
    def testExecutePipelineSucc(self):
        # create a light-weighted experiment
        create_exp_ret = self.metadata.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
        )
        self.assertEqual(int(create_exp_ret.id), 1)
        mock_pipeline = self.create_mock_pipeline()
        # create pipeline execution
        pip_execution = self.metadata.get_or_create_pipeline_execution(
            pipeline=mock_pipeline,
            experiment_id=create_exp_ret.id,
            parameters={},
            execution_name="execution_name",
            execution_desc="execution description",
        )
        self.assertEqual(pip_execution.id, 1)
        self.assertEqual(pip_execution.state, execution_pb2.State.RUNNING)

        # register component execution
        component_a = [
            comp
            for comp in mock_pipeline.components
            if comp.id == "component_a"
        ][0]
        (
            comp_execution,
            inputs,
            outputs,
        ) = self.metadata.register_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
        )
        # component_a execute.....
        # update component execution
        (
            comp_execution,
            intputs,
            outputs,
        ) = self.metadata.update_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_a,
            input_dict={},
            output_dict={
                "mock_a": [
                    MockArtifact_A(
                        meta=artifact_pb2.Artifact(
                            uri="hdfs://bigo-rt/user/bmlx/artifact.gz"
                        )
                    )
                ]
            },
            exec_properties={},
        )
        self.assertEqual(comp_execution.id, 1)
        # get artifact generated by component_a
        previous_artifacts = self.metadata.get_previous_artifacts(
            pipeline_execution=pip_execution
        )
        self.assertTrue("component_a" in previous_artifacts)
        self.assertEqual(len(previous_artifacts["component_a"]), 1)

        # component_b execute.....
        component_b = [
            comp
            for comp in mock_pipeline.components
            if comp.id == "component_b"
        ][0]
        (
            comp_execution,
            inputs,
            outputs,
        ) = self.metadata.register_component_execution(
            pipeline=mock_pipeline,
            pipeline_execution=pip_execution,
            component=component_b,
            input_dict={
                "mock_a_input": [
                    MockArtifact_A(meta=previous_artifacts["component_a"][0])
                ]
            },
        )
        self.assertEqual(comp_execution.type, "component_b")
        self.assertEqual(comp_execution.state, execution_pb2.State.RUNNING)
