import asyncio

import pytest

from aymara_ai.core.sdk import AymaraAI

API_KEY = "test_api_key"


@pytest.fixture(scope="session")
def api_key():
    return API_KEY


@pytest.fixture(scope="session")
def aymara_client(api_key, event_loop) -> AymaraAI:
    return AymaraAI(api_key=api_key)


# This sets up a single event loop for the entire test session
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
