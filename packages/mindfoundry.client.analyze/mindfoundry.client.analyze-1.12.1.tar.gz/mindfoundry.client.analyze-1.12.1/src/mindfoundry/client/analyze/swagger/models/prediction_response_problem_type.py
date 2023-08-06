from enum import Enum


class PredictionResponseProblemType(str, Enum):
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
    REGRESSION = "regression"
    FORECASTING = "forecasting"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)