import pytest
from pytest_asyncio import is_async_test

from aymara_ai.core.sdk import AymaraAI

API_KEY = "test_api_key"


@pytest.fixture(scope="session")
def api_key():
    return API_KEY


@pytest.fixture(scope="session")
def aymara_client(api_key) -> AymaraAI:
    return AymaraAI(api_key=api_key)


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
