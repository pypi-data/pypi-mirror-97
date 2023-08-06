from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeployedModelApiResponse")

@attr.s(auto_attribs=True)
class DeployedModelApiResponse:
    """  """
    id: int
    project_id: int
    name: str
    api_endpoint: str
    documentation_endpoint: str
    description: Union[Unset, Optional[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id =  self.id
        project_id =  self.project_id
        name =  self.name
        api_endpoint =  self.api_endpoint
        documentation_endpoint =  self.documentation_endpoint
        description =  self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "apiEndpoint": api_endpoint,
            "documentationEndpoint": documentation_endpoint,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        api_endpoint = d.pop("apiEndpoint")

        documentation_endpoint = d.pop("documentationEndpoint")

        description = d.pop("description", UNSET)

        deployed_model_api_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            api_endpoint=api_endpoint,
            documentation_endpoint=documentation_endpoint,
            description=description,
        )

        deployed_model_api_response.additional_properties = d
        return deployed_model_api_response

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
