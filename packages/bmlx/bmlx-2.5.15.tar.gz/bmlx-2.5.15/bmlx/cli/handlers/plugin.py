import sys
import logging
import click
import subprocess
import time
import random
from datetime import datetime
from typing import Text

TOTAL_TRY_COUNT = 3


def update(version: Text):
    if version == "local":
        logging.info("use local installed bmlx-components package")
        return

    command = (
        "pip uninstall -y bmlx-components && "
        "pip install bmlx-components"
    )
    if version == "latest":
        version = ""

    if version:
        command = f"{command}=={version}"

    try_cnt = 0
    random_initialized = False
    while try_cnt < TOTAL_TRY_COUNT:
        ret = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if ret.returncode == 0:
            break
        if not random_initialized:
            random.seed(int(datetime.now().timestamp() * 1000))
            random_initialized = True

        sleep_seconds = random.uniform(1, 5)
        logging.warn(
            "Failed to install bmlx_component package, retrying after %.4f seconds..",
            sleep_seconds,
        )
        time.sleep(sleep_seconds)
        try_cnt += 1

    if ret.returncode != 0:
        logging.error("update bmlx-components failed, error: %s", ret.stdout)
        sys.exit(-1)
    else:
        click.echo(
            "update bmlx-components to version: %s successfully"
            % (version or "latest")
        )
