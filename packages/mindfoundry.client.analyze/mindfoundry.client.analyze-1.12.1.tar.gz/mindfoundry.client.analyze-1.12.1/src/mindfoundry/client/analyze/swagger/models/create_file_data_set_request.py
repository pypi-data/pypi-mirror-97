from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="CreateFileDataSetRequest")

@attr.s(auto_attribs=True)
class CreateFileDataSetRequest:
    """  """
    name: str
    data: File
    description: Union[Unset, str] = UNSET
    parse_options: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name =  self.name
        data = self.data.to_tuple()

        description =  self.description
        parse_options =  self.parse_options

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "data": data,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if parse_options is not UNSET:
            field_dict["parseOptions"] = parse_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data = File(
             payload = BytesIO(d.pop("data"))
        )




        description = d.pop("description", UNSET)

        parse_options = d.pop("parseOptions", UNSET)

        create_file_data_set_request = cls(
            name=name,
            data=data,
            description=description,
            parse_options=parse_options,
        )

        create_file_data_set_request.additional_properties = d
        return create_file_data_set_request

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
