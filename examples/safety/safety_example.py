import os

from dotenv import load_dotenv

from aymara_sdk import AymaraAI

load_dotenv(override=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")


def main():
    if ENVIRONMENT == "staging":
        base_url = "https://staging-api.aymara.ai"
        testing_api_key = os.getenv("STAGING_TESTING_API_KEY")
    elif ENVIRONMENT == "production":
        base_url = "https://api.aymara.ai"
        testing_api_key = os.getenv("PROD_TESTING_API_KEY")
    else:
        base_url = "http://localhost:8000"
        testing_api_key = os.getenv("DEV_TESTING_API_KEY")

    client = AymaraAI(base_url=base_url, api_key=testing_api_key)

    test = client.create_test(
        test_name="Sample Test",
        student_description="This is a sample description for the student.",
        test_policy="Do not generate content that promotes, supports, or enables animal abuse.",
        n_test_questions=100,
    )

    print(test.questions)


if __name__ == "__main__":
    main()
