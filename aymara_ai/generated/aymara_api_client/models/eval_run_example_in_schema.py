from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.eval_run_example_in_schema_type import EvalRunExampleInSchemaType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvalRunExampleInSchema")


@_attrs_define
class EvalRunExampleInSchema:
    """Schema for examples to include with an eval run.

    Attributes:
        type (EvalRunExampleInSchemaType):
        prompt (str):
        response (str):
        explanation (Union[None, Unset, str]):
    """

    type: EvalRunExampleInSchemaType
    prompt: str
    response: str
    explanation: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        prompt = self.prompt

        response = self.response

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "prompt": prompt,
                "response": response,
            }
        )
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = EvalRunExampleInSchemaType(d.pop("type"))

        prompt = d.pop("prompt")

        response = d.pop("response")

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        eval_run_example_in_schema = cls(
            type=type,
            prompt=prompt,
            response=response,
            explanation=explanation,
        )

        eval_run_example_in_schema.additional_properties = d
        return eval_run_example_in_schema

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
