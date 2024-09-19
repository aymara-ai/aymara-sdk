from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paged_score_run_suite_summary_out_schema import PagedScoreRunSuiteSummaryOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/scores/summary/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PagedScoreRunSuiteSummaryOutSchema]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PagedScoreRunSuiteSummaryOutSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PagedScoreRunSuiteSummaryOutSchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[PagedScoreRunSuiteSummaryOutSchema]:
    """List Score Run Suite Summaries

    Args:
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PagedScoreRunSuiteSummaryOutSchema]
    """

    kwargs = _get_kwargs(
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
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[PagedScoreRunSuiteSummaryOutSchema]:
    """List Score Run Suite Summaries

    Args:
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PagedScoreRunSuiteSummaryOutSchema
    """

    return sync_detailed(
        client=client,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[PagedScoreRunSuiteSummaryOutSchema]:
    """List Score Run Suite Summaries

    Args:
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PagedScoreRunSuiteSummaryOutSchema]
    """

    kwargs = _get_kwargs(
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[PagedScoreRunSuiteSummaryOutSchema]:
    """List Score Run Suite Summaries

    Args:
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PagedScoreRunSuiteSummaryOutSchema
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace_uuid=workspace_uuid,
            limit=limit,
            offset=offset,
        )
    ).parsed
