import os
import io
import sys
import posixpath
import contextlib
import pyarrow.lib as lib
from bmlx.fs.file_system import FileSystem


class HadoopFileSystem(lib.HadoopFileSystem, FileSystem):
    def __init__(
        self,
        host="default",
        port=0,
        user=None,
        kerb_ticket=None,
        driver="libhdfs",
        extra_conf=None,
    ):
        if driver == "libhdfs":
            _maybe_set_hadoop_classpath()

        self._connect(host, port, user, kerb_ticket, driver, extra_conf)

    def __reduce__(self):
        return (
            HadoopFileSystem,
            (
                self.host,
                self.port,
                self.user,
                self.kerb_ticket,
                self.extra_conf,
            ),
        )

    def _isfilestore(self):
        return True

    def isdir(self, path):
        return super().isdir(path)

    def isfile(self, path):
        return super().isfile(path)

    def delete(self, path, recursive=False):
        return super().delete(path, recursive)

    def mkdir(self, path, **kwargs):
        return super().mkdir(path)

    def rename(self, path, new_path):
        return super().rename(path, new_path)

    def exists(self, path):
        return super().exists(path)

    def ls(self, path, detail=False):
        return super().ls(path, detail)

    def walk(self, top_path):
        contents = self.ls(top_path, detail=True)

        directories, files = _libhdfs_walk_files_dirs(top_path, contents)
        yield top_path, directories, files
        for dirname in directories:
            yield from self.walk(self._path_join(top_path, dirname))

    def upload(self, local_file, hdfs_file):
        with open(local_file, "rb") as rf:
            super().upload(path=hdfs_file, stream=rf)

    def download(self, hdfs_file, local_file):
        with open(local_file, "wb") as wf:
            super().download(hdfs_file, wf)


def _maybe_set_hadoop_classpath():
    import re

    if re.search(r"hadoop-common[^/]+.jar", os.environ.get("CLASSPATH", "")):
        return

    if "HADOOP_HOME" in os.environ:
        if sys.platform != "win32":
            classpath = _derive_hadoop_classpath()
        else:
            hadoop_bin = "{}/bin/hadoop".format(os.environ["HADOOP_HOME"])
            classpath = _hadoop_classpath_glob(hadoop_bin)
    else:
        classpath = _hadoop_classpath_glob("hadoop")

    os.environ["CLASSPATH"] = classpath.decode("utf-8")


def _derive_hadoop_classpath():
    import subprocess

    find_args = ("find", "-L", os.environ["HADOOP_HOME"], "-name", "*.jar")
    find = subprocess.Popen(find_args, stdout=subprocess.PIPE)
    xargs_echo = subprocess.Popen(
        ("xargs", "echo"), stdin=find.stdout, stdout=subprocess.PIPE
    )
    jars = subprocess.check_output(
        ("tr", "' '", "':'"), stdin=xargs_echo.stdout
    )
    hadoop_conf = (
        os.environ["HADOOP_CONF_DIR"]
        if "HADOOP_CONF_DIR" in os.environ
        else os.environ["HADOOP_HOME"] + "/conf"
    )
    return (hadoop_conf + ":").encode("utf-8") + jars


def _hadoop_classpath_glob(hadoop_bin):
    import subprocess

    hadoop_classpath_args = (hadoop_bin, "classpath", "--glob")
    return subprocess.check_output(hadoop_classpath_args)


def _libhdfs_walk_files_dirs(top_path, contents):
    files = []
    directories = []
    for c in contents:
        scrubbed_name = posixpath.split(c["name"])[1]
        if c["kind"] == "file":
            files.append(scrubbed_name)
        else:
            directories.append(scrubbed_name)

    return directories, files


def connect(
    host="default", port=0, user=None, kerb_ticket=None, extra_conf=None
):
    fs = HadoopFileSystem(
        host=host,
        port=port,
        user=user,
        kerb_ticket=kerb_ticket,
        extra_conf=extra_conf,
    )
    return fs
