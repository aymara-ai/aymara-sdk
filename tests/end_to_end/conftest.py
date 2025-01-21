import os

import pytest
from dotenv import load_dotenv
from pytest_asyncio import is_async_test

from aymara_ai import AymaraAI

load_dotenv(override=True)

# Read environment variables
ENVIRONMENT = os.getenv("API_TEST_ENV", "production")


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")


# Mark all tests in this directory with the e2e marker


def pytest_collection_modifyitems(items):
    """Automatically mark all tests in this directory with the e2e marker"""
    for item in items:
        # Check if the test is in the end_to_end directory
        if "end_to_end" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)

    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def client() -> AymaraAI:
    if ENVIRONMENT == "staging":
        base_url = "https://staging-api.aymara.ai"
        api_key = os.getenv("STAGING_E2E_TESTING_API_KEY")
    elif ENVIRONMENT == "production":
        base_url = "https://api.aymara.ai"
        api_key = os.getenv("PROD_E2E_TESTING_API_KEY")
    else:
        base_url = "http://localhost:8000"
        api_key = os.getenv("DEV_E2E_TESTING_API_KEY")

    if not api_key:
        pytest.skip(f"Missing {ENVIRONMENT}_E2E_TESTING_API_KEY environment variable")

    return AymaraAI(api_key=api_key, base_url=base_url)
