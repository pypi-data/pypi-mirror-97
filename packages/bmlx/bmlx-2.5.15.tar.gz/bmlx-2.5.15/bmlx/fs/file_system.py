import os
import io
import abc
import six
import pathlib
import contextlib
import urllib
from os.path import join as pjoin

class FileSystem:
    """ general file system wrapper """

    @abc.abstractmethod
    def cat(self, path):
        with self.open(path, "rb") as f:
            return f.read()

    @abc.abstractmethod
    def ls(self, path):
        pass

    @abc.abstractmethod
    def delete(self, path, recursive=False):
        pass

    def disk_usage(self, path):
        path = _stringify_path(path)
        path_info = self.stat(path)
        if path_info["kind"] == "file":
            return path_info["size"]

        total = 0
        for root, directories, files in self.walk(path):
            for child_path in files:
                abspath = self._path_join(root, child_path)
                total += self.stat(abspath)["size"]

        return total

    def _path_join(self, *args):
        return self.pathsep.join(args)

    @abc.abstractmethod
    def stat(self, path):
        pass

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    @abc.abstractmethod
    def rename(self, path, new_path):
        pass

    @abc.abstractmethod
    def mkdir(self, path, create_parents=True):
        pass

    @abc.abstractmethod
    def exists(self, path):
        pass

    @abc.abstractmethod
    def isdir(self, path):
        pass

    @abc.abstractmethod
    def isfile(self, path):
        pass

    @abc.abstractmethod
    def _isfilestore(self):
        pass

    @abc.abstractmethod
    def open(self, path, mode="rb"):
        pass

    @property
    def pathsep(self):
        return "/"


def _stringify_path(path):
    if isinstance(path, six.string_types):
        return path

    try:
        return path.__fspath__()  # new in python 3.6
    except AttributeError:
        if isinstance(path, pathlib.Path):
            return str(path)

    raise TypeError("not a path-like object")


class LocalFileSystem(FileSystem):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LocalFileSystem()
        return cls._instance

    def ls(self, path):
        path = _stringify_path(path)
        return sorted(pjoin(path, x) for x in os.listdir(path))

    def mkdir(self, path, create_parents=True):
        path = _stringify_path(path)
        if create_parents:
            os.makedirs(path)
        else:
            os.mkdir(path)

    def isdir(self, path):
        path = _stringify_path(path)
        return os.path.isdir(path)

    def isfile(self, path):
        path = _stringify_path(path)
        return os.path.isfile(path)

    def _isfilestore(self):
        return True

    def exists(self, path):
        path = _stringify_path(path)
        return os.path.exists(path)

    def open(self, path, mode="rb"):
        path = _stringify_path(path)
        return open(path, mode=mode)

    @property
    def pathsep(self):
        return os.path.sep

    def walk(self, path):
        path = _stringify_path(path)
        return os.walk(path)

def _is_path_like(path):
    # PEP519 filesystem path protocol is available from python 3.6, so pathlib
    # doesn't implement __fspath__ for earlier versions
    return (
        isinstance(path, six.string_types)
        or hasattr(path, "__fspath__")
        or isinstance(path, pathlib.Path)
    )

