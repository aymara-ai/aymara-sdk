from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_schema import ErrorResponseSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    summary_uuid: str,
    *,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["workspace_uuid"] = workspace_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/scores/summary/{summary_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponseSchema]]:
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
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ErrorResponseSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    summary_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ErrorResponseSchema]]:
    """Delete Score Run Suite Summary

    Args:
        summary_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponseSchema]]
    """

    kwargs = _get_kwargs(
        summary_uuid=summary_uuid,
        workspace_uuid=workspace_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    summary_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ErrorResponseSchema]]:
    """Delete Score Run Suite Summary

    Args:
        summary_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponseSchema]
    """

    return sync_detailed(
        summary_uuid=summary_uuid,
        client=client,
        workspace_uuid=workspace_uuid,
    ).parsed


async def asyncio_detailed(
    summary_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ErrorResponseSchema]]:
    """Delete Score Run Suite Summary

    Args:
        summary_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponseSchema]]
    """

    kwargs = _get_kwargs(
        summary_uuid=summary_uuid,
        workspace_uuid=workspace_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    summary_uuid: str,
    *,
    client: AuthenticatedClient,
    workspace_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ErrorResponseSchema]]:
    """Delete Score Run Suite Summary

    Args:
        summary_uuid (str):
        workspace_uuid (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponseSchema]
    """

    return (
        await asyncio_detailed(
            summary_uuid=summary_uuid,
            client=client,
            workspace_uuid=workspace_uuid,
        )
    ).parsed
