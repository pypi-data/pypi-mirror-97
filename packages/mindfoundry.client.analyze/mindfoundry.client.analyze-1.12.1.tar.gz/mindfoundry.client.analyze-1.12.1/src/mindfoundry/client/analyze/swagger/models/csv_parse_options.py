from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.csv_parse_options_file_type import CsvParseOptionsFileType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CsvParseOptions")

@attr.s(auto_attribs=True)
class CsvParseOptions:
    """  """
    file_type: CsvParseOptionsFileType
    charset: str = 'UTF-8'
    column_names_in_header: Union[Unset, bool] = False
    separator: Union[Unset, str] = UNSET
    quote_char: Union[Unset, str] = UNSET
    escape_char: Union[Unset, str] = UNSET
    skip_top: Union[Unset, int] = 0
    skip_bottom: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_type = self.file_type.value

        charset =  self.charset
        column_names_in_header =  self.column_names_in_header
        separator =  self.separator
        quote_char =  self.quote_char
        escape_char =  self.escape_char
        skip_top =  self.skip_top
        skip_bottom =  self.skip_bottom

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileType": file_type,
            "charset": charset,
        })
        if column_names_in_header is not UNSET:
            field_dict["columnNamesInHeader"] = column_names_in_header
        if separator is not UNSET:
            field_dict["separator"] = separator
        if quote_char is not UNSET:
            field_dict["quoteChar"] = quote_char
        if escape_char is not UNSET:
            field_dict["escapeChar"] = escape_char
        if skip_top is not UNSET:
            field_dict["skipTop"] = skip_top
        if skip_bottom is not UNSET:
            field_dict["skipBottom"] = skip_bottom

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_type = CsvParseOptionsFileType(d.pop("fileType"))




        charset = d.pop("charset")

        column_names_in_header = d.pop("columnNamesInHeader", UNSET)

        separator = d.pop("separator", UNSET)

        quote_char = d.pop("quoteChar", UNSET)

        escape_char = d.pop("escapeChar", UNSET)

        skip_top = d.pop("skipTop", UNSET)

        skip_bottom = d.pop("skipBottom", UNSET)

        csv_parse_options = cls(
            file_type=file_type,
            charset=charset,
            column_names_in_header=column_names_in_header,
            separator=separator,
            quote_char=quote_char,
            escape_char=escape_char,
            skip_top=skip_top,
            skip_bottom=skip_bottom,
        )

        csv_parse_options.additional_properties = d
        return csv_parse_options

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
