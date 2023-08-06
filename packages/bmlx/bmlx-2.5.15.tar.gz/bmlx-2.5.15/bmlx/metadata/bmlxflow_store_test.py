import unittest
from bmlx.metadata.bmlxflow_store import BmlxflowStore
import os
import time
import json
import pathlib
from bmlx_openapi_client.dummy_server import setup_api_server


class BmlxflowStoreTest(unittest.TestCase):
    def setUp(self):
        self.store = BmlxflowStore(
            api_endpoint="http://localhost:8080/api/v1", skip_auth=True
        )

    def tearDown(self):
        pass

    @setup_api_server(8080)
    def testGetOrCreatePipelineSuccCreate(self):
        ret = self.store.get_or_create_pipeline(
            name="good-pipeline",
            repo="https://git.sysop.bigo.sg/bmlx-pipelines/likee_search_russia",
            user_name="sunkaicheng",
            description="this is a good pipeline",
        )
        self.assertEqual(ret.owner, "sunkaicheng")
        self.assertEqual(
            ret.repo,
            "https://git.sysop.bigo.sg/bmlx-pipelines/likee_search_russia",
        )

    @setup_api_server(8080)
    def testGetOrCreatePipelineSuccGet(self):
        ret = self.store.get_or_create_pipeline(
            name="good-pipeline",
            repo="https://git.sysop.bigo.sg/bmlx-pipelines/likee_search_russia",
            user_name="sunkaicheng",
            description="this is a good pipeline",
        )
        self.assertEqual(ret.owner, "sunkaicheng")
        self.assertEqual(int(ret.id), 1)
        # same repo
        ret = self.store.get_or_create_pipeline(
            name="good-pipeline",
            repo="https://git.sysop.bigo.sg/bmlx-pipelines/likee_search_russia",
            user_name="sunkaicheng",
            description="this is a good pipeline",
        )
        self.assertEqual(ret.owner, "sunkaicheng")
        self.assertEqual(int(ret.id), 1)

    @setup_api_server(8080)
    def testCreatePipelineVersionSucc(self):
        ret = self.store.get_or_create_pipeline(
            name="good-pipeline",
            repo="https://git.sysop.bigo.sg/bmlx-pipelines/likee_search_russia",
            user_name="sunkaicheng",
            description="this is a good pipeline",
        )
        self.assertEqual(ret.owner, "sunkaicheng")

        ret = self.store.create_pipeline_version(
            pipeline_id=int(ret.id),
            version="1.0.1",
            commit_id="fdfdsfdsf",
            package_uri="hdfs://bigocluster/user",
            package_checksum="fdsfd",
        )
        self.assertEqual(int(ret.id), 1)

    @setup_api_server(8080)
    def testCreateLightWeightExperiment(self):
        ret = self.store.create_light_weight_experiment(
            name="this-is-a-specical-experiment",
            package_uri="hdfs://bigocluster/user",
            package_checksum="fdsfd",
            dag=[],
        )
        self.assertEqual(int(ret.id), 1)
