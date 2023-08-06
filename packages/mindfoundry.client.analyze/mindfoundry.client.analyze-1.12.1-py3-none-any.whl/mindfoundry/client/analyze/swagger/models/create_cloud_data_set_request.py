from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_cloud_data_set_request_cloud_type import (
    CreateCloudDataSetRequestCloudType,
)
from ..models.create_cloud_data_set_request_data_origin import (
    CreateCloudDataSetRequestDataOrigin,
)
from ..models.parse_options import ParseOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCloudDataSetRequest")

@attr.s(auto_attribs=True)
class CreateCloudDataSetRequest:
    """  """
    name: str
    description: str
    cloud_type: CreateCloudDataSetRequestCloudType
    access_key: str
    secret_key: str
    bucket_name: str
    path: str
    data_origin: CreateCloudDataSetRequestDataOrigin
    parse_options: Union[ParseOptions, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name =  self.name
        description =  self.description
        cloud_type = self.cloud_type.value

        access_key =  self.access_key
        secret_key =  self.secret_key
        bucket_name =  self.bucket_name
        path =  self.path
        data_origin = self.data_origin.value

        parse_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parse_options, Unset):
            parse_options = self.parse_options.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "cloudType": cloud_type,
            "accessKey": access_key,
            "secretKey": secret_key,
            "bucketName": bucket_name,
            "path": path,
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

        cloud_type = CreateCloudDataSetRequestCloudType(d.pop("cloudType"))




        access_key = d.pop("accessKey")

        secret_key = d.pop("secretKey")

        bucket_name = d.pop("bucketName")

        path = d.pop("path")

        data_origin = CreateCloudDataSetRequestDataOrigin(d.pop("dataOrigin"))




        parse_options: Union[ParseOptions, Unset] = UNSET
        _parse_options = d.pop("parseOptions", UNSET)
        if not isinstance(_parse_options,  Unset):
            parse_options = ParseOptions.from_dict(_parse_options)




        create_cloud_data_set_request = cls(
            name=name,
            description=description,
            cloud_type=cloud_type,
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket_name,
            path=path,
            data_origin=data_origin,
            parse_options=parse_options,
        )

        create_cloud_data_set_request.additional_properties = d
        return create_cloud_data_set_request

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
