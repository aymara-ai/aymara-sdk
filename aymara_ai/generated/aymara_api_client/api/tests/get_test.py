from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_schema import ErrorSchema
from ...models.test_out_schema import TestOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    test_uuid: str,
    *,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/v1/tests/{test_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TestOutSchema.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorSchema.from_dict(response.json())

        return response_404
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
    test_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Get Test

    Args:
        test_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
    """

    kwargs = _get_kwargs(
        test_uuid=test_uuid,
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    test_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Get Test

    Args:
        test_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return sync_detailed(
        test_uuid=test_uuid,
        client=client,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    test_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Get Test

    Args:
        test_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
    """

    kwargs = _get_kwargs(
        test_uuid=test_uuid,
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    test_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Get Test

    Args:
        test_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return (
        await asyncio_detailed(
            test_uuid=test_uuid,
            client=client,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
