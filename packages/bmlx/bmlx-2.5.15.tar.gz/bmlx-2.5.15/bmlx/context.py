import itertools
import logging
import sys
import yaml
import copy
from string import Template
from typing import Text, Dict, Any, Optional
from bmlx.alarm import AlarmManager, Receipt
from bmlx.project_spec import Project
from bmlx.bmlx_ini import BmlxINI
from bmlx.utils.import_utils import import_class_by_path
from bmlx.flow.hook import Hook
from bmlx.alarm import Alarm, Level


class DefaultAlarmHook(Hook):
    def onComponentDone(
        self, context, pipeline, pipeline_execution, component, ret
    ):
        if ret.status == Hook.Status.FAIL:
            context.alert_manager.emit_alarms(
                [
                    Alarm(
                        level=Level.WARNING,
                        vars={
                            "message": "execute pipeline %s, component %s error"
                            % (pipeline.meta.name, component.id),
                            "pipeline": pipeline,
                            "context": context,
                            "pipeline_execution": pipeline_execution,
                        },
                    )
                ]
            )

    def onPipelineDone(self, context, pipeline, pipeline_execution, ret):
        if ret.status == Hook.Status.FAIL:
            context.alert_manager.emit_alarms(
                [
                    Alarm(
                        level=Level.WARNING,
                        vars={
                            "message": "execute pipeline %s error"
                            % pipeline.meta.name,
                            "pipeline": pipeline,
                            "context": context,
                            "pipeline_execution": pipeline_execution,
                        },
                    )
                ]
            )


class BmlxContext(object):
    """
    Context shared between all command groups.
    there are two types of fields,
    one is parameters could be changed by commandline, it could be access by ctx.local ctx.hparams
    another is project spec fields, which could be access by ctx.project, such as ctx.project.name
    """

    __slots__ = [
        "local_mode",
        "env",
        "skip_auth",
        "user",
        "token",
        "project",
        "namespace",
        "dry_run",
        "custom_parameters",
        "settings",
        "debug",
        "engine",
        "package",
        "checksum",
        "package_uri",
        "workflow_id",
        "_store",
        "pipeline_storage_base",
        "alert_manager",
        "hooks",
        "_extra_custom_parameters",
    ]

    def __init__(self):
        self._store = None
        self.project = None
        self.alert_manager = None
        self.user = ""
        self.package = ""
        self.checksum = ""
        self.hooks = []
        self._extra_custom_parameters = {}

    def init(
        self,
        local_mode: Optional[bool] = False,
        env: Optional[Text] = "prod",
        skip_auth: Optional[bool] = False,
        namespace: Optional[Text] = None,
        custom_config_file: Optional[Text] = None,
        custom_entry_file: Optional[
            Text
        ] = None,  # 用于强制指定 bmlx run 使用的 pipeline 文件
        custom_parameters: Optional[Dict[Text, Any]] = {},
        dry_run: Optional[bool] = False,
        debug: Optional[bool] = False,
        engine: Optional[Text] = "bmlxflow",
        workflow_id: Optional[Text] = "",
        auth: bool = True,
        package_uri: Optional[Text] = "",
    ):
        self.local_mode = local_mode
        self.env = env
        self.skip_auth = skip_auth
        self.package_uri = package_uri
        self.project = Project(custom_config_file, custom_entry_file, env)
        sys.path.append(self.project.base_path)
        self.namespace = (
            namespace or self.project.configs["namespace"].as_str() or "default"
        )
        self.dry_run = dry_run
        self.debug = debug
        self.engine = engine

        if self.project.configs["settings"]["pipeline"][
            "pipeline_storage_base"
        ].exists():
            val = self.project.configs["settings"]["pipeline"][
                "pipeline_storage_base"
            ].get()
            if isinstance(val, dict):
                self.pipeline_storage_base = val[env]
            elif isinstance(val, str):
                self.pipeline_storage_base = val

        assert (
            self.pipeline_storage_base
        ), "pipeline storage base must be provided!"

        self.workflow_id = workflow_id
        bmlx_ini = BmlxINI(env)
        self.user = bmlx_ini.user
        self.token = bmlx_ini.token

        if self.project.configs["alert"].exists():
            self.alert_manager = AlarmManager.load_from_config(
                self.project, self.project.configs["alert"]
            )
            if self.local_mode:
                self.alert_manager.limit_receipt_types(
                    [Receipt.Type.CONSOLE]
                )  # 本地模式只打开本地打印报警，不发邮件和微信
            self.hooks.append(DefaultAlarmHook())

        for hook_path in self.project.configs["hooks"]:
            hook_cls = import_class_by_path(hook_path.as_str())
            if not issubclass(hook_cls, Hook):
                raise RuntimeError(
                    "invalid calss %s, must be subclass of bmlx.flow.pipeline.hook.Hook"
                    % hook_cls
                )
            self.hooks.append(hook_cls())
        # 从 bmlx.yml 中获取 custom_parameters
        self.custom_parameters = self.project.configs["parameters"]
        self.settings = self.project.configs["settings"]
        self._extra_custom_parameters = (
            custom_parameters or self._extra_custom_parameters
        )
        self.rewrite_custom_parameters(custom_parameters)

    def rewrite_custom_parameters(self, custom_parameters):
        # 使用命令行中的覆盖
        updated_dict = {}
        for k, v in custom_parameters.items():
            # TODO: 让前端做这个归一化的操作，不要这里来做 @zhangguanxing
            k = k.replace("bmlx.parameters.", "")
            ref = self.custom_parameters
            key_exist = True
            for p in k.split("."):
                if ref[p].exists():
                    ref = ref[p]
                else:
                    key_exist = False
                    break
            if not key_exist:
                logging.warning(
                    "key %s does not exist in ctx.custom_parameters", k
                )
                continue

            if isinstance(ref.get(), int):
                updated_dict[k] = int(v)
            elif isinstance(ref.get(), float):
                updated_dict[k] = float(v)
            elif isinstance(ref.get(), bool):
                updated_dict[k] = bool(v)
            else:
                updated_dict[k] = v
        self.custom_parameters.set_args(updated_dict)

    def render_configs(
        self, tpl: Text, additional: Optional[Dict[Text, Any]] = {}
    ):
        return self.custom_parameters.render(Template(tpl), additional)

    def render_file(
        self, file: Text, additional: Optional[Dict[Text, Any]] = {}
    ):
        with open(file, "r") as fd:
            return self.render_configs(fd.read(), additional=additional)

    def __str__(self):
        return ", ".join(
            [key + ": " + str(getattr(self, key)) for key in self.__slots__]
        )

    @property
    def metadata(self):
        from bmlx.metadata.metadata import Metadata

        if not self._store:
            self._store = Metadata(
                local_mode=self.local_mode,
                env=self.env,
                skip_auth=self.skip_auth,
            )
        return self._store

    def image(self):
        """
        get running image, we would use bmlx image as default
        but user's could override image
        """
        from bmlx import __version__

        return (
            self.project.configs["settings"]["pipeline"]["image"][
                "name"
            ].as_str("harbor.bigo.sg/mlplat/bmlx:%s" % __version__),
            self.project.configs["settings"]["pipeline"]["image"][
                "pull_secrets"
            ].as_str_seq(),
            self.project.configs["settings"]["pipeline"]["image"][
                "policy"
            ].as_str("Always"),
        )

    def dnsPolicy(self):
        return self.project.configs["settings"]["pipeline"][
            "dns_policy"
        ].as_str()

    def dnsConfig(self):
        return {
            "nameservers": self.project.configs["settings"]["pipeline"][
                "dns_config"
            ]["nameservers"].as_str_seq(),
        }

    def generate_component_run_command(
        self,
        component_id: Text,
        execution_name: Text,
        experiment_id: Text = "",
        entry: Text = None,
        extra: Optional[Dict[Text, Any]] = {},
        collect_log=False,
        sub_component=False,
        need_workflow_inject=False,
        checksum: Text = "",  # chksum 用来替换默认的 self.checksum
        package_uri: Text = "",  # 如果 package_uri 非空，则使用 package_uri 获取package；否则使用 package+checksum 获取
    ):
        """
        FOR internal developers:
        custom_arguments shoud be Text:Text Format, you could parse these arguments
        in component/launcher implements
        """
        argv = []
        if collect_log:
            argv = ["log_collector"]
        argv.extend(
            [
                "bmlx_rt",
                "run",
                "--namespace",
                self.namespace,
                "--entry",
                entry or self.project.pipeline_path,
                "--env",
                self.env,
                "--skip_auth",
                "true",
            ]
        )
        if experiment_id:
            argv.extend(["--experiment_id", experiment_id])

        # local run does not need to download package
        if not self.local_mode:
            assert checksum or self.checksum or package_uri
            argv.extend(
                [
                    "--package",
                    self.project.name,
                    "--pipeline_storage_base",
                    self.pipeline_storage_base,
                    "--checksum",
                    checksum or self.checksum,
                    "--package_uri",
                    package_uri or self.package_uri,
                ]
            )
        else:
            argv.extend(["--local"])

        # bmlxflow使用argo variable，是可以在argo模板中注入此次运行的唯一id
        # 这个可以方便后期追踪相关任务
        if need_workflow_inject:
            argv.extend(["--workflow_id", "{{workflow.uid}}"])

        for k, v in itertools.chain(extra.items()):
            argv.extend(["-T", "{}={}".format(k, v)])

        for k, v in self._extra_custom_parameters.items():
            argv.extend(["-P", "{}={}".format(k, v)])

        argv.extend(["-E", execution_name])
        argv.extend([component_id])
        if sub_component:
            argv.append("--sub_component")

        logging.debug("generated command %s" % argv)
        return argv

    def generate_pipeline_cleanup_command(
        self,
        execution_name: Text,
        checksum: Text,
        entry: Text = None,
        experiment_id: Text = "",
        package_uri: Text = "",  # 如果 package_uri 非空，则使用 package_uri 获取package；否则使用 package+checksum 获取
    ):
        argv = []
        argv.extend(
            [
                "bmlx_rt",
                "cleanup",
                "--package",
                self.project.name,
                "--checksum",
                checksum or self.checksum,
                "--package_uri",
                package_uri or self.package_uri,
                "--namespace",
                self.namespace,
                "--entry",
                entry or self.project.pipeline_path,
                "--env",
                self.env,
                "--pipeline_storage_base",
                self.pipeline_storage_base,
                "--skip_auth",
                "true",
                "--workflow_id",
                "{{workflow.uid}}",
                "--workflow_status",
                "{{workflow.status}}",
            ]
        )
        if experiment_id:
            argv.extend(["--experiment_id", experiment_id])

        argv.extend(["-E", execution_name])
        logging.debug("generated command %s" % argv)
        return argv
