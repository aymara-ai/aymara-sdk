from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_question_schema_metadata_type_0 import EvalQuestionSchemaMetadataType0


T = TypeVar("T", bound="EvalQuestionSchema")


@_attrs_define
class EvalQuestionSchema:
    """Schema for eval questions in the v2 API.

    Attributes:
        question_uuid (str):
        content (str):
        content_type (str):
        category (str):
        thread_uuid (Union[None, Unset, str]):
        turn_number (Union[Unset, int]):  Default: 1.
        metadata (Union['EvalQuestionSchemaMetadataType0', None, Unset]):
    """

    question_uuid: str
    content: str
    content_type: str
    category: str
    thread_uuid: Union[None, Unset, str] = UNSET
    turn_number: Union[Unset, int] = 1
    metadata: Union["EvalQuestionSchemaMetadataType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.eval_question_schema_metadata_type_0 import EvalQuestionSchemaMetadataType0

        question_uuid = self.question_uuid

        content = self.content

        content_type = self.content_type

        category = self.category

        thread_uuid: Union[None, Unset, str]
        if isinstance(self.thread_uuid, Unset):
            thread_uuid = UNSET
        else:
            thread_uuid = self.thread_uuid

        turn_number = self.turn_number

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, EvalQuestionSchemaMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "content": content,
                "content_type": content_type,
                "category": category,
            }
        )
        if thread_uuid is not UNSET:
            field_dict["thread_uuid"] = thread_uuid
        if turn_number is not UNSET:
            field_dict["turn_number"] = turn_number
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_question_schema_metadata_type_0 import EvalQuestionSchemaMetadataType0

        d = src_dict.copy()
        question_uuid = d.pop("question_uuid")

        content = d.pop("content")

        content_type = d.pop("content_type")

        category = d.pop("category")

        def _parse_thread_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_uuid = _parse_thread_uuid(d.pop("thread_uuid", UNSET))

        turn_number = d.pop("turn_number", UNSET)

        def _parse_metadata(data: object) -> Union["EvalQuestionSchemaMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = EvalQuestionSchemaMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EvalQuestionSchemaMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        eval_question_schema = cls(
            question_uuid=question_uuid,
            content=content,
            content_type=content_type,
            category=category,
            thread_uuid=thread_uuid,
            turn_number=turn_number,
            metadata=metadata,
        )

        eval_question_schema.additional_properties = d
        return eval_question_schema

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
