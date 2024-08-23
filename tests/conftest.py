import pytest
from aymara_sdk.sdk import AymaraAI

API_KEY = "test_api_key"


@pytest.fixture(scope="session")
def api_key():
    return API_KEY


@pytest.fixture(scope="session")
def aymara_client(api_key):
    return AymaraAI(api_key=api_key)
