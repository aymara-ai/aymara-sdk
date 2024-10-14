"""Students are the models that take tests."""

import asyncio
import os
from typing import Optional

from openai import OpenAI

from aymara_ai.types import StudentAnswerInput


class OpenAIStudent:
    """OpenAI API student."""

    def __init__(self, model="gpt-4o-mini", api_key=None):
        self.model = model
        if api_key is None:
            api_key = os.environ.get("OPENAI_KEY")
        self.client = OpenAI(api_key=api_key)

    def answer_question(self, question: str, system_prompt: Optional[str]) -> str:
        """Answer a test question."""

        messages = [{"role": "user", "content": question}]
        if system_prompt is not None:
            messages = [{"role": "system", "content": system_prompt}] + messages

        completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )

        return completion.choices[0].message.content

    async def get_student_answer(self, question, system_prompt):
        answer_text = await asyncio.to_thread(
            self.answer_question, question.question_text, system_prompt
        )
        return StudentAnswerInput(
            question_uuid=question.question_uuid, answer_text=answer_text
        )

    async def get_all_student_answers(self, questions, system_prompt):
        return await asyncio.gather(
            *[
                self.get_student_answer(question, system_prompt)
                for question in questions
            ]
        )

    async def answer_test_questions(self, tests, system_prompts=None):
        if system_prompts is None:
            system_prompts = [None] * len(tests)

        all_student_answers = await asyncio.gather(
            *[
                self.get_all_student_answers(test.questions, system_prompt)
                for test, system_prompt in zip(tests, system_prompts)
            ]
        )

        student_answers_dict = {}
        for test, student_answers in zip(tests, all_student_answers):
            student_answers_dict[test.test_uuid] = student_answers

        return student_answers_dict
