from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_schema import ErrorResponseSchema
from ...models.get_image_presigned_urls_response import GetImagePresignedUrlsResponse
from ...models.image_upload_request_in_schema import ImageUploadRequestInSchema
from ...types import Response


def _get_kwargs(
    *,
    body: ImageUploadRequestInSchema,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/scores/image/get-presigned-urls",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetImagePresignedUrlsResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ImageUploadRequestInSchema,
) -> Response[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    """Get Image Presigned Urls

     Generate presigned URLs for image uploads, keyed by question UUID.

    Each URL will be used to upload an image for a specific question in an image safety test.

    Args:
        body (ImageUploadRequestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]
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
    body: ImageUploadRequestInSchema,
) -> Optional[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    """Get Image Presigned Urls

     Generate presigned URLs for image uploads, keyed by question UUID.

    Each URL will be used to upload an image for a specific question in an image safety test.

    Args:
        body (ImageUploadRequestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ImageUploadRequestInSchema,
) -> Response[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    """Get Image Presigned Urls

     Generate presigned URLs for image uploads, keyed by question UUID.

    Each URL will be used to upload an image for a specific question in an image safety test.

    Args:
        body (ImageUploadRequestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ImageUploadRequestInSchema,
) -> Optional[Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]]:
    """Get Image Presigned Urls

     Generate presigned URLs for image uploads, keyed by question UUID.

    Each URL will be used to upload an image for a specific question in an image safety test.

    Args:
        body (ImageUploadRequestInSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponseSchema, GetImagePresignedUrlsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
