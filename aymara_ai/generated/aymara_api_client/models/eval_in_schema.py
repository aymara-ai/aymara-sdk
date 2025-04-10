from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_type import ContentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_example_in_schema import PromptExampleInSchema


T = TypeVar("T", bound="EvalInSchema")


@_attrs_define
class EvalInSchema:
    """Schema for configuring an Eval based on a eval_type.

    Attributes:
        name (str):
        ai_description (str):
        eval_type (str):
        ai_instructions (Union[None, Unset, str]):
        eval_instructions (Union[None, Unset, str]):
        language (Union[Unset, str]):  Default: 'en'.
        modality (Union[Unset, ContentType]): Content type for AI interactions. Default: ContentType.TEXT.
        num_prompts (Union[Unset, int]):  Default: 50.
        prompt_examples (Union[List['PromptExampleInSchema'], None, Unset]):
        is_jailbreak (Union[Unset, bool]):  Default: False.
        is_sandbox (Union[Unset, bool]):  Default: False.
        workspace_uuid (Union[None, Unset, str]):
    """

    name: str
    ai_description: str
    eval_type: str
    ai_instructions: Union[None, Unset, str] = UNSET
    eval_instructions: Union[None, Unset, str] = UNSET
    language: Union[Unset, str] = "en"
    modality: Union[Unset, ContentType] = ContentType.TEXT
    num_prompts: Union[Unset, int] = 50
    prompt_examples: Union[List["PromptExampleInSchema"], None, Unset] = UNSET
    is_jailbreak: Union[Unset, bool] = False
    is_sandbox: Union[Unset, bool] = False
    workspace_uuid: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        ai_description = self.ai_description

        eval_type = self.eval_type

        ai_instructions: Union[None, Unset, str]
        if isinstance(self.ai_instructions, Unset):
            ai_instructions = UNSET
        else:
            ai_instructions = self.ai_instructions

        eval_instructions: Union[None, Unset, str]
        if isinstance(self.eval_instructions, Unset):
            eval_instructions = UNSET
        else:
            eval_instructions = self.eval_instructions

        language = self.language

        modality: Union[Unset, str] = UNSET
        if not isinstance(self.modality, Unset):
            modality = self.modality.value

        num_prompts = self.num_prompts

        prompt_examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.prompt_examples, Unset):
            prompt_examples = UNSET
        elif isinstance(self.prompt_examples, list):
            prompt_examples = []
            for prompt_examples_type_0_item_data in self.prompt_examples:
                prompt_examples_type_0_item = prompt_examples_type_0_item_data.to_dict()
                prompt_examples.append(prompt_examples_type_0_item)

        else:
            prompt_examples = self.prompt_examples

        is_jailbreak = self.is_jailbreak

        is_sandbox = self.is_sandbox

        workspace_uuid: Union[None, Unset, str]
        if isinstance(self.workspace_uuid, Unset):
            workspace_uuid = UNSET
        else:
            workspace_uuid = self.workspace_uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "ai_description": ai_description,
                "eval_type": eval_type,
            }
        )
        if ai_instructions is not UNSET:
            field_dict["ai_instructions"] = ai_instructions
        if eval_instructions is not UNSET:
            field_dict["eval_instructions"] = eval_instructions
        if language is not UNSET:
            field_dict["language"] = language
        if modality is not UNSET:
            field_dict["modality"] = modality
        if num_prompts is not UNSET:
            field_dict["num_prompts"] = num_prompts
        if prompt_examples is not UNSET:
            field_dict["prompt_examples"] = prompt_examples
        if is_jailbreak is not UNSET:
            field_dict["is_jailbreak"] = is_jailbreak
        if is_sandbox is not UNSET:
            field_dict["is_sandbox"] = is_sandbox
        if workspace_uuid is not UNSET:
            field_dict["workspace_uuid"] = workspace_uuid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.prompt_example_in_schema import PromptExampleInSchema

        d = src_dict.copy()
        name = d.pop("name")

        ai_description = d.pop("ai_description")

        eval_type = d.pop("eval_type")

        def _parse_ai_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ai_instructions = _parse_ai_instructions(d.pop("ai_instructions", UNSET))

        def _parse_eval_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        eval_instructions = _parse_eval_instructions(d.pop("eval_instructions", UNSET))

        language = d.pop("language", UNSET)

        _modality = d.pop("modality", UNSET)
        modality: Union[Unset, ContentType]
        if isinstance(_modality, Unset):
            modality = UNSET
        else:
            modality = ContentType(_modality)

        num_prompts = d.pop("num_prompts", UNSET)

        def _parse_prompt_examples(data: object) -> Union[List["PromptExampleInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompt_examples_type_0 = []
                _prompt_examples_type_0 = data
                for prompt_examples_type_0_item_data in _prompt_examples_type_0:
                    prompt_examples_type_0_item = PromptExampleInSchema.from_dict(prompt_examples_type_0_item_data)

                    prompt_examples_type_0.append(prompt_examples_type_0_item)

                return prompt_examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["PromptExampleInSchema"], None, Unset], data)

        prompt_examples = _parse_prompt_examples(d.pop("prompt_examples", UNSET))

        is_jailbreak = d.pop("is_jailbreak", UNSET)

        is_sandbox = d.pop("is_sandbox", UNSET)

        def _parse_workspace_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workspace_uuid = _parse_workspace_uuid(d.pop("workspace_uuid", UNSET))

        eval_in_schema = cls(
            name=name,
            ai_description=ai_description,
            eval_type=eval_type,
            ai_instructions=ai_instructions,
            eval_instructions=eval_instructions,
            language=language,
            modality=modality,
            num_prompts=num_prompts,
            prompt_examples=prompt_examples,
            is_jailbreak=is_jailbreak,
            is_sandbox=is_sandbox,
            workspace_uuid=workspace_uuid,
        )

        eval_in_schema.additional_properties = d
        return eval_in_schema

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
