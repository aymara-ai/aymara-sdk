from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paged_score_run_out_schema import PagedScoreRunOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    test_uuid: Union[Unset, str] = UNSET,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["test_uuid"] = test_uuid

    params["workspace_uuid"] = workspace_uuid

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/scores/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PagedScoreRunOutSchema]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PagedScoreRunOutSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PagedScoreRunOutSchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    test_uuid: Union[Unset, str] = UNSET,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[PagedScoreRunOutSchema]:
    """List Score Runs

    Args:
        test_uuid (Union[Unset, str]):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PagedScoreRunOutSchema]
    """

    kwargs = _get_kwargs(
        test_uuid=test_uuid,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    test_uuid: Union[Unset, str] = UNSET,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[PagedScoreRunOutSchema]:
    """List Score Runs

    Args:
        test_uuid (Union[Unset, str]):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PagedScoreRunOutSchema
    """

    return sync_detailed(
        client=client,
        test_uuid=test_uuid,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    test_uuid: Union[Unset, str] = UNSET,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[PagedScoreRunOutSchema]:
    """List Score Runs

    Args:
        test_uuid (Union[Unset, str]):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PagedScoreRunOutSchema]
    """

    kwargs = _get_kwargs(
        test_uuid=test_uuid,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    test_uuid: Union[Unset, str] = UNSET,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[PagedScoreRunOutSchema]:
    """List Score Runs

    Args:
        test_uuid (Union[Unset, str]):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PagedScoreRunOutSchema
    """

    return (
        await asyncio_detailed(
            client=client,
            test_uuid=test_uuid,
            workspace_uuid=workspace_uuid,
            limit=limit,
            offset=offset,
        )
    ).parsed
