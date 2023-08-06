"""standard mlflow artifacts"""
from bmlx.flow import Artifact


class Model(Artifact):
    TYPE_NAME = "Model"


class Samples(Artifact):
    TYPE_NAME = "Samples"


class Schema(Artifact):
    TYPE_NAME = "Schema"


class Metrics(Artifact):
    TYPE_NAME = "Metrics"
