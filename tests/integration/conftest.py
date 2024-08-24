import os
import pytest
from aymara_sdk.sdk import AymaraAI
from dotenv import load_dotenv

load_dotenv(override=True)

# Read environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")


@pytest.fixture
def aymara_client():
    if ENVIRONMENT == "staging":
        base_url = "https://staging-api.aymara.ai"
        testing_api_key = os.getenv("STAGING_TESTING_API_KEY")
    elif ENVIRONMENT == "production":
        base_url = "https://api.aymara.ai"
        testing_api_key = os.getenv("PROD_TESTING_API_KEY")
    else:
        base_url = "http://localhost:8000"
        testing_api_key = os.getenv("DEV_TESTING_API_KEY")

    return AymaraAI(api_key=testing_api_key, base_url=base_url)
