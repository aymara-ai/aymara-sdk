import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_out_schema import EvalOutSchema
    from ..models.eval_response_out_schema import EvalResponseOutSchema


T = TypeVar("T", bound="EvalRunTurnOutSchema")


@_attrs_define
class EvalRunTurnOutSchema:
    """Schema for returning eval run turn.

    Attributes:
        eval_run_uuid (str):
        status (Status): Resource status.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        evaluation (Union['EvalOutSchema', None, Unset]):
        ai_description (Union[None, Unset, str]):
        workspace_uuid (Union[None, Unset, str]):
        pass_rate (Union[None, Unset, float]):
        num_prompts (Union[None, Unset, int]):
        num_responses_scored (Union[None, Unset, int]):
        responses (Union[List['EvalResponseOutSchema'], None, Unset]):
    """

    eval_run_uuid: str
    status: Status
    created_at: datetime.datetime
    updated_at: datetime.datetime
    evaluation: Union["EvalOutSchema", None, Unset] = UNSET
    ai_description: Union[None, Unset, str] = UNSET
    workspace_uuid: Union[None, Unset, str] = UNSET
    pass_rate: Union[None, Unset, float] = UNSET
    num_prompts: Union[None, Unset, int] = UNSET
    num_responses_scored: Union[None, Unset, int] = UNSET
    responses: Union[List["EvalResponseOutSchema"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.eval_out_schema import EvalOutSchema

        eval_run_uuid = self.eval_run_uuid

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        evaluation: Union[Dict[str, Any], None, Unset]
        if isinstance(self.evaluation, Unset):
            evaluation = UNSET
        elif isinstance(self.evaluation, EvalOutSchema):
            evaluation = self.evaluation.to_dict()
        else:
            evaluation = self.evaluation

        ai_description: Union[None, Unset, str]
        if isinstance(self.ai_description, Unset):
            ai_description = UNSET
        else:
            ai_description = self.ai_description

        workspace_uuid: Union[None, Unset, str]
        if isinstance(self.workspace_uuid, Unset):
            workspace_uuid = UNSET
        else:
            workspace_uuid = self.workspace_uuid

        pass_rate: Union[None, Unset, float]
        if isinstance(self.pass_rate, Unset):
            pass_rate = UNSET
        else:
            pass_rate = self.pass_rate

        num_prompts: Union[None, Unset, int]
        if isinstance(self.num_prompts, Unset):
            num_prompts = UNSET
        else:
            num_prompts = self.num_prompts

        num_responses_scored: Union[None, Unset, int]
        if isinstance(self.num_responses_scored, Unset):
            num_responses_scored = UNSET
        else:
            num_responses_scored = self.num_responses_scored

        responses: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.responses, Unset):
            responses = UNSET
        elif isinstance(self.responses, list):
            responses = []
            for responses_type_0_item_data in self.responses:
                responses_type_0_item = responses_type_0_item_data.to_dict()
                responses.append(responses_type_0_item)

        else:
            responses = self.responses

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eval_run_uuid": eval_run_uuid,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if evaluation is not UNSET:
            field_dict["evaluation"] = evaluation
        if ai_description is not UNSET:
            field_dict["ai_description"] = ai_description
        if workspace_uuid is not UNSET:
            field_dict["workspace_uuid"] = workspace_uuid
        if pass_rate is not UNSET:
            field_dict["pass_rate"] = pass_rate
        if num_prompts is not UNSET:
            field_dict["num_prompts"] = num_prompts
        if num_responses_scored is not UNSET:
            field_dict["num_responses_scored"] = num_responses_scored
        if responses is not UNSET:
            field_dict["responses"] = responses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.eval_out_schema import EvalOutSchema
        from ..models.eval_response_out_schema import EvalResponseOutSchema

        d = src_dict.copy()
        eval_run_uuid = d.pop("eval_run_uuid")

        status = Status(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_evaluation(data: object) -> Union["EvalOutSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                evaluation_type_0 = EvalOutSchema.from_dict(data)

                return evaluation_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EvalOutSchema", None, Unset], data)

        evaluation = _parse_evaluation(d.pop("evaluation", UNSET))

        def _parse_ai_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ai_description = _parse_ai_description(d.pop("ai_description", UNSET))

        def _parse_workspace_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workspace_uuid = _parse_workspace_uuid(d.pop("workspace_uuid", UNSET))

        def _parse_pass_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pass_rate = _parse_pass_rate(d.pop("pass_rate", UNSET))

        def _parse_num_prompts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_prompts = _parse_num_prompts(d.pop("num_prompts", UNSET))

        def _parse_num_responses_scored(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_responses_scored = _parse_num_responses_scored(d.pop("num_responses_scored", UNSET))

        def _parse_responses(data: object) -> Union[List["EvalResponseOutSchema"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                responses_type_0 = []
                _responses_type_0 = data
                for responses_type_0_item_data in _responses_type_0:
                    responses_type_0_item = EvalResponseOutSchema.from_dict(responses_type_0_item_data)

                    responses_type_0.append(responses_type_0_item)

                return responses_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["EvalResponseOutSchema"], None, Unset], data)

        responses = _parse_responses(d.pop("responses", UNSET))

        eval_run_turn_out_schema = cls(
            eval_run_uuid=eval_run_uuid,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            evaluation=evaluation,
            ai_description=ai_description,
            workspace_uuid=workspace_uuid,
            pass_rate=pass_rate,
            num_prompts=num_prompts,
            num_responses_scored=num_responses_scored,
            responses=responses,
        )

        eval_run_turn_out_schema.additional_properties = d
        return eval_run_turn_out_schema

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
