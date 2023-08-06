from enum import Enum


class ModelTypes(Enum):
    TREE = "TREE"
    DEEP = "DEEP"
    LINEAR = "LINEAR"


class DeepLearningFramework(Enum):
    TENSORFLOW = "TENSORFLOW"
    PYTORCH = "PYTORCH"
