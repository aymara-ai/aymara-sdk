from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_schema import ErrorResponseSchema
from ...models.usage_response_schema import UsageResponseSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_workspace_uuid: Union[None, Unset, str]
    if isinstance(workspace_uuid, Unset):
        json_workspace_uuid = UNSET
    else:
        json_workspace_uuid = workspace_uuid
    params["workspace_uuid"] = json_workspace_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/usage/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponseSchema, UsageResponseSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UsageResponseSchema.from_dict(response.json())

        return response_200
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
) -> Response[Union[ErrorResponseSchema, UsageResponseSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponseSchema, UsageResponseSchema]]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, UsageResponseSchema]]
    """

    kwargs = _get_kwargs(
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponseSchema, UsageResponseSchema]]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, UsageResponseSchema]
    """

    return sync_detailed(
        client=client,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponseSchema, UsageResponseSchema]]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, UsageResponseSchema]]
    """

    kwargs = _get_kwargs(
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponseSchema, UsageResponseSchema]]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, UsageResponseSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
