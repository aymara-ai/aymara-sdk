import asyncio
import time
from typing import Coroutine, List, Optional, Union

from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.generated.aymara_api_client import models
from aymara_ai.generated.aymara_api_client.api.tests import (
    create_test,
    delete_test,
    get_test,
    get_test_questions,
    list_tests,
)
from aymara_ai.generated.aymara_api_client.models.test_type import TestType
from aymara_ai.types import (
    AccuracyTestResponse,
    BadExample,
    BaseTestResponse,
    GoodExample,
    JailbreakTestResponse,
    ListTestResponse,
    SafetyTestResponse,
    Status,
)
from aymara_ai.utils.constants import (
    DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
    DEFAULT_ACCURACY_NUM_QUESTIONS,
    DEFAULT_CHAR_TO_TOKEN_MULTIPLIER,
    DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_NUM_QUESTIONS,
    DEFAULT_NUM_QUESTIONS_MAX,
    DEFAULT_NUM_QUESTIONS_MIN,
    DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
    DEFAULT_TEST_LANGUAGE,
    DEFAULT_TEST_NAME_LEN_MAX,
    DEFAULT_TEST_NAME_LEN_MIN,
    MAX_ADDITIONAL_INSTRUCTIONS_LENGTH,
    MAX_EXAMPLES_LENGTH,
    POLLING_INTERVAL,
    SUPPORTED_LANGUAGES,
)


class TestMixin(AymaraAIProtocol):
    # Create Safety Test Methods
    def create_safety_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: int = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
    ) -> SafetyTestResponse:
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=None,
            knowledge_base=None,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=False,
            test_type=TestType.SAFETY,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_safety_test.__doc__ = f"""
        Create an Aymara safety test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """

    async def create_safety_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
    ) -> SafetyTestResponse:
        return await self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=None,
            knowledge_base=None,
            test_language=test_language,
            num_test_questions=num_test_questions,
            is_async=True,
            test_type=TestType.SAFETY,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_safety_test_async.__doc__ = f"""
        Create an Aymara safety test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """

    # Create Jailbreak Test Methods
    def create_jailbreak_test(
        self,
        test_name: str,
        student_description: str,
        test_system_prompt: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        max_wait_time_secs: int = DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        limit_num_questions: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> JailbreakTestResponse:
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=None,
            test_system_prompt=test_system_prompt,
            knowledge_base=None,
            test_language=test_language,
            is_async=False,
            test_type=TestType.JAILBREAK,
            num_test_questions=limit_num_questions,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_jailbreak_test.__doc__ = f"""
        Create an Aymara jailbreak test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_system_prompt: System prompt of the jailbreak test.
        :type test_system_prompt: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :param limit_num_questions: Optional limit on the number of questions generated
        :type limit_num_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: JailbreakTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """

    async def create_jailbreak_test_async(
        self,
        test_name: str,
        student_description: str,
        test_system_prompt: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        max_wait_time_secs: int = DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        limit_num_questions: Optional[int] = None,
        is_sandbox: Optional[bool] = False,
    ) -> JailbreakTestResponse:
        return await self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=None,
            test_system_prompt=test_system_prompt,
            knowledge_base=None,
            test_language=test_language,
            is_async=True,
            test_type=TestType.JAILBREAK,
            num_test_questions=limit_num_questions,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_jailbreak_test_async.__doc__ = f"""
        Create an Aymara jailbreak test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_system_prompt: System prompt of the jailbreak test.
        :type test_system_prompt: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_JAILBREAK_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :param limit_num_questions: Optional limit on the number of questions generated
        :type limit_num_questions: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: JailbreakTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_system_prompt is not provided for jailbreak tests.
        """

    def create_image_safety_test(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
    ):
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            is_async=False,
            test_system_prompt=None,
            knowledge_base=None,
            test_language=test_language,
            test_type=TestType.IMAGE_SAFETY,
            num_test_questions=num_test_questions,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_image_safety_test.__doc__ = f"""
        Create an Aymara image safety test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """

    async def create_image_safety_test_async(
        self,
        test_name: str,
        student_description: str,
        test_policy: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions: int = DEFAULT_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = DEFAULT_SAFETY_MAX_WAIT_TIME_SECS,
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
    ):
        return await self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            is_async=True,
            test_system_prompt=None,
            knowledge_base=None,
            test_language=test_language,
            test_type=TestType.IMAGE_SAFETY,
            num_test_questions=num_test_questions,
            max_wait_time_secs=max_wait_time_secs,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
            is_sandbox=is_sandbox,
        )

    create_image_safety_test_async.__doc__ = f"""
        Create an Aymara image safety test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param test_policy: Policy of the test, which will measure compliance against this policy (required for safety tests).
        :type test_policy: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions: Number of test questions, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_SAFETY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :param additional_instructions: Optional additional instructions for test generation
        :type additional_instructions: str, optional
        :param good_examples: Optional list of good examples to guide question generation
        :type good_examples: List[GoodExample], optional
        :param bad_examples: Optional list of bad examples to guide question generation
        :type bad_examples: List[BadExample], optional
        :return: Test response containing test details and generated questions.
        :rtype: SafetyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If test_policy is not provided for safety tests.
        """

    def create_accuracy_test(
        self,
        test_name: str,
        student_description: str,
        knowledge_base: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions_per_question_type: int = DEFAULT_ACCURACY_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
        is_sandbox: Optional[bool] = False,
    ) -> AccuracyTestResponse:
        return self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=None,
            test_system_prompt=None,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions_per_question_type,
            is_async=False,
            test_type=TestType.ACCURACY,
            max_wait_time_secs=max_wait_time_secs,
            is_sandbox=is_sandbox,
        )

    create_accuracy_test.__doc__ = f"""
        Create an Aymara accuracy test synchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param knowledge_base: Knowledge base text that will be used to generate accuracy test questions.
        :type knowledge_base: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions_per_question_type: Number of test questions per question type, defaults to {DEFAULT_ACCURACY_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions_per_question_type: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: AccuracyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If knowledge_base is not provided for accuracy tests.
        """

    async def create_accuracy_test_async(
        self,
        test_name: str,
        student_description: str,
        knowledge_base: str,
        test_language: str = DEFAULT_TEST_LANGUAGE,
        num_test_questions_per_question_type: int = DEFAULT_ACCURACY_NUM_QUESTIONS,
        max_wait_time_secs: Optional[int] = DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS,
        is_sandbox: Optional[bool] = False,
    ) -> AccuracyTestResponse:
        return await self._create_test(
            test_name=test_name,
            student_description=student_description,
            test_policy=None,
            test_system_prompt=None,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions_per_question_type,
            is_async=True,
            test_type=TestType.ACCURACY,
            max_wait_time_secs=max_wait_time_secs,
            is_sandbox=is_sandbox,
        )

    create_accuracy_test_async.__doc__ = f"""
        Create an Aymara accuracy test asynchronously and wait for completion.

        :param test_name: Name of the test. Should be between {DEFAULT_TEST_NAME_LEN_MIN} and {DEFAULT_TEST_NAME_LEN_MAX} characters.
        :type test_name: str
        :param student_description: Description of the AI that will take the test (e.g., its purpose, expected use, typical user). The more specific your description is, the less generic the test questions will be.
        :type student_description: str
        :param knowledge_base: Knowledge base text that will be used to generate accuracy test questions.
        :type knowledge_base: str
        :param test_language: Language of the test, defaults to {DEFAULT_TEST_LANGUAGE}.
        :type test_language: str, optional
        :param num_test_questions_per_question_type: Number of test questions per question type, defaults to {DEFAULT_NUM_QUESTIONS}. Should be between {DEFAULT_NUM_QUESTIONS_MIN} and {DEFAULT_NUM_QUESTIONS_MAX} questions.
        :type num_test_questions_per_question_type: int, optional
        :param max_wait_time_secs: Maximum wait time for test creation, defaults to {DEFAULT_ACCURACY_MAX_WAIT_TIME_SECS} seconds.
        :type max_wait_time_secs: int, optional
        :return: Test response containing test details and generated questions.
        :rtype: AccuracyTestResponse

        :raises ValueError: If the test_name length is not within the allowed range.
        :raises ValueError: If num_test_questions is not within the allowed range.
        :raises ValueError: If knowledge_base is not provided for accuracy tests.
        """

    def _create_test(
        self,
        test_name: str,
        student_description: str,
        is_async: bool,
        test_type: TestType,
        test_language: str,
        test_system_prompt: Optional[str],
        test_policy: Optional[str],
        knowledge_base: Optional[str],
        num_test_questions: Optional[int],
        max_wait_time_secs: Optional[int],
        additional_instructions: Optional[str] = None,
        good_examples: Optional[List[GoodExample]] = None,
        bad_examples: Optional[List[BadExample]] = None,
        is_sandbox: Optional[bool] = False,
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        self._validate_test_inputs(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=test_type,
            additional_instructions=additional_instructions,
            good_examples=good_examples,
            bad_examples=bad_examples,
        )

        examples = []
        if good_examples:
            examples.extend([ex.to_example_in_schema() for ex in good_examples])
        if bad_examples:
            examples.extend([ex.to_example_in_schema() for ex in bad_examples])

        test_data = models.TestInSchema(
            test_name=test_name,
            student_description=student_description,
            test_policy=test_policy,
            test_system_prompt=test_system_prompt,
            knowledge_base=knowledge_base,
            test_language=test_language,
            num_test_questions=num_test_questions,
            test_type=test_type,
            additional_instructions=additional_instructions,
            test_examples=examples if examples else None,
        )

        if is_async:
            return self._create_and_wait_for_test_impl_async(
                test_data, max_wait_time_secs, is_sandbox
            )
        else:
            return self._create_and_wait_for_test_impl_sync(
                test_data, max_wait_time_secs, is_sandbox
            )

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
            raise ValueError("test_policy is required for safety tests")

        if test_type == TestType.JAILBREAK and test_system_prompt is None:
            raise ValueError("test_system_prompt is required for jailbreak tests")

        if test_type == TestType.ACCURACY and knowledge_base is None:
            raise ValueError("knowledge_base is required for accuracy tests")

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

    def _create_and_wait_for_test_impl_sync(
        self,
        test_data: models.TestInSchema,
        max_wait_time_secs: Optional[int],
        is_sandbox: Optional[bool] = None,
    ) -> BaseTestResponse:
        start_time = time.time()
        response = create_test.sync_detailed(
            client=self.client, body=test_data, is_sandbox=is_sandbox
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

    async def _create_and_wait_for_test_impl_async(
        self,
        test_data: models.TestInSchema,
        max_wait_time_secs: Optional[int],
        is_sandbox: Optional[bool] = None,
    ) -> BaseTestResponse:
        start_time = time.time()
        response = await create_test.asyncio_detailed(
            client=self.client, body=test_data, is_sandbox=is_sandbox
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
                response = await get_test.asyncio_detailed(
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
                    questions = await self._get_all_questions_async(test_uuid)
                    return BaseTestResponse.from_test_out_schema_and_questions(
                        test_response, questions, None
                    )

                await asyncio.sleep(POLLING_INTERVAL)

    # Get Test Methods
    def get_test(self, test_uuid: str) -> BaseTestResponse:
        """
        Get the current status of a test synchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: TestResponse
        """
        return self._get_test(test_uuid, is_async=False)

    async def get_test_async(self, test_uuid: str) -> BaseTestResponse:
        """
        Get the current status of a test asynchronously, and questions if it is completed.

        :param test_uuid: UUID of the test.
        :type test_uuid: str
        :return: Test response.
        :rtype: TestResponse
        """
        return await self._get_test(test_uuid, is_async=True)

    def _get_test(
        self, test_uuid: str, is_async: bool
    ) -> Union[BaseTestResponse, Coroutine[BaseTestResponse, None, None]]:
        if is_async:
            return self._get_test_async_impl(test_uuid)
        else:
            return self._get_test_sync_impl(test_uuid)

    def _get_test_sync_impl(self, test_uuid: str) -> BaseTestResponse:
        response = get_test.sync_detailed(client=self.client, test_uuid=test_uuid)

        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        test_response = response.parsed
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = self._get_all_questions_sync(test_uuid)

        return BaseTestResponse.from_test_out_schema_and_questions(
            test_response, questions
        )

    async def _get_test_async_impl(self, test_uuid: str) -> BaseTestResponse:
        response = await get_test.asyncio_detailed(
            client=self.client, test_uuid=test_uuid
        )

        if response.status_code == 404:
            raise ValueError(f"Test with UUID {test_uuid} not found")

        test_response = response.parsed
        questions = None
        if test_response.test_status == models.TestStatus.FINISHED:
            questions = await self._get_all_questions_async(test_uuid)

        return BaseTestResponse.from_test_out_schema_and_questions(
            test_response, questions
        )

    # List Tests Methods
    def list_tests(self) -> ListTestResponse:
        """
        List all tests synchronously.
        """
        tests = self._list_tests_sync_impl()

        return ListTestResponse(tests)

    async def list_tests_async(self) -> ListTestResponse:
        """
        List all tests asynchronously.
        """
        tests = await self._list_tests_async_impl()

        return ListTestResponse(tests)

    def _list_tests_sync_impl(self) -> List[BaseTestResponse]:
        all_tests = []
        offset = 0
        while True:
            response = list_tests.sync_detailed(client=self.client, offset=offset)

            paged_response = response.parsed
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            BaseTestResponse.from_test_out_schema_and_questions(test)
            for test in all_tests
        ]

    async def _list_tests_async_impl(self) -> List[BaseTestResponse]:
        all_tests = []
        offset = 0
        while True:
            response = await list_tests.asyncio_detailed(
                client=self.client, offset=offset
            )

            paged_response = response.parsed
            all_tests.extend(paged_response.items)
            if len(all_tests) >= paged_response.count:
                break
            offset += len(paged_response.items)

        return [
            BaseTestResponse.from_test_out_schema_and_questions(test)
            for test in all_tests
        ]

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
