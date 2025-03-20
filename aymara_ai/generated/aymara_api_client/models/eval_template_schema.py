from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_template_schema_validation_schema import EvalTemplateSchemaValidationSchema


T = TypeVar("T", bound="EvalTemplateSchema")


@_attrs_define
class EvalTemplateSchema:
    """Schema for eval templates.

    Attributes:
        template_uuid (str):
        template_name (str):
        template_key (str):
        description (str):
        generation_strategy (str):
        validation_schema (EvalTemplateSchemaValidationSchema):
        active (bool):
        supported_modalities (Union[Unset, List[str]]):
    """

    template_uuid: str
    template_name: str
    template_key: str
    description: str
    generation_strategy: str
    validation_schema: "EvalTemplateSchemaValidationSchema"
    active: bool
    supported_modalities: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        template_uuid = self.template_uuid

        template_name = self.template_name

        template_key = self.template_key

        description = self.description

        generation_strategy = self.generation_strategy

        validation_schema = self.validation_schema.to_dict()

        active = self.active

        supported_modalities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.supported_modalities, Unset):
            supported_modalities = self.supported_modalities

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "template_uuid": template_uuid,
                "template_name": template_name,
                "template_key": template_key,
                "description": description,
                "generation_strategy": generation_strategy,
                "validation_schema": validation_schema,
                "active": active,
            }
        )
        if supported_modalities is not UNSET:
            field_dict["supported_modalities"] = supported_modalities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_template_schema_validation_schema import EvalTemplateSchemaValidationSchema

        d = src_dict.copy()
        template_uuid = d.pop("template_uuid")

        template_name = d.pop("template_name")

        template_key = d.pop("template_key")

        description = d.pop("description")

        generation_strategy = d.pop("generation_strategy")

        validation_schema = EvalTemplateSchemaValidationSchema.from_dict(d.pop("validation_schema"))

        active = d.pop("active")

        supported_modalities = cast(List[str], d.pop("supported_modalities", UNSET))

        eval_template_schema = cls(
            template_uuid=template_uuid,
            template_name=template_name,
            template_key=template_key,
            description=description,
            generation_strategy=generation_strategy,
            validation_schema=validation_schema,
            active=active,
            supported_modalities=supported_modalities,
        )

        eval_template_schema.additional_properties = d
        return eval_template_schema

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
