from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_in_schema_eval_config import EvalInSchemaEvalConfig


T = TypeVar("T", bound="EvalInSchema")


@_attrs_define
class EvalInSchema:
    """Schema for configuring a eval based on a template.

    Attributes:
        eval_name (str):
        eval_template_key (str):
        eval_config (EvalInSchemaEvalConfig):
        num_prompts (Union[Unset, int]):  Default: 15.
        modalities (Union[Unset, List[str]]):
    """

    eval_name: str
    eval_template_key: str
    eval_config: "EvalInSchemaEvalConfig"
    num_prompts: Union[Unset, int] = 15
    modalities: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eval_name = self.eval_name

        eval_template_key = self.eval_template_key

        eval_config = self.eval_config.to_dict()

        num_prompts = self.num_prompts

        modalities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.modalities, Unset):
            modalities = self.modalities

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eval_name": eval_name,
                "eval_template_key": eval_template_key,
                "eval_config": eval_config,
            }
        )
        if num_prompts is not UNSET:
            field_dict["num_prompts"] = num_prompts
        if modalities is not UNSET:
            field_dict["modalities"] = modalities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_in_schema_eval_config import EvalInSchemaEvalConfig

        d = src_dict.copy()
        eval_name = d.pop("eval_name")

        eval_template_key = d.pop("eval_template_key")

        eval_config = EvalInSchemaEvalConfig.from_dict(d.pop("eval_config"))

        num_prompts = d.pop("num_prompts", UNSET)

        modalities = cast(List[str], d.pop("modalities", UNSET))

        eval_in_schema = cls(
            eval_name=eval_name,
            eval_template_key=eval_template_key,
            eval_config=eval_config,
            num_prompts=num_prompts,
            modalities=modalities,
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
