# 本地多进程runner
# 应用场景： 一个pipeline中多个xdl 任务，xdl 任务启动后会创建很多的内存对象。
# 如果在同一个进程下连续使用会有问题。因此使用多进程
import os
import atexit
import logging
import subprocess
import select
import signal
from typing import Text, Dict, Any

from bmlx.flow import Pipeline, Component
from bmlx.execution.runner import Runner


def cleanup():
    logging.info("multiprocess runner cleanup: try to kill process group")
    os.killpg(0, signal.SIGKILL)


class MultiProcessRunner(Runner):
    def _run_command(self, command):
        proc = subprocess.Popen(
            command,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        poll_obj = select.poll()
        poll_obj.register(proc.stdout, select.POLLIN)
        out = ""
        while proc.poll() is None or out:
            poll_ret = poll_obj.poll(1000)
            if poll_ret:
                out = proc.stdout.readline()
                if out.strip("\n"):
                    print(out.strip("\n"))
                    out = ""
        return proc.poll()

    def run(self, execution_name: Text, execution_description: Text) -> None:
        """
        local multi-process runner, this would run in topo sort order
        """
        os.setpgrp()
        atexit.register(cleanup)

        self._pipeline_execution = self._ctx.metadata.get_or_create_pipeline_execution(
            experiment_name=self._ctx.experiment,
            pipeline=self._pipeline,
            execution_name=execution_name,
            execution_desc=execution_description,
        )

        logging.info(
            "[MultiProcessRuner] pipeline {} start (id: {})".format(
                self._pipeline.meta.name, self._pipeline_execution.id,
            )
        )
        # TODO: 可优化成多进程并行执行多个可并行执行的component
        for component in self._pipeline.components:
            command = self._ctx.generate_component_run_command(
                component_id=component.id,
                execution_name=execution_name,
                collect_log=False,
                need_workflow_inject=False,
            )
            ret = self._run_command(command)
            logging.info(
                "finished component %s with exit code: %d", component.id, ret
            )
            if ret != 0:
                break
