from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
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
) -> Optional[WorkspaceOutSchema]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceOutSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WorkspaceOutSchema]:
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
) -> Response[WorkspaceOutSchema]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceOutSchema]
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
) -> Optional[WorkspaceOutSchema]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceOutSchema
    """

    return sync_detailed(
        workspace_uuid=workspace_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[WorkspaceOutSchema]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceOutSchema]
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
) -> Optional[WorkspaceOutSchema]:
    """Get Workspace

    Args:
        workspace_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceOutSchema
    """

    return (
        await asyncio_detailed(
            workspace_uuid=workspace_uuid,
            client=client,
        )
    ).parsed