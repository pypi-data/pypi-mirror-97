import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.create_auto_clustering_request import CreateAutoClusteringRequest
from ..models.create_classification_request import CreateClassificationRequest
from ..models.create_clustering_request import CreateClusteringRequest
from ..models.create_forecasting_request import CreateForecastingRequest
from ..models.create_multi_forecasting_request import CreateMultiForecastingRequest
from ..models.create_regression_request import CreateRegressionRequest
from ..models.model_health import ModelHealth
from ..models.model_influence import ModelInfluence
from ..models.model_score import ModelScore
from ..models.model_status import ModelStatus
from ..models.problem_type import ProblemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelResponse")

@attr.s(auto_attribs=True)
class ModelResponse:
    """  """
    id: int
    project_id: int
    name: str
    created_at: datetime.datetime
    created_by: str
    status: ModelStatus
    problem_type: ProblemType
    progress_percent: Optional[float]
    description: Union[Unset, Optional[str]] = UNSET
    failure_details: Union[Unset, Optional[str]] = UNSET
    model_type: Union[Unset, str] = UNSET
    health: Union[Unset, ModelHealth] = UNSET
    score: Union[Optional[ModelScore], Unset] = UNSET
    influences: Union[Unset, List[ModelInfluence]] = UNSET
    create_config: Union[Unset, CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest] = UNSET
    create_endpoint: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id =  self.id
        project_id =  self.project_id
        name =  self.name
        created_at = self.created_at.isoformat()

        created_by =  self.created_by
        status = self.status.value

        problem_type = self.problem_type.value

        description =  self.description
        progress_percent =  self.progress_percent
        failure_details =  self.failure_details
        model_type =  self.model_type
        health: Union[Unset, ModelHealth] = UNSET
        if not isinstance(self.health, Unset):
            health = self.health

        score: Union[None, Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.score, Unset):
            score = self.score.to_dict() if self.score else None

        influences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.influences, Unset):
            influences = []
            for influences_item_data in self.influences:
                influences_item = influences_item_data.to_dict()

                influences.append(influences_item)




        create_config: Union[Unset, CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest]
        if isinstance(self.create_config, Unset):
            create_config = UNSET
        elif isinstance(self.create_config, CreateAutoClusteringRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateClassificationRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateClusteringRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateForecastingRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        elif isinstance(self.create_config, CreateMultiForecastingRequest):
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()

        else:
            create_config = UNSET
            if not isinstance(self.create_config, Unset):
                create_config = self.create_config.to_dict()



        create_endpoint =  self.create_endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "projectId": project_id,
            "name": name,
            "createdAt": created_at,
            "createdBy": created_by,
            "status": status,
            "problemType": problem_type,
            "progressPercent": progress_percent,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if failure_details is not UNSET:
            field_dict["failureDetails"] = failure_details
        if model_type is not UNSET:
            field_dict["modelType"] = model_type
        if health is not UNSET:
            field_dict["health"] = health
        if score is not UNSET:
            field_dict["score"] = score
        if influences is not UNSET:
            field_dict["influences"] = influences
        if create_config is not UNSET:
            field_dict["createConfig"] = create_config
        if create_endpoint is not UNSET:
            field_dict["createEndpoint"] = create_endpoint

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        project_id = d.pop("projectId")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))




        created_by = d.pop("createdBy")

        status = ModelStatus(d.pop("status"))




        problem_type = ProblemType(d.pop("problemType"))




        description = d.pop("description", UNSET)

        progress_percent = d.pop("progressPercent")

        failure_details = d.pop("failureDetails", UNSET)

        model_type = d.pop("modelType", UNSET)

        health: Union[Unset, ModelHealth] = UNSET
        _health = d.pop("health", UNSET)
        if not isinstance(_health,  Unset):
            health = ModelHealth(_health)




        score = None
        _score = d.pop("score", UNSET)
        if _score is not None and not isinstance(_score,  Unset):
            score = ModelScore.from_dict(_score)




        influences = []
        _influences = d.pop("influences", UNSET)
        for influences_item_data in (_influences or []):
            influences_item = ModelInfluence.from_dict(influences_item_data)



            influences.append(influences_item)


        def _parse_create_config(data: Any) -> Union[Unset, CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest]:
            data = None if isinstance(data, Unset) else data
            create_config: Union[Unset, CreateAutoClusteringRequest, CreateClassificationRequest, CreateClusteringRequest, CreateForecastingRequest, CreateMultiForecastingRequest, CreateRegressionRequest]
            try:
                create_config = UNSET
                _create_config = data
                if not isinstance(_create_config,  Unset):
                    create_config = CreateAutoClusteringRequest.from_dict(_create_config)



                return create_config
            except: # noqa: E722
                pass
            try:
                create_config = UNSET
                _create_config = data
                if not isinstance(_create_config,  Unset):
                    create_config = CreateClassificationRequest.from_dict(_create_config)



                return create_config
            except: # noqa: E722
                pass
            try:
                create_config = UNSET
                _create_config = data
                if not isinstance(_create_config,  Unset):
                    create_config = CreateClusteringRequest.from_dict(_create_config)



                return create_config
            except: # noqa: E722
                pass
            try:
                create_config = UNSET
                _create_config = data
                if not isinstance(_create_config,  Unset):
                    create_config = CreateForecastingRequest.from_dict(_create_config)



                return create_config
            except: # noqa: E722
                pass
            try:
                create_config = UNSET
                _create_config = data
                if not isinstance(_create_config,  Unset):
                    create_config = CreateMultiForecastingRequest.from_dict(_create_config)



                return create_config
            except: # noqa: E722
                pass
            create_config = UNSET
            _create_config = data
            if not isinstance(_create_config,  Unset):
                create_config = CreateRegressionRequest.from_dict(_create_config)



            return create_config

        create_config = _parse_create_config(d.pop("createConfig", UNSET))


        create_endpoint = d.pop("createEndpoint", UNSET)

        model_response = cls(
            id=id,
            project_id=project_id,
            name=name,
            created_at=created_at,
            created_by=created_by,
            status=status,
            problem_type=problem_type,
            description=description,
            progress_percent=progress_percent,
            failure_details=failure_details,
            model_type=model_type,
            health=health,
            score=score,
            influences=influences,
            create_config=create_config,
            create_endpoint=create_endpoint,
        )

        model_response.additional_properties = d
        return model_response

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
