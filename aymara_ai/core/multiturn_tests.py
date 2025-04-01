from typing import List, Optional

from aymara_ai.core.errors import get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import continue_multiturn


class MultiturnTestMixin(AymaraAIProtocol):
    def continue_multiturn(
        self,
        test_uuid: str,
        messages: List[dict],
        max_wait_time_secs: Optional[int] = None,
        continue_eval: bool = True,
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
            continue_eval=continue_eval,
        )
        parsed_response = get_parsed_response(response)

        return parsed_response

    async def continue_multiturn_async(
        self,
        test_uuid: str,
        messages: List[dict],
        max_wait_time_secs: Optional[int] = None,
        continue_eval: bool = True,
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
            continue_eval=continue_eval,
        )

        parsed_response = get_parsed_response(response)

        return parsed_response

    def continue_multiturn_from_dict(
        self,
        test_uuid: str,
        messages: List[dict],
        max_wait_time_secs: Optional[int] = None,
        continue_eval: bool = True,
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

        return self.continue_multiturn(
            continue_request, max_wait_time_secs, continue_eval
        )
