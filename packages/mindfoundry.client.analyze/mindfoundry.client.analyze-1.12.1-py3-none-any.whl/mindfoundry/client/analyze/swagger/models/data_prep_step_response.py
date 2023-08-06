from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.data_prep_step import DataPrepStep
from ..models.status import Status

T = TypeVar("T", bound="DataPrepStepResponse")

@attr.s(auto_attribs=True)
class DataPrepStepResponse:
    """  """
    id: int
    status: Status
    warning_count: int
    step: DataPrepStep
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id =  self.id
        status = self.status.value

        warning_count =  self.warning_count
        step = self.step.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "status": status,
            "warningCount": warning_count,
            "step": step,
        })

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        status = Status(d.pop("status"))




        warning_count = d.pop("warningCount")

        step = DataPrepStep.from_dict(d.pop("step"))




        data_prep_step_response = cls(
            id=id,
            status=status,
            warning_count=warning_count,
            step=step,
        )

        data_prep_step_response.additional_properties = d
        return data_prep_step_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
