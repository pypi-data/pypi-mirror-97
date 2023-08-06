from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.data_prep_step import DataPrepStep
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplyDataPrepStepsRequest")

@attr.s(auto_attribs=True)
class ApplyDataPrepStepsRequest:
    """  """
    saved_steps_id: Union[Unset, float] = UNSET
    steps: Union[Unset, List[DataPrepStep]] = UNSET
    insertion_index: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        saved_steps_id =  self.saved_steps_id
        steps: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()

                steps.append(steps_item)




        insertion_index =  self.insertion_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if saved_steps_id is not UNSET:
            field_dict["savedStepsId"] = saved_steps_id
        if steps is not UNSET:
            field_dict["steps"] = steps
        if insertion_index is not UNSET:
            field_dict["insertionIndex"] = insertion_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        saved_steps_id = d.pop("savedStepsId", UNSET)

        steps = []
        _steps = d.pop("steps", UNSET)
        for steps_item_data in (_steps or []):
            steps_item = DataPrepStep.from_dict(steps_item_data)



            steps.append(steps_item)


        insertion_index = d.pop("insertionIndex", UNSET)

        apply_data_prep_steps_request = cls(
            saved_steps_id=saved_steps_id,
            steps=steps,
            insertion_index=insertion_index,
        )

        apply_data_prep_steps_request.additional_properties = d
        return apply_data_prep_steps_request

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
