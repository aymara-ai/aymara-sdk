from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.test_type import TestType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.example_in_schema import ExampleInSchema


T = TypeVar("T", bound="TestInSchema")


@_attrs_define
class TestInSchema:
    """
    Attributes:
        test_name (str):
        student_description (str):
        test_type (Union[Unset, TestType]): Test type. Default: TestType.SAFETY.
        test_language (Union[Unset, str]):  Default: 'en'.
        test_policy (Union[None, Unset, str]):
        num_test_questions (Union[None, Unset, int]):
        test_system_prompt (Union[None, Unset, str]):
        knowledge_base (Union[None, Unset, str]):
        additional_instructions (Union[None, Unset, str]):
        test_examples (Union[List['ExampleInSchema'], None, Unset]):
    """

    test_name: str
    student_description: str
    test_type: Union[Unset, TestType] = TestType.SAFETY
    test_language: Union[Unset, str] = "en"
    test_policy: Union[None, Unset, str] = UNSET
    num_test_questions: Union[None, Unset, int] = UNSET
    test_system_prompt: Union[None, Unset, str] = UNSET
    knowledge_base: Union[None, Unset, str] = UNSET
    additional_instructions: Union[None, Unset, str] = UNSET
    test_examples: Union[List["ExampleInSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_name = self.test_name

        student_description = self.student_description

        test_type: Union[Unset, str] = UNSET
        if not isinstance(self.test_type, Unset):
            test_type = self.test_type.value

        test_language = self.test_language

        test_policy: Union[None, Unset, str]
        if isinstance(self.test_policy, Unset):
            test_policy = UNSET
        else:
            test_policy = self.test_policy

        num_test_questions: Union[None, Unset, int]
        if isinstance(self.num_test_questions, Unset):
            num_test_questions = UNSET
        else:
            num_test_questions = self.num_test_questions

        test_system_prompt: Union[None, Unset, str]
        if isinstance(self.test_system_prompt, Unset):
            test_system_prompt = UNSET
        else:
            test_system_prompt = self.test_system_prompt

        knowledge_base: Union[None, Unset, str]
        if isinstance(self.knowledge_base, Unset):
            knowledge_base = UNSET
        else:
            knowledge_base = self.knowledge_base

        additional_instructions: Union[None, Unset, str]
        if isinstance(self.additional_instructions, Unset):
            additional_instructions = UNSET
        else:
            additional_instructions = self.additional_instructions

        test_examples: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.test_examples, Unset):
            test_examples = UNSET
        elif isinstance(self.test_examples, list):
            test_examples = []
            for test_examples_type_0_item_data in self.test_examples:
                test_examples_type_0_item = test_examples_type_0_item_data.to_dict()
                test_examples.append(test_examples_type_0_item)

        else:
            test_examples = self.test_examples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_name": test_name,
                "student_description": student_description,
            }
        )
        if test_type is not UNSET:
            field_dict["test_type"] = test_type
        if test_language is not UNSET:
            field_dict["test_language"] = test_language
        if test_policy is not UNSET:
            field_dict["test_policy"] = test_policy
        if num_test_questions is not UNSET:
            field_dict["num_test_questions"] = num_test_questions
        if test_system_prompt is not UNSET:
            field_dict["test_system_prompt"] = test_system_prompt
        if knowledge_base is not UNSET:
            field_dict["knowledge_base"] = knowledge_base
        if additional_instructions is not UNSET:
            field_dict["additional_instructions"] = additional_instructions
        if test_examples is not UNSET:
            field_dict["test_examples"] = test_examples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.example_in_schema import ExampleInSchema

        d = src_dict.copy()
        test_name = d.pop("test_name")

        student_description = d.pop("student_description")

        _test_type = d.pop("test_type", UNSET)
        test_type: Union[Unset, TestType]
        if isinstance(_test_type, Unset):
            test_type = UNSET
        else:
            test_type = TestType(_test_type)

        test_language = d.pop("test_language", UNSET)

        def _parse_test_policy(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_policy = _parse_test_policy(d.pop("test_policy", UNSET))

        def _parse_num_test_questions(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_test_questions = _parse_num_test_questions(d.pop("num_test_questions", UNSET))

        def _parse_test_system_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_system_prompt = _parse_test_system_prompt(d.pop("test_system_prompt", UNSET))

        def _parse_knowledge_base(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        knowledge_base = _parse_knowledge_base(d.pop("knowledge_base", UNSET))

        def _parse_additional_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        additional_instructions = _parse_additional_instructions(d.pop("additional_instructions", UNSET))

        def _parse_test_examples(data: object) -> Union[List["ExampleInSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                test_examples_type_0 = []
                _test_examples_type_0 = data
                for test_examples_type_0_item_data in _test_examples_type_0:
                    test_examples_type_0_item = ExampleInSchema.from_dict(test_examples_type_0_item_data)

                    test_examples_type_0.append(test_examples_type_0_item)

                return test_examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ExampleInSchema"], None, Unset], data)

        test_examples = _parse_test_examples(d.pop("test_examples", UNSET))

        test_in_schema = cls(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            num_test_questions=num_test_questions,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=test_examples,
        )

        test_in_schema.additional_properties = d
        return test_in_schema

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
