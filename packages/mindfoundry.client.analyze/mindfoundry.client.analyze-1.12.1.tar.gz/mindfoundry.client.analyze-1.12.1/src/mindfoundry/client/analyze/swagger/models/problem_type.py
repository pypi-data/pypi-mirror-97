from enum import Enum


class ProblemType(str, Enum):
    CLASSIFICATION = "CLASSIFICATION"
    REGRESSION = "REGRESSION"
    CLUSTERING = "CLUSTERING"
    AUTOCLUSTERING = "AUTOCLUSTERING"
    FORECASTING = "FORECASTING"

    def __str__(self) -> str:
        return str(self.value)