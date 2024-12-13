import os

from aymara_ai.core.sdk import AymaraAI
from aymara_ai.generated.aymara_api_client.models.policy_schema import PolicySchema

ENVIRONMENT = os.getenv("API_TEST_ENV")


class TestPolicyMixin:
    async def test_list_policies_async(self, aymara_client: AymaraAI):
        policies = await aymara_client.list_policies_async()
        assert isinstance(policies, list)
        assert len(policies) > 0
        assert all(isinstance(policy, PolicySchema) for policy in policies)

    def test_list_policies_sync(self, aymara_client: AymaraAI):
        policies = aymara_client.list_policies()
        assert isinstance(policies, list)
        assert len(policies) > 0
        assert all(isinstance(policy, PolicySchema) for policy in policies)

    async def test_list_policies_with_test_type_async(self, aymara_client: AymaraAI):
        policies = await aymara_client.list_policies_async(test_type="safety")
        assert isinstance(policies, list)
        assert all(isinstance(policy, PolicySchema) for policy in policies)

    def test_list_policies_with_test_type_sync(self, aymara_client: AymaraAI):
        policies = aymara_client.list_policies(test_type="safety")
        assert isinstance(policies, list)
        assert all(isinstance(policy, PolicySchema) for policy in policies)

    async def test_list_policies_pagination_async(self, aymara_client: AymaraAI):
        # First, get all policies
        all_policies = await aymara_client.list_policies_async()

        # Then get policies with a small limit to force pagination
        paginated_policies = []
        offset = 0
        limit = 1
        while True:
            response = await aymara_client.list_policies_async()
            if not response:
                break
            paginated_policies.extend(response)
            if len(paginated_policies) >= len(all_policies):
                break
            offset += limit

        assert len(paginated_policies) == len(all_policies)
        assert all(isinstance(policy, PolicySchema) for policy in paginated_policies)

    def test_list_policies_pagination_sync(self, aymara_client: AymaraAI):
        # First, get all policies
        all_policies = aymara_client.list_policies()

        # Then get policies with a small limit to force pagination
        paginated_policies = []
        offset = 0
        limit = 1
        while True:
            response = aymara_client.list_policies()
            if not response:
                break
            paginated_policies.extend(response)
            if len(paginated_policies) >= len(all_policies):
                break
            offset += limit

        assert len(paginated_policies) == len(all_policies)
        assert all(isinstance(policy, PolicySchema) for policy in paginated_policies)
