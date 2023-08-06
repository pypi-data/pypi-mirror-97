import boto3
import contextlib
import io
import logging
import re
import os
from bmlx.fs.file_system import FileSystem
from bmlx.config import ConfigError, NotFoundError
from typing import Text, Dict
from botocore.response import StreamingBody


class StreamingBodyWrapper(object):
    def __init__(self, sb: StreamingBody):
        self._sb = sb
        self._iter_lines = self._sb.iter_lines

    def __iter__(self):
        return self._iter_lines()

    def readlines(self):
        return [line for line in self._iter_lines()]

    def close(self):
        self._sb.close()


class StreamingBodyBytesWrapper(StreamingBodyWrapper):
    def read(self, amt=None):
        return self._sb.read(amt)


class StreamingBodyTextWrapper(StreamingBodyWrapper):
    def __init__(self, sb: StreamingBody):
        self._sb = sb
        self._iter_lines = self.__iter_lines_str

    def __iter_lines_str(self, chunk_size=1024):
        """
        Hack from StreamingBody.iter_lines(),
        return iterator with type 'str'
        """
        pending = ""
        for chunk in self._sb.iter_chunks(chunk_size):
            chunk = chunk.decode()
            lines = (pending + chunk).splitlines(True)
            for line in lines[:-1]:
                yield line.splitlines()[0]
            pending = lines[-1]
        if pending:
            yield pending.splitlines()[0]

    def read(self, amt=None):
        return self._sb.read(amt).decode()


class CephFileSystem(FileSystem):
    def _resolove_path(self, path):
        if (
            path is None
            or not path.startswith("ceph://")
            or path.count("/") < 3
        ):
            raise RuntimeError("Path %s not match s3 path pattern" % path)
        # ceph://fs-ceph-hk.bigo.sg/bmlx-pipeline/{object-name}
        paths = path.split(self.pathsep)
        return paths[3], self.pathsep.join(paths[4:])

    def __init__(self, endpoint, access_key, secret_key):
        session = boto3.session.Session()
        self.s3_client = session.client(
            service_name="s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def cat(self, path):
        bucket, obj = self._resolove_path(path)
        resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
        return resp["Body"].read()

    def stat(self, path):
        bucket, obj = self._resolove_path(path)
        self.s3_client.head_object(Bucket=bucket, Key=obj)

    def ls(self, path):
        bucket, obj = self._resolove_path(path)
        prefix = path if not obj else path.partition(obj)[0]
        result = []
        marker = ""
        while True:
            s3_elements = self.s3_client.list_objects(
                Bucket=bucket, Prefix=(obj.rstrip("/") + "/"), Marker=marker
            ).get("Contents", [])

            ret = ["%s%s" % (prefix, ele["Key"]) for ele in s3_elements]
            if not ret:
                break
            result.extend(ret)
            marker = s3_elements[-1]["Key"]
        return result

    def is_dir(self, path):
        bucket, obj = self._resolove_path(path)
        s3_elements = self.s3_client.list_objects(
            Bucket=bucket, Prefix=obj
        ).get("Contents", [])
        if s3_elements:
            return True
        return False

    def delete(self, path, recursive=False):
        bucket, obj = self._resolove_path(path)
        if recursive:
            for ele in self.s3_client.list_objects(
                Bucket=bucket, Prefix=(obj.rstrip("/") + "/")
            ).get("Contents", []):
                self.s3_client.delete_object(Bucket=bucket, Key=ele["Key"])
        self.s3_client.delete_object(Bucket=bucket, Key=(obj.rstrip("/")))
        self.s3_client.delete_object(Bucket=bucket, Key=(obj.rstrip("/") + "/"))

    def disk_usage(self, path):
        raise NotImplementedError()

    def _path_join(self, *args):
        return self.pathsep.join(args)

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mkdir(self, path, create_parents=False):
        bucket, obj = self._resolove_path(path)
        prefix = path if not obj else path.partition(obj)[0]
        if create_parents:
            paths = obj.rstrip("/").split("/")
            obj_cur_path = ""
            assert paths[0]
            for i in paths:
                obj_cur_path = "%s%s/" % (obj_cur_path, i)
                if not self.exists("%s%s" % (prefix, obj_cur_path)):
                    self.s3_client.put_object(
                        Bucket=bucket,
                        Key=obj_cur_path,
                        Body=io.BytesIO(),
                        ContentLength=0,
                    )
        elif not self.exists("%s%s" % (prefix, path)):
            self.s3_client.put_object(
                Bucket=bucket, Key=path, Body=io.BytesIO(), ContentLength=0
            )

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    def rename(self, path, new_path):
        self.copy(path, new_path)
        self.rm(path)

    def copy(self, path, new_path):
        bucket, obj = self._resolove_path(new_path)
        self.s3_client.copy_object(Bucket=bucket, CopySource=obj, Key=path)

    def exists(self, path):
        try:
            self.stat(path)
            return True
        except Exception:  # as e:
            # print("stat file get exception %s", e)
            return False

    def _isfilestore(self):
        return False

    @contextlib.contextmanager
    def open(self, path, mode="rb"):
        bucket, obj = self._resolove_path(path)
        if "w" in mode:
            try:
                if "b" in mode:
                    b = bytes()
                    streaming = io.BytesIO(b)
                else:
                    streaming = io.StringIO()
                yield streaming
            finally:
                streaming.seek(0)
                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=obj,
                    Body=streaming.read(),
                    ContentLength=len(streaming.getvalue()),
                )
        elif "r" in mode:
            try:
                resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
                if "b" not in mode:
                    stream_body = StreamingBodyTextWrapper(resp["Body"])
                else:
                    stream_body = StreamingBodyBytesWrapper(resp["Body"])
                yield stream_body
            finally:
                stream_body.close()
        else:
            raise RuntimeError("unknown mode %s" % mode)

    def upload(self, local_path, remote_path):
        bucket, obj = self._resolove_path(remote_path)
        with open(local_path, "rb") as upload_file:
            file_stat = os.stat(local_path)
            self.s3_client.put_object(
                Bucket=bucket,
                Key=obj,
                Body=upload_file,
                ContentLength=file_stat.st_size,
            )

    def download(
        self,
        remote_path,
        local_path,
        config=None,
    ):
        bucket, obj = self._resolove_path(remote_path)
        with open(local_path, "wb") as file_object:
            self.s3_client.download_fileobj(
                Bucket=bucket,
                Key=obj,
                Fileobj=file_object,
                Config=config,
            )

    @property
    def pathsep(self):
        return "/"
