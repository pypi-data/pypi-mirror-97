import abc
import logging
import json
from google.protobuf import json_format
from google.protobuf import message
from typing import Text, Optional, Dict, Any

from bmlx.proto.metadata import artifact_pb2
from bmlx.utils.json_utils import Jsonable
from bmlx.utils import import_utils


class Artifact(Jsonable):
    __slots__ = ["type_name", "meta", "name"]

    TYPE_NAME: str = None

    def __init__(
        self,
        type_name: Optional[Text] = None,
        meta: Optional[artifact_pb2.Artifact] = None,
        name: Optional[Text] = "",
    ):
        if self.__class__ != Artifact:
            if type_name:
                raise ValueError(
                    "'type_name' must not passed for Artifact subclass: %s"
                    % self.__class__
                )

            type_name = self.__class__.TYPE_NAME

            if not type_name or not isinstance(type_name, (str, Text)):
                raise ValueError(
                    "Artifact subclass %s should override TYPE_NAME"
                    "class field with str type (got %r instead)",
                    self.__class__,
                    type_name,
                )

        if not type_name:
            raise ValueError(
                "'type_name' field must passed to type for this artifact"
            )

        self.type_name = type_name
        if meta:
            self.meta = meta
        else:
            self.meta = artifact_pb2.Artifact()
            self.meta.type = type_name
            self.meta.state = artifact_pb2.Artifact.State.UNKNOWN
            self.meta.name = name

    def set_artifact(self, artifact: artifact_pb2.Artifact):
        """Set entire artifact in this object."""
        self.meta = artifact

    def __repr__(self):
        return "Artifact (type: %s, id:%s, uri: %s, name: %s)" % (
            self.type_name,
            self.meta.id,
            self.meta.uri,
            self.meta.name,
        )

    def to_json_dict(self) -> Dict[Text, Any]:
        return {
            "meta": json.loads(
                json_format.MessageToJson(
                    message=self.meta, preserving_proto_field_name=True
                )
            ),
            "type_name": self.type_name,
            "__artifact_class_module__": self.__class__.__module__,
            "__artifact_class_name__": self.__class__.__name__,
        }

    @classmethod
    def from_json_dict(cls, dict_data: Dict[Text, Any]) -> Any:
        module_name = dict_data["__artifact_class_module__"]
        class_name = dict_data["__artifact_class_name__"]
        type_name = dict_data["type_name"]
        meta = artifact_pb2.Artifact()
        json_format.Parse(json.dumps(dict_data["meta"]), meta)
        result = None
        try:
            class_path = f"{module_name}.{class_name}"
            artifact_cls = import_utils.import_class_by_path(class_path)
            # If the artifact type is the base Artifact class, do not construct the
            # object here since that constructor requires the mlmd_artifact_type
            # argument.
            if artifact_cls != Artifact:
                result = artifact_cls(meta=meta)
        except (AttributeError, ImportError, ValueError):
            logging.warning(
                (
                    "Could not load artifact class %s.%s; using fallback deserialization "
                    "for the relevant artifact. Please make sure that any artifact "
                    "classes can be imported within your container or environment."
                )
                % (module_name, class_name)
            )
        if not result:
            result = Artifact(type_name=type_name, meta=meta)
        return result
