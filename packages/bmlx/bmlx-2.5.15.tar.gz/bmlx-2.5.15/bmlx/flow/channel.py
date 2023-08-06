from typing import Optional, Iterable, Type, Text
from bmlx.flow import Artifact


class Channel(object):
    __slots__ = ["type_name", "_artifacts", "optional"]

    def __init__(
        self,
        artifact_type: Optional[Type[Artifact]] = None,
        type_name: Optional[Text] = None,
        artifacts: Optional[Iterable[Artifact]] = None,
        optional: Optional[bool] = False,
    ):
        if bool(artifact_type) == bool(type_name):
            raise RuntimeError("you should set type_name or artifact_type")
        if artifact_type:
            self.type_name = artifact_type.TYPE_NAME
        else:
            self.type_name = type_name
        self.optional = optional
        self._artifacts: Optional[Iterable[Artifact]] = artifacts or []
        self._validate()

    def __repr__(self):
        artifacts_str = "\n\t".join([repr(a) for a in self._artifacts])

        return "Channel(\n\toptional:%s\n\ttype: %s\n\tartifacts: [{%s}]\n)" % (
            self.optional,
            self.type_name,
            artifacts_str,
        )

    def _validate(self):
        for a in self._artifacts:
            if a.type_name != self.type_name:
                raise TypeError(
                    "artifact type %s not match Channel Type %s"
                    % (a.type_name, self.type_name)
                )

    def get(self) -> Optional[Iterable[Artifact]]:
        return self._artifacts
