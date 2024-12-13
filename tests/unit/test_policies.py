from unittest.mock import patch

import pytest

from aymara_ai.generated.aymara_api_client.models.paged_policy_schema import (
    PagedPolicySchema,
)
from aymara_ai.generated.aymara_api_client.models.policy_schema import PolicySchema


def test_list_policies(aymara_client):
    with patch(
        "aymara_ai.core.policies.list_policies.sync_detailed"
    ) as mock_list_policies:
        # Mock first page
        mock_list_policies.return_value.parsed = PagedPolicySchema(
            items=[
                PolicySchema(
                    test_type="safety",
                    test_language="en",
                    aymara_policy_name="Test Policy 1",
                    display_name="Test Policy 1",
                    policy_text="Description 1",
                ),
                PolicySchema(
                    test_type="safety",
                    test_language="en",
                    aymara_policy_name="Test Policy 2",
                    display_name="Test Policy 2",
                    policy_text="Description 2",
                ),
            ],
            count=2,
        )

        result = aymara_client.list_policies()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(policy, PolicySchema) for policy in result)
        assert result[0].aymara_policy_name == "Test Policy 1"
        assert result[1].aymara_policy_name == "Test Policy 2"


def test_list_policies_with_test_type(aymara_client):
    with patch(
        "aymara_ai.core.policies.list_policies.sync_detailed"
    ) as mock_list_policies:
        # Mock response with test_type filter
        mock_list_policies.return_value.parsed = PagedPolicySchema(
            items=[
                PolicySchema(
                    test_type="safety",
                    test_language="en",
                    aymara_policy_name="Safety Policy",
                    display_name="Safety Policy",
                    policy_text="Safety Description",
                ),
            ],
            count=1,
        )

        result = aymara_client.list_policies(test_type="safety")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].aymara_policy_name == "Safety Policy"
        mock_list_policies.assert_called_with(
            client=aymara_client.client,
            test_type="safety",
            offset=0,
        )


def test_list_policies_pagination(aymara_client):
    with patch(
        "aymara_ai.core.policies.list_policies.sync_detailed"
    ) as mock_list_policies:
        # Mock first page
        mock_list_policies.side_effect = [
            type(
                "Response",
                (),
                {
                    "parsed": PagedPolicySchema(
                        items=[
                            PolicySchema(
                                test_type="safety",
                                test_language="en",
                                aymara_policy_name="Test Policy 1",
                                display_name="Test Policy 1",
                                policy_text="Description 1",
                            ),
                        ],
                        count=2,
                    )
                },
            ),
            # Mock second page
            type(
                "Response",
                (),
                {
                    "parsed": PagedPolicySchema(
                        items=[
                            PolicySchema(
                                test_type="safety",
                                test_language="en",
                                aymara_policy_name="Test Policy 2",
                                display_name="Test Policy 2",
                                policy_text="Description 2",
                            ),
                        ],
                        count=2,
                    )
                },
            ),
        ]

        result = aymara_client.list_policies()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].aymara_policy_name == "Test Policy 1"
        assert result[1].aymara_policy_name == "Test Policy 2"
        assert mock_list_policies.call_count == 2


@pytest.mark.asyncio
async def test_list_policies_async(aymara_client):
    with patch(
        "aymara_ai.core.policies.list_policies.asyncio_detailed"
    ) as mock_list_policies:
        # Mock response
        mock_list_policies.return_value.parsed = PagedPolicySchema(
            items=[
                PolicySchema(
                    test_type="safety",
                    test_language="en",
                    aymara_policy_name="Test Policy 1",
                    display_name="Test Policy 1",
                    policy_text="Description 1",
                ),
                PolicySchema(
                    test_type="safety",
                    test_language="en",
                    aymara_policy_name="Test Policy 2",
                    display_name="Test Policy 2",
                    policy_text="Description 2",
                ),
            ],
            count=2,
        )

        result = await aymara_client.list_policies_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(policy, PolicySchema) for policy in result)
        assert result[0].aymara_policy_name == "Test Policy 1"
        assert result[1].aymara_policy_name == "Test Policy 2"


@pytest.mark.asyncio
async def test_list_policies_async_pagination(aymara_client):
    with patch(
        "aymara_ai.core.policies.list_policies.asyncio_detailed"
    ) as mock_list_policies:
        # Mock first page
        mock_list_policies.side_effect = [
            type(
                "Response",
                (),
                {
                    "parsed": PagedPolicySchema(
                        items=[
                            PolicySchema(
                                test_type="safety",
                                test_language="en",
                                aymara_policy_name="Test Policy 1",
                                display_name="Test Policy 1",
                                policy_text="Description 1",
                            ),
                        ],
                        count=2,
                    )
                },
            ),
            # Mock second page
            type(
                "Response",
                (),
                {
                    "parsed": PagedPolicySchema(
                        items=[
                            PolicySchema(
                                test_type="safety",
                                test_language="en",
                                aymara_policy_name="Test Policy 2",
                                display_name="Test Policy 2",
                                policy_text="Description 2",
                            ),
                        ],
                        count=2,
                    )
                },
            ),
        ]

        result = await aymara_client.list_policies_async()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].aymara_policy_name == "Test Policy 1"
        assert result[1].aymara_policy_name == "Test Policy 2"
        assert mock_list_policies.call_count == 2
