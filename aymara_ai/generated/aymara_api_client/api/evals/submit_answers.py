from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_schema import ErrorResponseSchema
from ...models.eval_answer_in_schema import EvalAnswerInSchema
from ...models.eval_answer_out_schema import EvalAnswerOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    eval_uuid: str,
    *,
    body: EvalAnswerInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v2/evals/{eval_uuid}/answers",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = EvalAnswerOutSchema.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponseSchema.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorResponseSchema.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = ErrorResponseSchema.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponseSchema.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = ErrorResponseSchema.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorResponseSchema.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = ErrorResponseSchema.from_dict(response.json())

        return response_429
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponseSchema.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = ErrorResponseSchema.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    eval_uuid: str,
    *,
    client: AuthenticatedClient,
    body: EvalAnswerInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    """Submit Answers

     Store an AI response to a test prompt.

    Args:
        test_uuid: UUID of the test
        response_data: Response data including prompt UUID and content
        workspace_uuid: Optional workspace UUID for filtering

    Returns:
        The stored response object

    Args:
        eval_uuid (str):
        workspace_uuid (Union[Unset, str]):
        body (EvalAnswerInSchema): Schema for submitting AI responses to eval questions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, EvalAnswerOutSchema]]
    """

    kwargs = _get_kwargs(
        eval_uuid=eval_uuid,
        body=body,
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    eval_uuid: str,
    *,
    client: AuthenticatedClient,
    body: EvalAnswerInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    """Submit Answers

     Store an AI response to a test prompt.

    Args:
        test_uuid: UUID of the test
        response_data: Response data including prompt UUID and content
        workspace_uuid: Optional workspace UUID for filtering

    Returns:
        The stored response object

    Args:
        eval_uuid (str):
        workspace_uuid (Union[Unset, str]):
        body (EvalAnswerInSchema): Schema for submitting AI responses to eval questions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, EvalAnswerOutSchema]
    """

    return sync_detailed(
        eval_uuid=eval_uuid,
        client=client,
        body=body,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    eval_uuid: str,
    *,
    client: AuthenticatedClient,
    body: EvalAnswerInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    """Submit Answers

     Store an AI response to a test prompt.

    Args:
        test_uuid: UUID of the test
        response_data: Response data including prompt UUID and content
        workspace_uuid: Optional workspace UUID for filtering

    Returns:
        The stored response object

    Args:
        eval_uuid (str):
        workspace_uuid (Union[Unset, str]):
        body (EvalAnswerInSchema): Schema for submitting AI responses to eval questions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, EvalAnswerOutSchema]]
    """

    kwargs = _get_kwargs(
        eval_uuid=eval_uuid,
        body=body,
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    eval_uuid: str,
    *,
    client: AuthenticatedClient,
    body: EvalAnswerInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorResponseSchema, EvalAnswerOutSchema]]:
    """Submit Answers

     Store an AI response to a test prompt.

    Args:
        test_uuid: UUID of the test
        response_data: Response data including prompt UUID and content
        workspace_uuid: Optional workspace UUID for filtering

    Returns:
        The stored response object

    Args:
        eval_uuid (str):
        workspace_uuid (Union[Unset, str]):
        body (EvalAnswerInSchema): Schema for submitting AI responses to eval questions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, EvalAnswerOutSchema]
    """

    return (
        await asyncio_detailed(
            eval_uuid=eval_uuid,
            client=client,
            body=body,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
