from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.continue_multiturn_response import ContinueMultiturnResponse
from ...models.error_response_schema import ErrorResponseSchema
from ...models.multiturn_user_response_schema import MultiturnUserResponseSchema
from ...types import Response


def _get_kwargs(
    *,
    body: List["MultiturnUserResponseSchema"],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/tests/continue_multiturn",
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ContinueMultiturnResponse.from_dict(response.json())

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
) -> Response[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnUserResponseSchema"],
) -> Response[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    """Continue Multiturn

    Args:
        body (List['MultiturnUserResponseSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ContinueMultiturnResponse, ErrorResponseSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnUserResponseSchema"],
) -> Optional[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    """Continue Multiturn

    Args:
        body (List['MultiturnUserResponseSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ContinueMultiturnResponse, ErrorResponseSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnUserResponseSchema"],
) -> Response[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    """Continue Multiturn

    Args:
        body (List['MultiturnUserResponseSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ContinueMultiturnResponse, ErrorResponseSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnUserResponseSchema"],
) -> Optional[Union[ContinueMultiturnResponse, ErrorResponseSchema]]:
    """Continue Multiturn

    Args:
        body (List['MultiturnUserResponseSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ContinueMultiturnResponse, ErrorResponseSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
