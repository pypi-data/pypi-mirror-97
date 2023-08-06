from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_http_data_set_request_data_origin import (
    CreateHttpDataSetRequestDataOrigin,
)
from ..models.parse_options import ParseOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateHttpDataSetRequest")

@attr.s(auto_attribs=True)
class CreateHttpDataSetRequest:
    """  """
    name: str
    description: str
    url: str
    data_origin: CreateHttpDataSetRequestDataOrigin
    parse_options: Union[ParseOptions, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name =  self.name
        description =  self.description
        url =  self.url
        data_origin = self.data_origin.value

        parse_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parse_options, Unset):
            parse_options = self.parse_options.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "url": url,
            "dataOrigin": data_origin,
        })
        if parse_options is not UNSET:
            field_dict["parseOptions"] = parse_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        url = d.pop("url")

        data_origin = CreateHttpDataSetRequestDataOrigin(d.pop("dataOrigin"))




        parse_options: Union[ParseOptions, Unset] = UNSET
        _parse_options = d.pop("parseOptions", UNSET)
        if not isinstance(_parse_options,  Unset):
            parse_options = ParseOptions.from_dict(_parse_options)




        create_http_data_set_request = cls(
            name=name,
            description=description,
            url=url,
            data_origin=data_origin,
            parse_options=parse_options,
        )

        create_http_data_set_request.additional_properties = d
        return create_http_data_set_request

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
