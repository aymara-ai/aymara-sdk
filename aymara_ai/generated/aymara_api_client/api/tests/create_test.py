from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_schema import ErrorSchema
from ...models.test_in_schema import TestInSchema
from ...models.test_out_schema import TestOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: TestInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
    is_sandbox: Union[None, Unset, bool] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    json_is_sandbox: Union[None, Unset, bool]
    if isinstance(is_sandbox, Unset):
        json_is_sandbox = UNSET
    else:
        json_is_sandbox = is_sandbox
    params["is_sandbox"] = json_is_sandbox

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/tests/",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = TestOutSchema.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorSchema.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorSchema.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorSchema.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TestInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
    is_sandbox: Union[None, Unset, bool] = UNSET,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Create Test

    Args:
        workspace_uuid (Union[Unset, str]):
        is_sandbox (Union[None, Unset, bool]):
        body (TestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
        workspace_uuid=workspace_uuid,
        is_sandbox=is_sandbox,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TestInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
    is_sandbox: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Create Test

    Args:
        workspace_uuid (Union[Unset, str]):
        is_sandbox (Union[None, Unset, bool]):
        body (TestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
        workspace_uuid=workspace_uuid,
        is_sandbox=is_sandbox,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TestInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
    is_sandbox: Union[None, Unset, bool] = UNSET,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Create Test

    Args:
        workspace_uuid (Union[Unset, str]):
        is_sandbox (Union[None, Unset, bool]):
        body (TestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
        workspace_uuid=workspace_uuid,
        is_sandbox=is_sandbox,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TestInSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
    is_sandbox: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Create Test

    Args:
        workspace_uuid (Union[Unset, str]):
        is_sandbox (Union[None, Unset, bool]):
        body (TestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            workspace_uuid=workspace_uuid,
            is_sandbox=is_sandbox,
        )
    ).parsed
