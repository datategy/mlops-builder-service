from enum import StrEnum, auto


class UseCase(StrEnum):
    REGRESSION = auto()
    MULTIOUTPUT_REGRESSION = auto()
    BINARY_CLASSIFICATION = auto()
    MULTI_CLASSIFICATION = auto()
    IMAGE_CLASSIFICATION = auto()
    TIMESERIES_FORECASTING = auto()
    CLUSTERING = auto()
