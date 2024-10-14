import os

import pytest
from dotenv import load_dotenv
from pytest_asyncio import is_async_test

from aymara_ai import AymaraAI

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


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(autouse=True, scope="session")
def cleanup_after_test(aymara_client: AymaraAI):
    created_test_uuids = []
    created_score_run_uuids = []
    created_summary_uuids = []

    yield created_test_uuids, created_score_run_uuids, created_summary_uuids

    for test_uuid in created_test_uuids:
        try:
            aymara_client.delete_test(test_uuid)
        except ValueError:
            pass
    print("Deleted %s tests", len(created_test_uuids))

    for score_run_uuid in created_score_run_uuids:
        try:
            aymara_client.delete_score_run(score_run_uuid)
        except ValueError:
            pass
    print("Deleted %s score runs", len(created_score_run_uuids))

    for summary_uuid in created_summary_uuids:
        try:
            aymara_client.delete_summary(summary_uuid)
        except ValueError:
            pass
    print("Deleted %s summaries", len(created_summary_uuids))
