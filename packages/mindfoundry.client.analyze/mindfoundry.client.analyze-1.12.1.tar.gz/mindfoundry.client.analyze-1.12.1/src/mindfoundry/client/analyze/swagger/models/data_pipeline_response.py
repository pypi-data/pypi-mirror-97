import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.data_prep_step import DataPrepStep

T = TypeVar("T", bound="DataPipelineResponse")

@attr.s(auto_attribs=True)
class DataPipelineResponse:
    """  """
    id: int
    project_id: int
    name: str
    created_at: datetime.datetime
    created_by: str
    steps: List[DataPrepStep]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id =  self.id
        project_id =  self.project_id
        name =  self.name
        created_at = self.created_at.isoformat()

        created_by =  self.created_by
        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()

            steps.append(steps_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "createdAt": created_at,
            "createdBy": created_by,
            "steps": steps,
        })

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in (_steps):
            steps_item = DataPrepStep.from_dict(steps_item_data)



            steps.append(steps_item)


        data_pipeline_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            created_at=created_at,
            created_by=created_by,
            steps=steps,
        )

        data_pipeline_response.additional_properties = d
        return data_pipeline_response

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
