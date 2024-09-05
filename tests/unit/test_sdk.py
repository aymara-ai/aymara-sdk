import os
from unittest.mock import AsyncMock, patch

import pytest

from aymara_sdk import AymaraAI
from aymara_sdk.utils.constants import DEFAULT_MAX_WAIT_TIME


def test_aymara_ai_initialization():
    # Clear the AYMARA_API_KEY environment variable
    if "AYMARA_API_KEY" in os.environ:
        del os.environ["AYMARA_API_KEY"]
    with pytest.raises(ValueError):
        AymaraAI()  # No API key provided

    ai = AymaraAI(api_key="test_api_key")
    assert ai.client is not None
    assert ai.max_wait_time == DEFAULT_MAX_WAIT_TIME

    ai_custom = AymaraAI(
        api_key="test_api_key", base_url="https://custom.api.com", max_wait_time=300
    )
    assert ai_custom.client._base_url == "https://custom.api.com"
    assert ai_custom.max_wait_time == 300


def test_aymara_ai_context_manager():
    with patch("aymara_sdk.core.sdk.client.Client") as mock_client:
        with AymaraAI(api_key="test_api_key") as ai:
            assert ai.client is not None
        mock_client.return_value._client.close.assert_called_once()


@pytest.mark.asyncio
async def test_aymara_ai_async_context_manager():
    with patch("aymara_sdk.core.sdk.client.Client") as mock_client:
        mock_async_client = mock_client.return_value._async_client
        mock_async_client.aclose = AsyncMock()
        async with AymaraAI(api_key="test_api_key") as ai:
            assert ai.client is not None
        mock_async_client.aclose.assert_called_once()
