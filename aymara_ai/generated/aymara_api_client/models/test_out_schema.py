import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.test_status import TestStatus
from ..models.test_type import TestType

T = TypeVar("T", bound="TestOutSchema")


@_attrs_define
class TestOutSchema:
    """
    Attributes:
        test_uuid (str):
        test_name (str):
        test_status (TestStatus): Test status.
        test_type (TestType): Test type.
        organization_name (str):
        num_test_questions (Union[None, int]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        test_system_prompt (Union[None, str]):
        test_policy (Union[None, str]):
    """

    test_uuid: str
    test_name: str
    test_status: TestStatus
    test_type: TestType
    organization_name: str
    num_test_questions: Union[None, int]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    test_system_prompt: Union[None, str]
    test_policy: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_uuid = self.test_uuid

        test_name = self.test_name

        test_status = self.test_status.value

        test_type = self.test_type.value

        organization_name = self.organization_name

        num_test_questions: Union[None, int]
        num_test_questions = self.num_test_questions

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        test_system_prompt: Union[None, str]
        test_system_prompt = self.test_system_prompt

        test_policy: Union[None, str]
        test_policy = self.test_policy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_uuid": test_uuid,
                "test_name": test_name,
                "test_status": test_status,
                "test_type": test_type,
                "organization_name": organization_name,
                "num_test_questions": num_test_questions,
                "created_at": created_at,
                "updated_at": updated_at,
                "test_system_prompt": test_system_prompt,
                "test_policy": test_policy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_uuid = d.pop("test_uuid")

        test_name = d.pop("test_name")

        test_status = TestStatus(d.pop("test_status"))

        test_type = TestType(d.pop("test_type"))

        organization_name = d.pop("organization_name")

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

        test_out_schema = cls(
            test_uuid=test_uuid,
            test_name=test_name,
            test_status=test_status,
            test_type=test_type,
            organization_name=organization_name,
            num_test_questions=num_test_questions,
            created_at=created_at,
            updated_at=updated_at,
            test_system_prompt=test_system_prompt,
            test_policy=test_policy,
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
