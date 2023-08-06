import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.data_prep_step_response import DataPrepStepResponse
from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataSetResponse")

@attr.s(auto_attribs=True)
class DataSetResponse:
    """  """
    id: int
    project_id: int
    name: str
    rows: int
    columns: int
    created_at: datetime.datetime
    created_by: str
    data_prep_steps: List[DataPrepStepResponse]
    status: Status
    description: Union[Unset, Optional[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id =  self.id
        project_id =  self.project_id
        name =  self.name
        rows =  self.rows
        columns =  self.columns
        created_at = self.created_at.isoformat()

        created_by =  self.created_by
        data_prep_steps = []
        for data_prep_steps_item_data in self.data_prep_steps:
            data_prep_steps_item = data_prep_steps_item_data.to_dict()

            data_prep_steps.append(data_prep_steps_item)




        status = self.status.value

        description =  self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "rows": rows,
            "columns": columns,
            "createdAt": created_at,
            "createdBy": created_by,
            "dataPrepSteps": data_prep_steps,
            "status": status,
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

        rows = d.pop("rows")

        columns = d.pop("columns")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        data_prep_steps = []
        _data_prep_steps = d.pop("dataPrepSteps")
        for data_prep_steps_item_data in (_data_prep_steps):
            data_prep_steps_item = DataPrepStepResponse.from_dict(data_prep_steps_item_data)



            data_prep_steps.append(data_prep_steps_item)


        status = Status(d.pop("status"))




        description = d.pop("description", UNSET)

        data_set_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            rows=rows,
            columns=columns,
            created_at=created_at,
            created_by=created_by,
            data_prep_steps=data_prep_steps,
            status=status,
            description=description,
        )

        data_set_response.additional_properties = d
        return data_set_response

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
