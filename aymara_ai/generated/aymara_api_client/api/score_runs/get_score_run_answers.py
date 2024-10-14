from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_schema import ErrorSchema
from ...models.paged_answer_out_schema import PagedAnswerOutSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    score_run_uuid: str,
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
        "url": f"/v1/scores/{score_run_uuid}/answers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorSchema, PagedAnswerOutSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PagedAnswerOutSchema.from_dict(response.json())

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
) -> Response[Union[ErrorSchema, PagedAnswerOutSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    score_run_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[ErrorSchema, PagedAnswerOutSchema]]:
    """Get Score Run Answers

    Args:
        score_run_uuid (str):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, PagedAnswerOutSchema]]
    """

    kwargs = _get_kwargs(
        score_run_uuid=score_run_uuid,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    score_run_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[ErrorSchema, PagedAnswerOutSchema]]:
    """Get Score Run Answers

    Args:
        score_run_uuid (str):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, PagedAnswerOutSchema]
    """

    return sync_detailed(
        score_run_uuid=score_run_uuid,
        client=client,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    score_run_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[ErrorSchema, PagedAnswerOutSchema]]:
    """Get Score Run Answers

    Args:
        score_run_uuid (str):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, PagedAnswerOutSchema]]
    """

    kwargs = _get_kwargs(
        score_run_uuid=score_run_uuid,
        workspace_uuid=workspace_uuid,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    score_run_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[ErrorSchema, PagedAnswerOutSchema]]:
    """Get Score Run Answers

    Args:
        score_run_uuid (str):
        workspace_uuid (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, PagedAnswerOutSchema]
    """

    return (
        await asyncio_detailed(
            score_run_uuid=score_run_uuid,
            client=client,
            workspace_uuid=workspace_uuid,
            limit=limit,
            offset=offset,
        )
    ).parsed
