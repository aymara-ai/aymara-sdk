import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_status import TestStatus
from ..models.test_type import TestType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.example_out_schema import ExampleOutSchema


T = TypeVar("T", bound="TestOutSchema")


@_attrs_define
class TestOutSchema:
    """
    Attributes:
        test_uuid (str):
        test_name (str):
        test_status (TestStatus): Test status.
        test_type (TestType): Test type.
        num_test_questions (Union[None, int]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        test_system_prompt (Union[None, str]):
        test_policy (Union[None, str]):
        organization_name (Union[None, Unset, str]):
        additional_instructions (Union[None, Unset, str]):
        examples (Union[List['ExampleOutSchema'], None, Unset]):
    """

    test_uuid: str
    test_name: str
    test_status: TestStatus
    test_type: TestType
    num_test_questions: Union[None, int]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    test_system_prompt: Union[None, str]
    test_policy: Union[None, str]
    organization_name: Union[None, Unset, str] = UNSET
    additional_instructions: Union[None, Unset, str] = UNSET
    examples: Union[List["ExampleOutSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        test_name = self.test_name

        test_status = self.test_status.value

        test_type = self.test_type.value

        num_test_questions: Union[None, int]
        num_test_questions = self.num_test_questions

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        test_system_prompt: Union[None, str]
        test_system_prompt = self.test_system_prompt

        test_policy: Union[None, str]
        test_policy = self.test_policy

        organization_name: Union[None, Unset, str]
        if isinstance(self.organization_name, Unset):
            organization_name = UNSET
        else:
            organization_name = self.organization_name

        additional_instructions: Union[None, Unset, str]
        if isinstance(self.additional_instructions, Unset):
            additional_instructions = UNSET
        else:
            additional_instructions = self.additional_instructions

        examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.examples, Unset):
            examples = UNSET
        elif isinstance(self.examples, list):
            examples = []
            for examples_type_0_item_data in self.examples:
                examples_type_0_item = examples_type_0_item_data.to_dict()
                examples.append(examples_type_0_item)

        else:
            examples = self.examples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "test_name": test_name,
                "test_status": test_status,
                "test_type": test_type,
                "num_test_questions": num_test_questions,
                "created_at": created_at,
                "updated_at": updated_at,
                "test_system_prompt": test_system_prompt,
                "test_policy": test_policy,
            }
        )
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if additional_instructions is not UNSET:
            field_dict["additional_instructions"] = additional_instructions
        if examples is not UNSET:
            field_dict["examples"] = examples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.example_out_schema import ExampleOutSchema

        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        test_name = d.pop("test_name")

        test_status = TestStatus(d.pop("test_status"))

        test_type = TestType(d.pop("test_type"))

        def _parse_num_test_questions(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        num_test_questions = _parse_num_test_questions(d.pop("num_test_questions"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_test_system_prompt(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        test_system_prompt = _parse_test_system_prompt(d.pop("test_system_prompt"))

        def _parse_test_policy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        test_policy = _parse_test_policy(d.pop("test_policy"))

        def _parse_organization_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        organization_name = _parse_organization_name(d.pop("organization_name", UNSET))

        def _parse_additional_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        additional_instructions = _parse_additional_instructions(d.pop("additional_instructions", UNSET))

        def _parse_examples(data: object) -> Union[List["ExampleOutSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                examples_type_0 = []
                _examples_type_0 = data
                for examples_type_0_item_data in _examples_type_0:
                    examples_type_0_item = ExampleOutSchema.from_dict(examples_type_0_item_data)

                    examples_type_0.append(examples_type_0_item)

                return examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ExampleOutSchema"], None, Unset], data)

        examples = _parse_examples(d.pop("examples", UNSET))

        test_out_schema = cls(
            test_uuid=test_uuid,
            test_name=test_name,
            test_status=test_status,
            test_type=test_type,
            num_test_questions=num_test_questions,
            created_at=created_at,
            updated_at=updated_at,
            test_system_prompt=test_system_prompt,
            test_policy=test_policy,
            organization_name=organization_name,
            additional_instructions=additional_instructions,
            examples=examples,
        )

        test_out_schema.additional_properties = d
        return test_out_schema

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
