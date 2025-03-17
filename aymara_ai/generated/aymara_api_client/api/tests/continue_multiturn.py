from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_schema import ErrorSchema
from ...models.multiturn_continue_in_schema import MultiturnContinueInSchema
from ...models.test_out_schema import TestOutSchema
from ...types import Response


def _get_kwargs(
    *,
    body: List["MultiturnContinueInSchema"],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/tests/multiturn/continue",
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
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TestOutSchema.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorSchema.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorSchema.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorSchema.from_dict(response.json())

        return response_500
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
    *,
    client: AuthenticatedClient,
    body: List["MultiturnContinueInSchema"],
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Continue Multiturn

     Continue multiple conversations in a multiturn test with user messages.

    Args:
        body (List['MultiturnContinueInSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
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
    body: List["MultiturnContinueInSchema"],
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Continue Multiturn

     Continue multiple conversations in a multiturn test with user messages.

    Args:
        body (List['MultiturnContinueInSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnContinueInSchema"],
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Continue Multiturn

     Continue multiple conversations in a multiturn test with user messages.

    Args:
        body (List['MultiturnContinueInSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorSchema, TestOutSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: List["MultiturnContinueInSchema"],
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Continue Multiturn

     Continue multiple conversations in a multiturn test with user messages.

    Args:
        body (List['MultiturnContinueInSchema']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorSchema, TestOutSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
