from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client.api.policies import list_policies
from aymara_ai.generated.aymara_api_client.models.policy_schema import PolicySchema


class PolicyMixin(AymaraAIProtocol):
    def list_policies(
        self,
        test_type: Optional[str] = None,
    ) -> List[PolicySchema]:
        """
        List all policies, optionally filtered by test type.

        :param test_type: Optional filter for specific test type
        :type test_type: Optional[str]
        :return: List of policies
        :rtype: List[PolicySchema]
        """
        return self._list_policies(test_type=test_type, is_async=False)

    async def list_policies_async(
        self,
        test_type: Optional[str] = None,
    ) -> List[PolicySchema]:
        """
        List all policies asynchronously, optionally filtered by test type.

        :param test_type: Optional filter for specific test type
        :type test_type: Optional[str]
        :return: List of policies
        :rtype: List[PolicySchema]
        """
        return await self._list_policies(test_type=test_type, is_async=True)

    def _list_policies(
        self,
        test_type: Optional[str] = None,
        is_async: bool = False,
    ) -> Union[List[PolicySchema], Coroutine[List[PolicySchema], None, None]]:
        if is_async:
            return self._list_policies_async_impl(test_type)
        else:
            return self._list_policies_sync_impl(test_type)

    def _list_policies_sync_impl(
        self,
        test_type: Optional[str] = None,
    ) -> List[PolicySchema]:
        all_policies = []
        offset = 0
        while True:
            response = list_policies.sync_detailed(
                client=self.client,
                test_type=test_type,
                offset=offset,
            )
            paged_response = response.parsed
            all_policies.extend(paged_response.items)
            if len(all_policies) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return all_policies

    async def _list_policies_async_impl(
        self,
        test_type: Optional[str] = None,
    ) -> List[PolicySchema]:
        all_policies = []
        offset = 0
        while True:
            response = await list_policies.asyncio_detailed(
                client=self.client,
                test_type=test_type,
                offset=offset,
            )
            paged_response = response.parsed
            all_policies.extend(paged_response.items)
            if len(all_policies) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return all_policies
