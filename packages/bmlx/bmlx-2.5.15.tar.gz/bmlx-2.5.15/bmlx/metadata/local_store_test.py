import unittest
import tempfile
import shutil
from bmlx.proto.metadata import artifact_pb2, execution_pb2
import bmlx.metadata.local_store as ks


class LocalStoreTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.store = ks.LocalStore(local_storage_path=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def testExtractSpec(self):
        artifact = artifact_pb2.Artifact(id=123, uri="http://www.bigo.sg",)
        ret = ks._artifact_b2m(artifact=artifact)
        self.assertEqual(
            ret.properties["uri"].string_value, "http://www.bigo.sg"
        )
        self.assertEqual(ret.properties["id"].int_value, 123)

    def testCreateArtifact(self):
        artifact = artifact_pb2.Artifact(
            uri="https://www.bigo.sg",
            name="MockName",
            type="MockType",
            state=artifact_pb2.Artifact.State.LIVE,
        )

        [artifact_id] = self.store.create_artifacts([artifact])
        saved = self.store.get_artifacts_by_id([artifact_id])[0]

        self.assertEqual(saved.uri, artifact.uri)
        self.assertEqual(saved.name, artifact.name)
        self.assertEqual(saved.type, artifact.type)
        self.assertEqual(saved.state, artifact.state)

        artifact_type = self.store._ml_store.get_artifact_types_by_id(
            [saved.type_id]
        )[0]
        self.assertEqual(artifact_type.name, artifact.type)

    def testCreateComponentExecution(self):
        exe = execution_pb2.Execution()
        exe.name = "Test_A"
        exe.description = "desc"

        ctx = self.store._make_mlpb_context(
            context_type=ks._PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=ks._PIPELINE_EXECUTION_SPEC,
            context_name=exe.name,
            bmlx_pb_msg=exe,
        )
        [ctx.id] = self.store._ml_store.put_contexts([ctx])
        exe.context_id = ctx.id

        inputs = [
            artifact_pb2.Artifact(type="artifact_A", uri="s3://schema_a",),
            artifact_pb2.Artifact(type="artifact_B", uri="s3://schema_b",),
        ]

        outputs = [
            artifact_pb2.Artifact(type="artifact_C", uri="s3://schema_c",),
        ]

        ce = execution_pb2.ComponentExecution(
            name="execution_1",
            state=execution_pb2.State.NOT_STARTED,
            type="Train",
        )

        (
            saved,
            saved_inputs,
            saved_outputs,
        ) = self.store.create_or_update_component_execution(
            exe, ce, inputs, outputs
        )
        self.assertEqual(saved.name, ce.name)
        self.assertEqual(saved.state, ce.state)
        self.assertEqual(saved.type, ce.type)

        self.assertEqual(len(saved_inputs), 2)
        self.assertEqual(saved_inputs[0].uri, inputs[0].uri)
        self.assertEqual(saved_inputs[1].uri, inputs[1].uri)
        self.assertEqual(len(saved_outputs), 1)
        self.assertEqual(saved_outputs[0].uri, outputs[0].uri)

        exe_type = self.store._ml_store.get_execution_types_by_id(
            [saved.type_id]
        )[0]
        self.assertIsNotNone(exe_type)

    def testPipelineExcutionAndContext(self):
        exe = execution_pb2.Execution()
        exe.name = "Test_A"
        exe.description = "desc"

        ctx = self.store._make_mlpb_context(
            context_type=ks._PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=ks._PIPELINE_EXECUTION_SPEC,
            context_name=exe.name,
            bmlx_pb_msg=exe,
        )
        [ctx.id] = self.store._ml_store.put_contexts([ctx])

        saved = self.store._get_pipeline_execution_context(ctx.id)
        self.assertEqual(saved.name, exe.name)
        self.assertEqual(saved.description, exe.description)
        exe.context_id = ctx.id

        a = artifact_pb2.Artifact(
            name="a", type="artifact_A", uri="s3://schema_a",
        )
        b = artifact_pb2.Artifact(
            name="b", type="artifact_B", uri="s3://schema_b",
        )

        ce1 = execution_pb2.ComponentExecution(
            name="execution_1",
            state=execution_pb2.State.NOT_STARTED,
            type="Train_A",
        )

        ce2 = execution_pb2.ComponentExecution(
            name="execution_1",
            state=execution_pb2.State.NOT_STARTED,
            type="Train_B",
        )

        # test tracking
        self.store.create_or_update_component_execution(
            exe, ce1, input_artifacts=[a], output_artifacts=[b]
        )

        self.store.create_or_update_component_execution(
            exe, ce2, input_artifacts=[b]
        )

        saved_ces = self.store.get_component_executions_of_pipeline(exe)
        self.assertEqual(len(saved_ces), 2)

        inputs, outputs = self.store.get_component_executions_artifacts(
            [saved_ces[0]]
        )
        self.assertTrue(len(inputs), 1)
        self.assertTrue(inputs[0].uri, a.uri)
        self.assertTrue(len(outputs), 1)
        self.assertTrue(outputs[0].uri, b.uri)
