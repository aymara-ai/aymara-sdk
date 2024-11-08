from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
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
) -> Optional[UsageResponseSchema]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UsageResponseSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UsageResponseSchema]:
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
) -> Response[UsageResponseSchema]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsageResponseSchema]
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
) -> Optional[UsageResponseSchema]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsageResponseSchema
    """

    return sync_detailed(
        client=client,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[None, Unset, str] = UNSET,
) -> Response[UsageResponseSchema]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsageResponseSchema]
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
) -> Optional[UsageResponseSchema]:
    """Get Usage

    Args:
        workspace_uuid (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsageResponseSchema
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
