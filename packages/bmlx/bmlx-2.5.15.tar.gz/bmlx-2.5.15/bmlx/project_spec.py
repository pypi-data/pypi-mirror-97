"""Internal utilities for parsing MLproject YAML files."""

import os
import logging
import pathlib
import glob
import tempfile
import zipfile
import json
import yaml
import shutil
import re
from distutils.dir_util import copy_tree

from typing import Text, Optional

from bmlx import config as bmlx_config
from bmlx.cli.cli_exception import BmlxCliException
from bmlx.cli.constants import (
    BMLX_CONFIG_FILE,
    BMLX_PIPELINE_ENTRY,
)
from bmlx.utils import io_utils, checksum_utils

MY_DIR = os.path.dirname(os.path.realpath(__file__))

_CONFIG_VALIDATION = {
    "name": str,
    "namespace": bmlx_config.String(default=""),
    "description": bmlx_config.String(default=""),
    "local": bmlx_config.Choice([True, False]),
    "entry": bmlx_config.Filename(),
    "tags": bmlx_config.StrSeq(),
    "package": {"include": bmlx_config.StrSeq(),},
    "configurables": {},
    "parameters": {},
    "settings": {
        "pipeline": {
            "image": {
                "name": str,
                "pull_secrets": bmlx_config.StrSeq(),
                "pull_policy": str,
            },
            "components": {"version": str},
        },
    },
}


class _ProjectPackingContext(tempfile.TemporaryDirectory):
    __slots__ = ["_project"]

    def __init__(self, project, runtime_generators=[]):
        self._project = project
        self._project.package = None
        self._project.checksum = None
        self._runtime_generators = runtime_generators
        super(_ProjectPackingContext, self).__init__(prefix=self._project.name)

    def __enter__(self):
        tmpdir = super(_ProjectPackingContext, self).__enter__()
        base_dir = os.path.join(tmpdir, self._project.name)
        for f in self._project._get_package_files():
            rel_path = os.path.relpath(f, self._project.base_path)
            dst_path = os.path.join(base_dir, rel_path)
            if os.path.isdir(f) and not os.path.exists(f):
                shutil.copytree(f, dst_path, copy_function=shutil.copy2)
            else:
                if not os.path.exists(os.path.dirname(dst_path)):
                    os.makedirs(os.path.dirname(dst_path))
                shutil.copy2(f, os.path.join(base_dir, rel_path))

        for generator in self._runtime_generators:
            generator(base_dir)

        # archive to zip file
        zip_file = os.path.join(tmpdir, self._project.name + ".zip")
        os.listdir(base_dir)
        cksum = checksum_utils.dirhash(base_dir)

        io_utils.zip_dir(base_dir, zip_file)

        self._project.package = zip_file
        self._project.checksum = (
            "r%s" % cksum
        )  # pyyaml could not handle leading zero's with quote, so add a r prefix would fix this issue
        return (self._project.package, self._project.checksum)

    def __exit__(self, exc_type, exc_value, exc_traceback):

        self._project.package = None
        self._project.checksum = None
        super(_ProjectPackingContext, self).__exit__(
            exc_type, exc_value, exc_traceback
        )


class Project(object):
    __slots__ = [
        "_data",
        "name",
        "namespace",
        "description",
        "base_path",
        "artifact_storage_base",
        "bmlx_config_path",
        "pipeline_path",
        "package",
        "checksum",
        "components_version",
        "tags",
    ]

    """A project specification loaded from an BMLX project file in the passed-in directory."""

    def __init__(self, config_name=None, entry=None, env="prod"):
        if config_name is None:
            config_name = BMLX_CONFIG_FILE

        self._locate_config_file(config_name)
        self._load(entry, env)

    @classmethod
    def load_from_remote(
        cls,
        pipeline_storage_base: Text,
        dst: Text,
        package: Text,
        checksum: Text,
        package_uri: Text = "",
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            from bmlx.metadata.metadata import Metadata

            if package_uri:
                ret = Metadata._download_package(
                    input_path=package_uri,
                    output_path=f"{tmpdir}/{package}.zip",
                )
            else:
                ret = Metadata.download_package(
                    pipeline_storage_path=pipeline_storage_base,
                    package_name=package,
                    checksum=checksum,
                    local_dir=tmpdir,
                )
            if not ret:
                raise RuntimeError(
                    "Failed to download package with package name: %s, checksum: %s"
                    % (package, checksum)
                )

            with zipfile.ZipFile(
                os.path.join(tmpdir, package + ".zip"), "r"
            ) as zip_ref:
                zip_ref.extractall(tmpdir)
                logging.debug("extracting package %s to %s" % (package, tmpdir))
            copy_tree(os.path.join(tmpdir), dst)

    @property
    def configs(self) -> bmlx_config.Configuration:
        return self._data

    @configs.setter
    def configs(self):
        raise AttributeError("data should not set ouside project")

    def packing(self, runtime_generators=[]):
        return _ProjectPackingContext(
            self, runtime_generators=runtime_generators
        )

    def _locate_config_file(self, config_name):
        cur = pathlib.Path(os.getcwd())

        while True:
            conf_file = pathlib.Path(cur, config_name)
            if conf_file.exists():
                self.base_path = cur.as_posix()
                self.bmlx_config_path = conf_file.as_posix()
                break
            if cur.as_posix() == cur.root:
                raise BmlxCliException(
                    "not a bmlx pipeline (or any of the parent directories): bmlx.yml"
                )

            cur = cur.parent

    def _load(self, entry: Optional[Text] = None, env: Text = "prod"):
        self._data = bmlx_config.Configuration(
            os.path.join(MY_DIR, "bmlx.yml"),
            self.bmlx_config_path,
            value_converter=lambda x: x["value"]
            if isinstance(x, dict) and "value" in x
            else x,
        )
        self._data.get(_CONFIG_VALIDATION)  # validate schema

        self.name = self._data["name"].as_str()
        self.namespace = self._data["namespace"].as_str()
        self.description = self._data["description"].as_str()
        self.tags = self._data["tags"].as_str_seq()

        if self._data["settings"]["pipeline"]["artifact_storage_base"].exists():
            val = self._data["settings"]["pipeline"][
                "artifact_storage_base"
            ].get()
            if isinstance(val, dict):
                self.artifact_storage_base = val[env]
            elif isinstance(val, str):
                self.artifact_storage_base = val
        assert (
            self.artifact_storage_base
        ), "artifact storage base must be provided!"

        user_assigned_edp_bkt = {}
        # bmlx.yml添加endpoint/bucket_name和aksk信息
        if self._data["settings"]["pipeline"]["s3_storage"].exists():
            for name in self._data["settings"]["pipeline"]["s3_storage"]:
                user_assigned_edp_bkt[name] = {
                    "endpoint": self._data["settings"]["pipeline"][
                        "s3_storage"
                    ][name]["endpoint"].as_str(),
                    "access_key": self._data["settings"]["pipeline"][
                        "s3_storage"
                    ][name]["access_key"].as_str(),
                    "secret_key": self._data["settings"]["pipeline"][
                        "s3_storage"
                    ][name]["secret_key"].as_str(),
                }
        io_utils.update_storage_map(user_assigned_edp_bkt)

        self.components_version = self._data["settings"]["pipeline"][
            "components"
        ]["version"].as_str()

        # set base paths
        self._data.relatives = {
            "artifacts": self.artifact_storage_base,
            "project": self.base_path,
        }

        # resolve pipeline entry
        self.pipeline_path = (
            entry or self._data["entry"].as_str() or BMLX_PIPELINE_ENTRY
        )

        logging.debug("detected pipeline base path: %s" % self.pipeline_path)

        if not io_utils.exists(self.pipeline_path):
            raise BmlxCliException(
                "entrypoint not found, please set 'entry' to bmlx.yml or add"
                "a file named 'pipeline.py' in your project"
            )

        logging.debug(
            "loaded project %s, entry_point: %s, base_artifact_storage_path: %s"
            % (self.name, self.pipeline_path, self.artifact_storage_base)
        )

    def resolve_artifact_fs_path(self, path, is_uri=False):
        pure_path = pathlib.PurePath(path)
        if not pure_path.is_absolute():
            pure_path = os.path.join(
                self.artifact_storage_base, pure_path.as_posix()
            )
        else:
            pure_path = pure_path.as_posix()

        return io_utils.resolve_filesystem_and_path(pure_path, is_uri)

    def resolve_project_path(self, path):
        pure_path = pathlib.Path(path)
        if pure_path.is_absolute():
            pure_path = pure_path.as_posix()
        else:
            pure_path = pathlib.Path(self.base_path, path).as_posix()

        return io_utils.resolve_filesystem_and_path(pure_path)

    def _get_package_files(self):
        assert self.base_path
        result = []

        for include in self.configs["package"]["include"].as_str_seq():
            for fn in glob.glob(
                os.path.join(self.base_path, include), recursive=True
            ):
                result.append(fn)
        result = list(filter(os.path.isfile, set(result)))

        spec_file = os.path.join(self.base_path, ".workflow_spec.json")
        if io_utils.exists(spec_file):
            result.append(spec_file)

        return result

    # 返回可以在页面上设置的参数，比如 parameters, settings, hyper parameters
    # 具体可以看 project_spec_test.py 的testGetConfigurableSuccess 函数
    def configurables(self):
        def resolve_config_xpath_pairs(cur_dict, cur_xpath):
            if isinstance(cur_dict, dict):
                if "value" in cur_dict and (
                    "description" in cur_dict or "validator" in cur_dict
                ):
                    return [(cur_dict, cur_xpath)]
                else:
                    result = []
                    for k, v in cur_dict.items():
                        if len(k.split(".")) > 1:
                            raise ValueError(
                                "configurable parameter should not have key contains dot, invalid key %s"
                                % k
                            )
                        result += resolve_config_xpath_pairs(
                            v, ".".join([cur_xpath, k])
                        )
                    return result
            elif isinstance(cur_dict, list):
                raise ValueError(
                    "list type configurable parameters %s is not supported now, only flatten key-value is supported!"
                    % cur_xpath
                )
                # print(
                #     "list type configurable parameters {} is not supported now, only flatten key-value is supported!".format(
                #         cur_xpath
                #     )
                # )
                # return []
            else:
                return [(cur_dict, cur_xpath)]

        def xpath_get(content_dict, xpath):
            cur_dict = content_dict
            xpath_splits = [x for x in xpath.split(".") if x != "*"]
            for i, x in enumerate(xpath_splits):
                if x not in cur_dict:
                    raise ValueError(
                        "xpath %s does not exist in content_dict %s"
                        % (xpath, content_dict)
                    )
                cur_dict = cur_dict[x]
            return cur_dict

        def resolve_patterns(file_name, pattern):
            file_path = os.path.join(
                os.path.dirname(self.bmlx_config_path), file_name
            )
            if not io_utils.exists(file_path):
                raise ValueError("file path %s does not exist!" % file_path)
            with open(file_path, "r") as f:
                content_dict = yaml.load(f, yaml.Loader)
                pattern_dict = xpath_get(content_dict, pattern)
                config_xpath_pairs = resolve_config_xpath_pairs(
                    pattern_dict, pattern.strip(".*")
                )
                return [
                    (
                        f"{os.path.splitext(file_name)[0]}.{element[1]}",
                        element[0],
                    )
                    for element in config_xpath_pairs
                ]

        result = []
        if not self._data["configurables"].exists():
            return result
        params_dict = self._data["configurables"].get(dict)
        # file_name 是相对于 bmlx.yml 的相对路径
        for file_name, patterns in params_dict.items():
            if not file_name.endswith(".yml"):
                raise ValueError("configure file's extension should be .yml")
            if not isinstance(patterns, list):
                raise ValueError(
                    "Invalid configurables, should be dict[file_name, list[patterns]]"
                )
            for pattern in patterns:
                result.extend(resolve_patterns(file_name, pattern))
        return result
