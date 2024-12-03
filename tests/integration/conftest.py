import os

import pytest
from dotenv import load_dotenv
from pytest_asyncio import is_async_test

from aymara_ai import AymaraAI
from aymara_ai.generated.aymara_api_client.api.integration_test import integration_test

load_dotenv(override=True)


# Read environment variables
ENVIRONMENT = os.getenv("API_TEST_ENV", "production")


@pytest.fixture(scope="session")
def aymara_client():
    if ENVIRONMENT == "staging":
        base_url = "https://staging-api.aymara.ai"
        testing_api_key = os.getenv("STAGING_INTEGRATION_TESTING_API_KEY")
    elif ENVIRONMENT == "production":
        base_url = "https://api.aymara.ai"
        testing_api_key = os.getenv("PROD_INTEGRATION_TESTING_API_KEY")
    else:
        base_url = "http://localhost:8000"
        testing_api_key = os.getenv("DEV_INTEGRATION_TESTING_API_KEY")

    return AymaraAI(api_key=testing_api_key, base_url=base_url)


@pytest.fixture(scope="session")
def free_aymara_client() -> AymaraAI:
    if ENVIRONMENT == "staging":
        base_url = "https://staging-api.aymara.ai"
        api_key = os.getenv("STAGING_FREE_INTEGRATION_TESTING_API_KEY")
    elif ENVIRONMENT == "production":
        base_url = "https://api.aymara.ai"
        api_key = os.getenv("PROD_FREE_INTEGRATION_TESTING_API_KEY")
    else:
        base_url = "http://localhost:8000"
        api_key = os.getenv("DEV_FREE_INTEGRATION_TESTING_API_KEY")

    return AymaraAI(api_key=api_key, base_url=base_url)


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session", autouse=True)
def cleanup(aymara_client):
    yield
    # Run integration test check endpoint to clean up test data
    integration_test.sync_detailed(client=aymara_client.client)
