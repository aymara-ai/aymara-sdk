from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.score_run_out_schema import ScoreRunOutSchema
from ...models.score_run_schema import ScoreRunSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ScoreRunSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/scores/",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ScoreRunOutSchema]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ScoreRunOutSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ScoreRunOutSchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ScoreRunSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[ScoreRunOutSchema]:
    """Create Score Run

    Args:
        workspace_uuid (Union[Unset, str]):
        body (ScoreRunSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScoreRunOutSchema]
    """

    kwargs = _get_kwargs(
        body=body,
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ScoreRunSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[ScoreRunOutSchema]:
    """Create Score Run

    Args:
        workspace_uuid (Union[Unset, str]):
        body (ScoreRunSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScoreRunOutSchema
    """

    return sync_detailed(
        client=client,
        body=body,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ScoreRunSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[ScoreRunOutSchema]:
    """Create Score Run

    Args:
        workspace_uuid (Union[Unset, str]):
        body (ScoreRunSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScoreRunOutSchema]
    """

    kwargs = _get_kwargs(
        body=body,
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ScoreRunSchema,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[ScoreRunOutSchema]:
    """Create Score Run

    Args:
        workspace_uuid (Union[Unset, str]):
        body (ScoreRunSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScoreRunOutSchema
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
