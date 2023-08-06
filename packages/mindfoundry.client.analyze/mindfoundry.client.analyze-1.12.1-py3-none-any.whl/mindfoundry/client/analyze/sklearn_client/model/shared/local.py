import abc
from typing import Optional

from ....swagger.models import ModelResponse
from ....utils.typing import PathLike
from ...data_set import DataLike
from ...prediction import Prediction
from ...test import Test
from .base import BaseModel


class LocalModel(BaseModel, abc.ABC):
    """
    A model that has not yet been saved to Analyze (and thus hasn't been fitted)
    """

    def is_fitting(self) -> bool:
        return False

    def is_fitted(self) -> bool:
        return False

    def has_failed_fitting(self) -> bool:
        return False

    #######################
    # Remote only methods #
    #######################

    @property
    def model_id(self) -> int:
        raise Exception("Must call .fit before the model has an ID")

    def save(self, path: PathLike) -> None:
        # Don't try and save models that are not currently on Analyze
        raise Exception("Must call .fit before a model can be saved")

    def predict(
        self,
        data: DataLike,
        *,
        name: str,
        description: Optional[str],
        wait_until_complete: bool,
    ) -> Prediction:
        raise Exception("Must call .fit before a prediction can occur")

    def test(
        self,
        data: DataLike,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> Test:
        raise Exception("Must call .fit before a test can occur")

    def model_info(self) -> ModelResponse:
        raise Exception("Must call .fit before obtaining model information")

    def url(self) -> str:
        raise Exception("Must call .fit before obtaining model url")

    def wait_until_fitted(self):
        raise Exception("Must call .fit before waiting for the model to be fitted")
