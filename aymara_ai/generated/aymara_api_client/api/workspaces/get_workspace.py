from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_schema import ErrorResponseSchema
from ...models.workspace_out_schema import WorkspaceOutSchema
from ...types import Response


def _get_kwargs(
    workspace_uuid: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/v1/workspaces/{workspace_uuid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceOutSchema.from_dict(response.json())

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
) -> Response[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, WorkspaceOutSchema]]
    """

    kwargs = _get_kwargs(
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, WorkspaceOutSchema]
    """

    return sync_detailed(
        workspace_uuid=workspace_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, WorkspaceOutSchema]]
    """

    kwargs = _get_kwargs(
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponseSchema, WorkspaceOutSchema]]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, WorkspaceOutSchema]
    """

    return (
        await asyncio_detailed(
            workspace_uuid=workspace_uuid,
            client=client,
        )
    ).parsed
