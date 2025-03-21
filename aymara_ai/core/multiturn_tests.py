from typing import List

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import continue_multiturn


class MultiturnTestMixin(AymaraAIProtocol):
    def continue_multiturn(
        self,
        test_uuid: str,
        messages: List[dict],
    ):
        """
        Continue multiple multiturn conversations by providing user responses.

        :param test_uuid: UUID of the test
        :param messages: List of message dictionaries, each containing conversation_uuid and message_text
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        # Convert raw message dictionaries to MessageInSchema objects
        formatted_messages = [
            models.MessageInSchema.from_dict(msg) if isinstance(msg, dict) else msg
            for msg in messages
        ]

        # Create the continue request
        continue_request = models.MultiturnContinueInSchema(
            test_uuid=test_uuid, messages=formatted_messages
        )

        response = continue_multiturn.sync_detailed(
            client=self.client,
            body=continue_request,
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

    async def continue_multiturn_async(
        self,
        test_uuid: str,
        messages: List[dict],
    ):
        """
        Continue multiple multiturn conversations asynchronously by providing user responses.

        :param test_uuid: UUID of the test
        :param messages: List of message dictionaries, each containing conversation_uuid and message_text
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        # Convert raw message dictionaries to MessageInSchema objects
        formatted_messages = [
            models.MessageInSchema.from_dict(msg) if isinstance(msg, dict) else msg
            for msg in messages
        ]

        # Create the continue request
        continue_request = models.MultiturnContinueInSchema(
            test_uuid=test_uuid, messages=formatted_messages
        )

        response = await continue_multiturn.asyncio_detailed(
            client=self.client,
            body=continue_request,
        )

        if response.status_code == 404:
            raise ValueError("Test or question not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

        return response.parsed

    def continue_multiturn_from_dict(
        self,
        test_uuid: str,
        messages: List[dict],
    ):
        """
        Convenience method to continue conversations using raw dictionary input.

        :param test_uuid: UUID of the test
        :param messages: List of message dictionaries, each containing conversation_uuid and message_text
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        formatted_messages = [models.MessageInSchema.from_dict(msg) for msg in messages]

        continue_request = models.MultiturnContinueInSchema(
            test_uuid=test_uuid, messages=formatted_messages
        )

        return self.continue_multiturn(continue_request)
