"""HTTP client for interacting with the API."""

import logging
from typing import Dict, Any, Optional
import aiohttp
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TIMEOUT = 30


class HTTPClient:
    """
    A client for making HTTP requests with support for both synchronous and asynchronous operations.
    Automatically manages session lifecycle when used as a context manager.
    """

    def __init__(self, base_url: str = "", api_key: str = "", timeout: int = TIMEOUT):
        """
        Initialize the HTTPClient.

        Args:
            base_url (str): The base URL for all requests.
            api_key (str): The API key for authentication.
            timeout (int): The timeout for requests in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.api_key = api_key
        self._sync_session = requests.Session()
        self._async_session = None
        logger.debug("HTTPClient initialized with base_url: %s", base_url)

    def _get_full_url(self, endpoint: str) -> str:
        """Construct the full URL for a given endpoint."""
        return f"{self.base_url}/{endpoint}"

    def _get_headers(self) -> Dict[str, str]:
        """Get headers including the API key."""
        return {"x-api-key": self.api_key}

    def _handle_response(self, response: requests.Response):
        """Handle the response for synchronous requests."""
        response.raise_for_status()
        logger.debug("Received response: status=%s", response.status_code)
        return response.json()

    async def _handle_async_response(self, response: aiohttp.ClientResponse):
        """Handle the response for asynchronous requests."""
        response.raise_for_status()
        logger.debug("Received async response: status=%s", response.status)
        return await response.json()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a synchronous request."""
        url = self._get_full_url(endpoint)
        headers = self._get_headers()
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        logger.debug("Making %s request to %s", method, url)
        response = self._sync_session.request(
            method, url, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    async def _make_async_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an asynchronous request."""
        url = self._get_full_url(endpoint)
        headers = self._get_headers()
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        logger.debug("Making async %s request to %s", method, url)
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession()
        async with self._async_session.request(method, url, timeout=self.timeout, **kwargs) as response:
            return await self._handle_async_response(response)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a synchronous GET request."""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a synchronous POST request."""
        return self._make_request("POST", endpoint, data=data, json=json)

    async def async_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an asynchronous GET request."""
        return await self._make_async_request("GET", endpoint, params=params)

    async def async_post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an asynchronous POST request."""
        return await self._make_async_request("POST", endpoint, data=data, json=json)

    def close(self):
        """Close both synchronous and asynchronous sessions."""
        if self._sync_session:
            self._sync_session.close()
            self._sync_session = None
        logger.debug("Closed synchronous session")

    async def aclose(self):
        """Close the asynchronous session."""
        if self._async_session:
            await self._async_session.close()
            self._async_session = None
        logger.debug("Closed asynchronous session")

    def __enter__(self):
        """Enable the HTTPClient to be used as a context manager for synchronous operations."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the synchronous session is closed when exiting the context."""
        self.close()

    async def __aenter__(self):
        """Enable the HTTPClient to be used as an async context manager for asynchronous operations."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure the asynchronous session is closed when exiting the async context."""
        await self.aclose()

    def __del__(self):
        """Ensure synchronous session is closed when the object is garbage collected."""
        self.close()
