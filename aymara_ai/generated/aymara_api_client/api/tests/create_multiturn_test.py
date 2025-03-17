from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_schema import ErrorSchema
from ...models.multiturn_test_in_schema import MultiturnTestInSchema
from ...models.test_out_schema import TestOutSchema
from ...types import Response


def _get_kwargs(
    *,
    body: MultiturnTestInSchema,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/tests/multiturn",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = TestOutSchema.from_dict(response.json())

        return response_201
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
    body: MultiturnTestInSchema,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Create Multiturn Test

     Create a multiturn test with multiple conversations.

    Args:
        body (MultiturnTestInSchema): Schema for creating a multiturn safety test.

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
    body: MultiturnTestInSchema,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Create Multiturn Test

     Create a multiturn test with multiple conversations.

    Args:
        body (MultiturnTestInSchema): Schema for creating a multiturn safety test.

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
    body: MultiturnTestInSchema,
) -> Response[Union[ErrorSchema, TestOutSchema]]:
    """Create Multiturn Test

     Create a multiturn test with multiple conversations.

    Args:
        body (MultiturnTestInSchema): Schema for creating a multiturn safety test.

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
    body: MultiturnTestInSchema,
) -> Optional[Union[ErrorSchema, TestOutSchema]]:
    """Create Multiturn Test

     Create a multiturn test with multiple conversations.

    Args:
        body (MultiturnTestInSchema): Schema for creating a multiturn safety test.

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
