from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.data_value import DataValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscriminatorsColumnValuesItem")

@attr.s(auto_attribs=True)
class DiscriminatorsColumnValuesItem:
    """  """
    column_name: Union[Unset, str] = UNSET
    value: Union[DataValue, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        column_name =  self.column_name
        value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if column_name is not UNSET:
            field_dict["columnName"] = column_name
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column_name = d.pop("columnName", UNSET)

        value: Union[DataValue, Unset] = UNSET
        _value = d.pop("value", UNSET)
        if not isinstance(_value,  Unset):
            value = DataValue.from_dict(_value)




        discriminators_column_values_item = cls(
            column_name=column_name,
            value=value,
        )

        discriminators_column_values_item.additional_properties = d
        return discriminators_column_values_item

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
