"""HTTP client for interacting with the API."""
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class HTTPClient:
    """Synchronous HTTP client for interacting with the API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        logger.debug("HTTPClient initialized with base URL: %s", self.base_url)

    def __enter__(self) -> 'HTTPClient':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
        logger.debug("HTTPClient session closed")

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        logger.info("Sending %s request to %s", method, url)
        response = self.session.request(method, url, **kwargs)
        logger.debug("Response status code: %s", response.status_code)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request to the API."""
        logger.info("Sending GET request to %s", path)
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Dict[str, Any]) -> Any:
        """Send a POST request to the API."""
        logger.info("Sending POST request to %s", path)
        return self._request("POST", path, json=json)

    def put(self, path: str, json: Dict[str, Any]) -> Any:
        """Send a PUT request to the API."""
        logger.info("Sending PUT request to %s", path)
        return self._request("PUT", path, json=json)

    def delete(self, path: str) -> Any:
        """Send a DELETE request to the API."""
        logger.info("Sending DELETE request to %s", path)
        return self._request("DELETE", path)
