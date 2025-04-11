from typing import List, Optional, Union

from aymara_ai.core.errors import get_parsed_response
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import continue_multiturn

from ..generated.aymara_api_client.models.multiturn_out_schema import MultiturnOutSchema


class MultiturnTestMixin(AymaraAIProtocol):
    def score_test_multiturn(
        self,
        test_uuid: str,
        answers: List[Union[dict, models.AnswerInSchema]],
        max_wait_time_secs: Optional[int] = None,
        continue_test: bool = True,
    ) -> MultiturnOutSchema:
        """
        Continue multiple multiturn conversations by providing user responses.

        :param test_uuid: UUID of the test
        :param answers: List of answer dictionaries, each containing conversation_uuid and message_text
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        # Convert raw answer dictionaries to AnswerInSchema objects
        formatted_answers = [
            answer if isinstance(answer, models.AnswerInSchema) else models.AnswerInSchema.from_dict(dict(answer))
            for answer in answers
        ]

        # Create the continue request
        continue_request = models.MultiturnContinueInSchema(test_uuid=test_uuid, answers=formatted_answers)

        response = continue_multiturn.sync_detailed(
            client=self.client,
            body=continue_request,
            continue_eval=continue_test,
        )
        parsed_response = get_parsed_response(response)

        return parsed_response

    async def score_test_multiturn_async(
        self,
        test_uuid: str,
        answers: List[dict],
        max_wait_time_secs: Optional[int] = None,
        continue_test: bool = True,
    ) -> MultiturnOutSchema:
        """
        Continue multiple multiturn conversations asynchronously by providing user responses.

        :param test_uuid: UUID of the test
        :param answers: List of answer dictionaries, each containing conversation_uuid and message_text
        :return: Response containing the next steps in the conversations
        :rtype: MultiturnOutSchema
        """
        # Convert raw answer dictionaries to AnswerInSchema objects
        formatted_answers = [
            answer if isinstance(answer, models.AnswerInSchema) else models.AnswerInSchema.from_dict(dict(answer))
            for answer in answers
        ]

        # Create the continue request
        continue_request = models.MultiturnContinueInSchema(test_uuid=test_uuid, answers=formatted_answers)

        response = await continue_multiturn.asyncio_detailed(
            client=self.client,
            body=continue_request,
            continue_eval=continue_test,
        )

        parsed_response = get_parsed_response(response)

        return parsed_response
