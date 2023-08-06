import os
import copy
import unittest
import yaml
import tempfile
from bmlx.project_spec import Project


yaml_content = """
name: demo-pipeline
namespace: mlplat
experiment: Default
description: "demo pipeline for bmlx tutorial"
entry: pipeline.py
configurables:
  bmlx.yml:
    - parameters.*
    - settings.*

# parameters 可能经常变动
parameters:
  fg_conf_path: "hdfs://bigo-rt/user/bmlx/fg/likee-follow/ori_fg.yml"
  sample_uri_base: "hdfs://bigocluster/user/alg_rank/like/trainDataMr/mr_feature_processor_xdl_follow/OTHER/"
  model_uri_base: hdfs://bigo-rt/user/bmlx/checkpoints/demo-pipeline/"
  start_sample_hour: "20200713/20"
  end_sample_hour: ""
  max_input_hours:
    value: 1
    validator: {name: maxmin, parameters: {max: 24, min: 1}}
# settings 一般很少变动，主要是一些使用资源的配置
settings:
  # pipeline 级别的setting
  pipeline:
    image:
      name: harbor.bigo.sg/mlplat/bmlx:0.5.15
"""


class ProjectSpecTest(unittest.TestCase):
    def createTmpProject(self, bmlx_dict):
        tmp = tempfile.TemporaryDirectory()
        tempdir = tmp.name
        os.chdir(tempdir)

        pipeline_path = os.path.join(tempdir, "pipeline.py")
        with open(pipeline_path, "w") as f:
            f.write("test")

        bmlx_yml_path = os.path.join(tempdir, "bmlx.yml")
        yaml_content = yaml.dump(bmlx_dict)
        print(yaml_content)
        with open(bmlx_yml_path, "w") as f:
            f.write(yaml_content)

        return tmp, bmlx_yml_path

    def testGetConfigurableSuccess(self):
        yaml_dict = yaml.load(yaml_content, Loader=yaml.FullLoader)
        _, bmlx_yml_path = self.createTmpProject(yaml_dict)

        project = Project(config_name=bmlx_yml_path)
        configs = project.configurables()
        self.assertEqual(len(configs), 7)
        self.assertEqual("bmlx.settings.pipeline.image.name", configs[-1][0])

    def testSecrets(self):
        add = ["secret1", ["secret1"], ["secret1", "secret2"]]
        yaml_dict = yaml.load(yaml_content, Loader=yaml.FullLoader)
        for secrets in add:
            yd = copy.deepcopy(yaml_dict)
            yd["settings"]["pipeline"]["image"]["pull_secrets"] = secrets
            _, bmlx_yml_path = self.createTmpProject(yd)

            project = Project(config_name=bmlx_yml_path)
            my_secrets = project.configs["settings"]["pipeline"]["image"][
                "pull_secrets"
            ].as_str_seq()
            ref_secrets = secrets if isinstance(secrets, list) else [secrets]
            self.assertTrue(isinstance(my_secrets, list))
            self.assertTrue(my_secrets == ref_secrets)
