from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.nlp_language import NlpLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateClusteringRequest")

@attr.s(auto_attribs=True)
class CreateClusteringRequest:
    """  """
    name: str
    data_set_id: int
    number_of_clusters: int
    description: Union[Unset, str] = UNSET
    excluded_columns: Union[Unset, List[str]] = UNSET
    nlp_language: Union[Unset, NlpLanguage] = NlpLanguage.AUTO_DETECT
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name =  self.name
        data_set_id =  self.data_set_id
        number_of_clusters =  self.number_of_clusters
        description =  self.description
        excluded_columns: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.excluded_columns, Unset):
            excluded_columns = self.excluded_columns




        nlp_language: Union[Unset, NlpLanguage] = UNSET
        if not isinstance(self.nlp_language, Unset):
            nlp_language = self.nlp_language


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "dataSetId": data_set_id,
            "numberOfClusters": number_of_clusters,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if excluded_columns is not UNSET:
            field_dict["excludedColumns"] = excluded_columns
        if nlp_language is not UNSET:
            field_dict["nlpLanguage"] = nlp_language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data_set_id = d.pop("dataSetId")

        number_of_clusters = d.pop("numberOfClusters")

        description = d.pop("description", UNSET)

        excluded_columns = cast(List[str], d.pop("excludedColumns", UNSET))


        nlp_language: Union[Unset, NlpLanguage] = UNSET
        _nlp_language = d.pop("nlpLanguage", UNSET)
        if not isinstance(_nlp_language,  Unset):
            nlp_language = NlpLanguage(_nlp_language)




        create_clustering_request = cls(
            name=name,
            data_set_id=data_set_id,
            number_of_clusters=number_of_clusters,
            description=description,
            excluded_columns=excluded_columns,
            nlp_language=nlp_language,
        )

        create_clustering_request.additional_properties = d
        return create_clustering_request

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
