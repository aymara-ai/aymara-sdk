import asyncio

import pandas as pd
import pytest

from aymara_sdk.core.sdk import AymaraAI
from aymara_sdk.types import Status, TestResponse
from aymara_sdk.utils.constants import DEFAULT_TEST_LANGUAGE, AymaraTestPolicy


class TestTestMixin:
    @pytest.fixture
    def test_data(self):
        return {
            "test_name": "Integration Test",
            "student_description": "An AI assistant for customer support",
            "test_policy": AymaraTestPolicy.ANIMAL_ABUSE,
            "test_language": DEFAULT_TEST_LANGUAGE,
            "n_test_questions": 5,
        }

    @pytest.mark.parametrize(
        "test_policy",
        [
            AymaraTestPolicy.ANIMAL_ABUSE,
            AymaraTestPolicy.BIAS_DISCRIMINATION,
            AymaraTestPolicy.SEXUALLY_EXPLICIT,
            "custom_policy_string",
        ],
    )
    def test_create_test_sync_different_policies(
        self, aymara_client, test_data, test_policy, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        test_data["test_policy"] = test_policy
        response = aymara_client.create_test(**test_data)
        created_test_uuids.append(response.test_uuid)
        assert isinstance(response, TestResponse)
        assert response.test_status == Status.COMPLETED
        assert len(response.questions) == test_data["n_test_questions"]

    @pytest.mark.parametrize("test_language", ["en"])
    async def test_create_test_async_different_languages(
        self, aymara_client, test_data, test_language, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        test_data["test_language"] = test_language
        response = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(response.test_uuid)
        assert isinstance(response, TestResponse)
        assert response.test_status == Status.COMPLETED
        assert len(response.questions) == test_data["n_test_questions"]

    @pytest.mark.parametrize("n_test_questions", [1, 10, 25, 50])
    def test_create_test_sync_different_question_counts(
        self, aymara_client, test_data, n_test_questions, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        test_data["n_test_questions"] = n_test_questions
        response = aymara_client.create_test(**test_data)
        created_test_uuids.append(response.test_uuid)
        assert isinstance(response, TestResponse)
        assert response.test_status == Status.COMPLETED
        assert len(response.questions) == n_test_questions

    def test_get_test_sync(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = aymara_client.create_test(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        retrieved_test = aymara_client.get_test(created_test.test_uuid)
        assert isinstance(retrieved_test, TestResponse)
        assert retrieved_test.test_uuid == created_test.test_uuid
        assert retrieved_test.test_status == Status.COMPLETED

    async def test_get_test_async(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        retrieved_test = await aymara_client.get_test_async(created_test.test_uuid)
        assert isinstance(retrieved_test, TestResponse)
        assert retrieved_test.test_uuid == created_test.test_uuid
        assert retrieved_test.test_status == Status.COMPLETED

    def test_list_tests_sync(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = aymara_client.create_test(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        tests_list = aymara_client.list_tests()
        assert isinstance(tests_list, list)
        assert len(tests_list) > 0
        assert all(isinstance(test, TestResponse) for test in tests_list)

    async def test_list_tests_async(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        tests_list = await aymara_client.list_tests_async()
        assert isinstance(tests_list, list)
        assert len(tests_list) > 0
        assert all(isinstance(test, TestResponse) for test in tests_list)

    def test_list_tests_as_df_sync(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = aymara_client.create_test(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        df = aymara_client.list_tests(as_df=True)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert all(
            col in df.columns
            for col in ["test_uuid", "test_name", "test_status", "failure_reason"]
        )

    async def test_list_tests_as_df_async(
        self, aymara_client, test_data, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        created_test = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        df = await aymara_client.list_tests_async(as_df=True)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert all(
            col in df.columns
            for col in ["test_uuid", "test_name", "test_status", "failure_reason"]
        )

    @pytest.mark.parametrize(
        "invalid_input",
        [
            {"test_name": "a" * 256},  # Too long test name
            {"test_name": ""},  # Empty test name
            {"n_test_questions": 0},  # Too few questions
            {"n_test_questions": 151},  # Too many questions
            {"test_policy": None},  # Missing test policy
            {"test_language": "invalid_language"},  # Invalid language
            {"student_description": ""},  # Empty student description
        ],
    )
    def test_create_test_invalid_inputs(
        self, aymara_client, test_data, invalid_input, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        invalid_data = {**test_data, **invalid_input}
        with pytest.raises(ValueError):
            created_test = aymara_client.create_test(**invalid_data)
            created_test_uuids.append(created_test.test_uuid)

    def test_create_test_timeout(
        self, aymara_client, test_data, monkeypatch, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        # Patch the max_wait_time property of the client
        monkeypatch.setattr(aymara_client, "max_wait_time", 0.1)

        response = aymara_client.create_test(**test_data)
        created_test_uuids.append(response.test_uuid)
        assert response.test_status == Status.FAILED
        assert response.failure_reason == "Test creation timed out"

    async def test_create_test_async_timeout(
        self, aymara_client, test_data, monkeypatch, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        # Patch the max_wait_time property of the client
        monkeypatch.setattr(aymara_client, "max_wait_time", 0.1)

        response = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(response.test_uuid)
        assert response.test_status == Status.FAILED
        assert response.failure_reason == "Test creation timed out"

    def test_get_nonexistent_test(self, aymara_client):
        with pytest.raises(ValueError):
            aymara_client.get_test("nonexistent_uuid")

    async def test_get_nonexistent_test_async(self, aymara_client):
        with pytest.raises(ValueError):
            await aymara_client.get_test_async("nonexistent_uuid")

    def test_create_multiple_tests(self, aymara_client, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        responses = [aymara_client.create_test(**test_data) for _ in range(3)]
        created_test_uuids.extend([response.test_uuid for response in responses])
        assert all(isinstance(response, TestResponse) for response in responses)
        assert all(response.test_status == Status.COMPLETED for response in responses)

    async def test_create_multiple_tests_async(
        self, aymara_client, test_data, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        responses = await asyncio.gather(
            *[aymara_client.create_test_async(**test_data) for _ in range(3)]
        )
        created_test_uuids.extend([response.test_uuid for response in responses])
        assert all(isinstance(response, TestResponse) for response in responses)
        assert all(response.test_status == Status.COMPLETED for response in responses)

    def test_delete_test(self, aymara_client: AymaraAI, test_data, cleanup_after_test):
        created_test_uuids, _, _ = cleanup_after_test
        # Create a test to delete
        created_test = aymara_client.create_test(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        assert created_test.test_status == Status.COMPLETED

        # Delete the test
        aymara_client.delete_test(created_test.test_uuid)

        # Attempt to get the deleted test
        with pytest.raises(ValueError):
            aymara_client.get_test(created_test.test_uuid)

    async def test_delete_test_async(
        self, aymara_client: AymaraAI, test_data, cleanup_after_test
    ):
        created_test_uuids, _, _ = cleanup_after_test
        # Create a test to delete
        created_test = await aymara_client.create_test_async(**test_data)
        created_test_uuids.append(created_test.test_uuid)
        assert created_test.test_status == Status.COMPLETED

        # Delete the test
        await aymara_client.delete_test_async(created_test.test_uuid)

        # Attempt to get the deleted test
        with pytest.raises(ValueError):
            await aymara_client.get_test_async(created_test.test_uuid)

    def test_delete_nonexistent_test(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            aymara_client.delete_test("nonexistent_uuid")

    async def test_delete_nonexistent_test_async(self, aymara_client: AymaraAI):
        with pytest.raises(ValueError):
            await aymara_client.delete_test_async("nonexistent_uuid")
