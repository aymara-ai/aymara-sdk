from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_response_in_schema import EvalResponseInSchema
    from ..models.eval_run_example_in_schema import EvalRunExampleInSchema


T = TypeVar("T", bound="EvalRunInSchema")


@_attrs_define
class EvalRunInSchema:
    """Schema for creating or continuing an eval run.

    Attributes:
        eval_uuid (str):
        responses (List['EvalResponseInSchema']):
        name (Union[None, Unset, str]):
        eval_run_uuid (Union[None, Unset, str]):
        ai_description (Union[None, Unset, str]):
        generate_prompts (Union[None, Unset, bool]):  Default: False.
        eval_run_examples (Union[List['EvalRunExampleInSchema'], None, Unset]):
    """

    eval_uuid: str
    responses: List["EvalResponseInSchema"]
    name: Union[None, Unset, str] = UNSET
    eval_run_uuid: Union[None, Unset, str] = UNSET
    ai_description: Union[None, Unset, str] = UNSET
    generate_prompts: Union[None, Unset, bool] = False
    eval_run_examples: Union[List["EvalRunExampleInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eval_uuid = self.eval_uuid

        responses = []
        for responses_item_data in self.responses:
            responses_item = responses_item_data.to_dict()
            responses.append(responses_item)

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        eval_run_uuid: Union[None, Unset, str]
        if isinstance(self.eval_run_uuid, Unset):
            eval_run_uuid = UNSET
        else:
            eval_run_uuid = self.eval_run_uuid

        ai_description: Union[None, Unset, str]
        if isinstance(self.ai_description, Unset):
            ai_description = UNSET
        else:
            ai_description = self.ai_description

        generate_prompts: Union[None, Unset, bool]
        if isinstance(self.generate_prompts, Unset):
            generate_prompts = UNSET
        else:
            generate_prompts = self.generate_prompts

        eval_run_examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.eval_run_examples, Unset):
            eval_run_examples = UNSET
        elif isinstance(self.eval_run_examples, list):
            eval_run_examples = []
            for eval_run_examples_type_0_item_data in self.eval_run_examples:
                eval_run_examples_type_0_item = eval_run_examples_type_0_item_data.to_dict()
                eval_run_examples.append(eval_run_examples_type_0_item)

        else:
            eval_run_examples = self.eval_run_examples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eval_uuid": eval_uuid,
                "responses": responses,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if eval_run_uuid is not UNSET:
            field_dict["eval_run_uuid"] = eval_run_uuid
        if ai_description is not UNSET:
            field_dict["ai_description"] = ai_description
        if generate_prompts is not UNSET:
            field_dict["generate_prompts"] = generate_prompts
        if eval_run_examples is not UNSET:
            field_dict["eval_run_examples"] = eval_run_examples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_response_in_schema import EvalResponseInSchema
        from ..models.eval_run_example_in_schema import EvalRunExampleInSchema

        d = src_dict.copy()
        eval_uuid = d.pop("eval_uuid")

        responses = []
        _responses = d.pop("responses")
        for responses_item_data in _responses:
            responses_item = EvalResponseInSchema.from_dict(responses_item_data)

            responses.append(responses_item)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_eval_run_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        eval_run_uuid = _parse_eval_run_uuid(d.pop("eval_run_uuid", UNSET))

        def _parse_ai_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ai_description = _parse_ai_description(d.pop("ai_description", UNSET))

        def _parse_generate_prompts(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        generate_prompts = _parse_generate_prompts(d.pop("generate_prompts", UNSET))

        def _parse_eval_run_examples(data: object) -> Union[List["EvalRunExampleInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                eval_run_examples_type_0 = []
                _eval_run_examples_type_0 = data
                for eval_run_examples_type_0_item_data in _eval_run_examples_type_0:
                    eval_run_examples_type_0_item = EvalRunExampleInSchema.from_dict(eval_run_examples_type_0_item_data)

                    eval_run_examples_type_0.append(eval_run_examples_type_0_item)

                return eval_run_examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["EvalRunExampleInSchema"], None, Unset], data)

        eval_run_examples = _parse_eval_run_examples(d.pop("eval_run_examples", UNSET))

        eval_run_in_schema = cls(
            eval_uuid=eval_uuid,
            responses=responses,
            name=name,
            eval_run_uuid=eval_run_uuid,
            ai_description=ai_description,
            generate_prompts=generate_prompts,
            eval_run_examples=eval_run_examples,
        )

        eval_run_in_schema.additional_properties = d
        return eval_run_in_schema

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
