import asyncio
import time
from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import (
    upload_user_test,
    get_test,
    get_test_questions,
    delete_test,
)
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    
    BadExample,
    BaseTestResponse,
    GoodExample,
    
    Status,
)
from aymara_ai.utils.constants import (
    DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_MAX_TOKENS,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
)


class UploadUserTestMixin(AymaraAIProtocol):
    def _upload_user_test(
        self,
        test_name: str,
        student_description: str,
        is_async: bool,
        test_type: TestType,
        test_language: str,
        questions: List[dict],
        test_system_prompt: Optional[str],
        test_policy: Optional[str],
        knowledge_base: Optional[str],
        max_wait_time_secs: Optional[int],
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        """
        Generic method to upload user test.
        """

        self._validate_test_inputs(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=len(questions),
            test_type=test_type,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
        )
        
        self._validate_test_questions(
            questions=questions,
            test_type=test_type,
        )
        examples = []
        if good_examples:
            examples.extend([ex.to_example_in_schema() for ex in good_examples])
        if bad_examples:
            examples.extend([ex.to_example_in_schema() for ex in bad_examples])
        
        # Create TestInSchema object first
        test_data = models.TestInSchema(
            test_name=test_name,
            student_description=student_description,
            test_type=test_type,
            test_language=test_language,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            additional_instructions=additional_instructions,
            test_examples=examples if examples else None,
        )

        # Create QuestionInSchema objects
        question_objects = [
            models.QuestionInSchema(question_text=q["question_text"]) 
            for q in questions
        ]
        # Create the final TestWithQuestionsInSchema object
        user_test_data = models.TestWithQuestionsInSchema(
            test=test_data,
            questions=question_objects
        )

        if is_async:
            return self._upload_and_wait_for_test_impl_async(user_test_data, max_wait_time_secs)
        else:
            return self._upload_and_wait_for_test_impl_sync(user_test_data, max_wait_time_secs)

    def upload_safety_test(
        self,
        test_name: str,
        test_policy: str,
        questions: List[dict],
        student_description: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        max_wait_time_secs: int = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
    ) -> str:
        return self._upload_user_test(
            test_name=test_name,
            test_language=test_language,
            test_policy=test_policy,
            test_type=TestType.SAFETY,
            questions=questions,
            student_description=student_description,
            max_wait_time_secs=max_wait_time_secs,
            is_async=False,
            additional_instructions=additional_instructions,
            test_system_prompt=None,
            knowledge_base=None,
        )

    upload_safety_test.__doc__ = f"""
        Upload a safety test to evaluate an AI model's adherence to safety policies.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param test_policy: The safety policy that the model should follow.
        :type test_policy: str
        :param questions: List of questions to test the model. Each question should be a dict with "question_text" key and str value
        :type questions: List[dict]
        :param student_description: Description of the AI model being tested.
        :type student_description: str
        :param test_language: Language of the test. Defaults to English.
        :type test_language: str
        :param max_wait_time_secs: Maximum time in seconds to wait for test results.
            Defaults to DEFAULT_SAFETY_MAX_WAIT_TIME_SECS.
        :type max_wait_time_secs: int
        :param additional_instructions: Optional additional instructions for the test that were added by the user.
        :type additional_instructions: str
        :return: SafetyTestResponse object containing the test results.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety test.
        :raises ValueError: If the test_language is not supported.
        :raises ValueError: If the max_wait_time_secs is not positive.
        :raises ValueError: If the questions are not provided.
        :raises ValueError: If the student_description is not provided.
        :raises ValueError: If the test_name is not provided.
        """

    # def upload_accuracy_test(
    #     self,
    #     test_name: str,
    #     questions: List[dict],
    #     test_language: str = DEFAULT_TEST_LANGUAGE,
    #     max_wait_time_secs: int = DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
    #     additional_instructions: Optional[str] = None,
    # ) -> AccuracyTestResponse:
    #     return self._upload_user_test(
    #         test_name=test_name,
    #         questions=questions,
    #         test_language=test_language,
    #         test_type=TestType.ACCURACY,
    #         max_wait_time_secs=max_wait_time_secs,
    #         is_async=False,
    #         additional_instructions=additional_instructions,
    #     )

    # def upload_jailbreak_test(
    #     self,
    #     test_name: str,
    #     questions: List[dict],
    #     test_language: str = DEFAULT_TEST_LANGUAGE,
    #     max_wait_time_secs: int = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    #     additional_instructions: Optional[str] = None,
    # ) -> JailbreakTestResponse:
    #     return self._upload_user_test(
    #         test_name=test_name,
    #         questions=questions,
    #         test_language=test_language,
    #         test_type=TestType.JAILBREAK,
    #         max_wait_time_secs=max_wait_time_secs,
    #         is_async=False,
    #         additional_instructions=additional_instructions,
    #     )

    async def upload_safety_test_async(
        self,
        test_name: str,
        questions: List[dict],
        test_language: str = DEFAULT_TEST_LANGUAGE,
        additional_instructions: Optional[str] = None,
    ) -> BaseTestResponse:
        return await self._upload_user_test(
            test_name=test_name,
            questions=questions,
            test_language=test_language,
            test_type=TestType.SAFETY,
            max_wait_time_secs=0,
            is_async=True,
            additional_instructions=additional_instructions,
        )

    # async def upload_accuracy_test_async(
    #     self,
    #     test_name: str,
    #     questions: List[dict],
    #     test_language: str = DEFAULT_TEST_LANGUAGE,
    #     additional_instructions: Optional[str] = None,
    # ) -> AccuracyTestResponse:
    #     return await self._upload_user_test(
    #         test_name=test_name,
    #         questions=questions,
    #         test_language=test_language,
    #         test_type=TestType.ACCURACY,
    #         max_wait_time_secs=0,
    #         is_async=True,
    #         additional_instructions=additional_instructions,
    #     )

    # async def upload_jailbreak_test_async(
    #     self,
    #     test_name: str,
    #     questions: List[dict],
    #     test_language: str = DEFAULT_TEST_LANGUAGE,
    #     additional_instructions: Optional[str] = None,
    # ) -> JailbreakTestResponse:
    #     return await self._upload_user_test(
    #         test_name=test_name,
    #         questions=questions,
    #         test_language=test_language,
    #         test_type=TestType.JAILBREAK,
    #         max_wait_time_secs=0,
    #         is_async=True,
    #         additional_instructions=additional_instructions,
    #     )

    def _validate_test_inputs(
        self,
        test_name: str,
        student_description: str,
        test_policy: Optional[str],
        test_system_prompt: Optional[str],
        knowledge_base: Optional[str],
        test_language: str,
        num_test_questions: Optional[int],
        test_type: TestType,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
    ) -> None:
        if not student_description:
            raise ValueError("student_description is required")

        if test_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"test_language must be one of {SUPPORTED_LANGUAGES}")

        if (
            test_type == TestType.SAFETY or test_type == TestType.IMAGE_SAFETY
        ) and test_policy is None:
            raise ValueError("test_policy is required for safety test")

        if test_type == TestType.JAILBREAK and test_system_prompt is None:
            raise ValueError("test_system_prompt is required for jailbreak test")

        if test_type == TestType.ACCURACY and knowledge_base is None:
            raise ValueError("knowledge_base is required for accuracy test")

        if (
            len(test_name) < DEFAULT_TEST_NAME_LEN_MIN
            or len(test_name) > DEFAULT_TEST_NAME_LEN_MAX
        ):
            raise ValueError(
                f"test_name must be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters"
            )

        if num_test_questions is not None:
            if test_type == TestType.JAILBREAK and num_test_questions < 1:
                raise ValueError("limit_num_questions must be at least one question")
            elif test_type != TestType.JAILBREAK and not (
                DEFAULT_NUM_QUESTIONS_MIN
                <= num_test_questions
                <= DEFAULT_NUM_QUESTIONS_MAX
            ):
                raise ValueError(
                    f"num_test_questions must be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions"
                )

        token1 = len(student_description) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER

        token_2_field = (
            "test_policy"
            if test_type == TestType.SAFETY or test_type == TestType.IMAGE_SAFETY
            else "test_system_prompt"
            if test_type == TestType.JAILBREAK
            else "knowledge_base"
        )
        token2 = (
            len(test_policy) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if test_type == TestType.SAFETY or test_type == TestType.IMAGE_SAFETY
            else len(test_system_prompt) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            if test_type == TestType.JAILBREAK
            else len(knowledge_base) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
        )

        total_tokens = token1 + token2
        if total_tokens > DEFAULT_MAX_TOKENS:
            raise ValueError(
                f"student_description is ~{token1:,} tokens and {token_2_field} is ~{token2:,} tokens. They are ~{total_tokens:,} tokens in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
            )

        if additional_instructions is not None:
            token3 = len(additional_instructions) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"student_description is ~{token1:,} tokens, {token_2_field} is ~{token2:,} tokens, "
                    f"and additional_instructions is ~{token3:,} tokens. They are ~{total_tokens:,} tokens "
                    f"in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
                )

            if len(additional_instructions) > MAX_ADDITIONAL_INSTRUCTIONS_LENGTH:
                raise ValueError(
                    f"additional_instructions must be less than {MAX_ADDITIONAL_INSTRUCTIONS_LENGTH} characters"
                )

        if good_examples is not None or bad_examples is not None:
            # Validate example types separately
            for example in good_examples or bad_examples:
                if not isinstance(example, (GoodExample, BadExample)):
                    raise ValueError(
                        "examples must be instances of GoodExample or BadExample"
                    )

            if len(good_examples or bad_examples) > MAX_EXAMPLES_LENGTH:
                raise ValueError(
                    f"examples must be less than {MAX_EXAMPLES_LENGTH} examples"
                )

        # Add knowledge_base to token calculation if it exists
        if knowledge_base is not None:
            token3 = len(knowledge_base) * DEFAULT_CHAR_TO_TOKEN_MULTIPLIER
            total_tokens = token1 + token2 + token3

            if total_tokens > DEFAULT_MAX_TOKENS:
                raise ValueError(
                    f"student_description is ~{token1:,} tokens, {token_2_field} is ~{token2:,} tokens, "
                    f"and knowledge_base is ~{token3:,} tokens. They are ~{total_tokens:,} tokens "
                    f"in total but they should be less than {DEFAULT_MAX_TOKENS:,} tokens."
                )

    def _validate_test_questions(
        self,
        questions: List[dict],
        test_type: TestType,
    ) -> None:
        """
        Validate test questions to ensure they have required fields.
        """
        if not questions:
            raise ValueError("questions list cannot be empty")

        for i, question in enumerate(questions):
            if not isinstance(question, dict):
                raise ValueError(f"Question at index {i} must be a dictionary")
                
            if "question_text" not in question:
                raise ValueError(f"Question at index {i} is missing required field 'question_text'")
            
            if not isinstance(question["question_text"], str):
                raise ValueError(f"Question text at index {i} must be a string")
            
            if not question["question_text"].strip():
                raise ValueError(f"Question text at index {i} cannot be empty")

    def _upload_and_wait_for_test_impl_sync(
        self, test_data: models.TestWithQuestionsInSchema, max_wait_time_secs: Optional[int]
    ) -> BaseTestResponse:
        print("Uploading test...", test_data)
        start_time = time.time()
        
        response = upload_user_test.sync_detailed(
            client=self.client, body=test_data
        )
        print("Response...", response)
        create_response = response.parsed

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name
        
        with self.logger.progress_bar(
            test_name, 
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                response = get_test.sync_detailed(
                    client=self.client, test_uuid=test_uuid
                  )

                if response.status_code == 404:
                    raise ValueError(f"Test with UUID {test_uuid} not found")

                test_response = response.parsed

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                  test_response.test_status = models.TestStatus.FAILED
                  self.logger.update_progress_bar(test_uuid, Status.FAILED)
                  return BaseTestResponse.from_test_out_schema_and_questions(
                    test_response, None, "Test creation timed out"
                  )

                if test_response.test_status == models.TestStatus.FAILED:
                  failure_reason = "Internal server error, please try again."
                  return BaseTestResponse.from_test_out_schema_and_questions( 
                    test_response, None, failure_reason
                  )

                if test_response.test_status == models.TestStatus.FINISHED:
                  questions = self._get_all_questions_sync(test_uuid)
                  return BaseTestResponse.from_test_out_schema_and_questions(
                    test_response, questions, None
                  )

                time.sleep(POLLING_INTERVAL)


    async def _upload_and_wait_for_test_impl_async(
        self, test_data: models.TestWithQuestionsInSchema, max_wait_time_secs: Optional[int]
    ) -> BaseTestResponse:
        start_time = time.time()
  
        response = await upload_user_test.asyncio_detailed(
            client=self.client, body=test_data
        )
        create_response = response.parsed

        if response.status_code == 422:
            raise ValueError(f"{create_response.detail}")

        test_uuid = create_response.test_uuid
        test_name = create_response.test_name
        
        with self.logger.progress_bar(
            test_name, 
            test_uuid,
            Status.from_api_status(create_response.test_status),
        ):
            while True:
                response = get_test.asyncio_detailed(
                    client=self.client,
                    test_uuid=test_uuid,
                )

                if response.status_code == 404:
                    raise ValueError(f"Test with UUID {test_uuid} not found")

                test_response = response.parsed

                self.logger.update_progress_bar(
                    test_uuid,
                    Status.from_api_status(test_response.test_status),
                )

                elapsed_time = time.time() - start_time

                if elapsed_time > max_wait_time_secs:
                  test_response.test_status = models.TestStatus.FAILED
                  self.logger.update_progress_bar(test_uuid, Status.FAILED)
                  return BaseTestResponse.from_test_out_schema_and_questions(
                    test_response, None, "Test creation timed out"
                  )

                if test_response.test_status == models.TestStatus.FAILED:
                  failure_reason = "Internal server error, please try again."
                  return BaseTestResponse.from_test_out_schema_and_questions(
                    test_response, None, failure_reason
                  )

                if test_response.test_status == models.TestStatus.FINISHED:
                  questions = await self._get_all_questions_async(test_uuid)
                  return BaseTestResponse.from_test_out_schema_and_questions(
                    test_response, questions, None
                  )

                await asyncio.sleep(POLLING_INTERVAL)



    # Helper Methods
    def _get_all_questions_sync(self, test_uuid: str) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = get_test_questions.sync_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            questions.extend(paged_response.items)
            if len(questions) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return questions

    async def _get_all_questions_async(
        self, test_uuid: str
    ) -> List[models.QuestionSchema]:
        questions = []
        offset = 0
        while True:
            response = await get_test_questions.asyncio_detailed(
                client=self.client, test_uuid=test_uuid, offset=offset
            )
            if response.status_code == 404:
                raise ValueError(f"Test with UUID {test_uuid} not found")

            paged_response = response.parsed
            questions.extend(paged_response.items)
            if len(questions) >= paged_response.count:
                break
            offset += len(paged_response.items)
        return questions

    def delete_test(self, test_uuid: str) -> None:
        """
        Delete a test synchronously.
        """
        response = delete_test.sync_detailed(client=self.client, test_uuid=test_uuid)
        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")

    async def delete_test_async(self, test_uuid: str) -> None:
        """
        Delete a test asynchronously.
        """
        response = await delete_test.asyncio_detailed(
            client=self.client, test_uuid=test_uuid
        )
        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        if response.status_code == 422:
            raise ValueError(f"{response.parsed.detail}")