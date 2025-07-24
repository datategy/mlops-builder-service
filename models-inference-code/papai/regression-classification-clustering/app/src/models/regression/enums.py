from enum import Enum


class BoosterEnum(str, Enum):
    gbtree = "gbtree"
    gblinear = "gblinear"
    dart = "dart"


class KNNAlgorithmEnum(str, Enum):
    auto = "auto"
    ball_tree = "ball_tree"
    kd_tree = "kd_tree"
    brute = "brute"


class KernelEnum(str, Enum):
    linear = "linear"
    poly = "poly"
    rbf = "rbf"
    sigmoid = "sigmoid"
    precomputed = "precomputed"


class ADABoostLossEnum(str, Enum):
    linear = "linear"
    square = "square"
    exponential = "exponential"


class ActivationEnum(str, Enum):
    identity = "identity"
    logistic = "logistic"
    tanh = "tanh"
    relu = "relu"


class MLPSolverEnum(str, Enum):
    lbfgs = "lbfgs"
    sgd = "sgd"
    adam = "adam"


class LearningRateEnum(str, Enum):
    constant = "constant"
    invscaling = "invscaling"
    adaptive = "adaptive"
