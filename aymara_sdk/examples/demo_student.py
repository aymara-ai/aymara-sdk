"""Students are the models that take tests."""

import os
import asyncio
from openai import OpenAI

from aymara_sdk.types import StudentAnswerInput

class OpenAIStudent:
    """OpenAI API student."""

    def __init__(self, model="gpt-4o-mini", api_key=None):
        self.model = model
        if api_key is None:
            api_key=os.environ.get("OPENAI_KEY")
        self.client = OpenAI(api_key=api_key)

    def answer_question(self, question: str) -> str:
        """Answer a test question."""
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": question}],
            model=self.model,
        )

        return completion.choices[0].message.content

    async def get_student_answer(self, question):
        answer_text = await asyncio.to_thread(self.answer_question, question.question_text)
        return StudentAnswerInput(question_uuid=question.question_uuid, answer_text=answer_text)

    async def get_all_student_answers(self, questions):
        return await asyncio.gather(*[self.get_student_answer(question) for question in questions])

    async def process_tests(self, tests):
        all_student_answers = await asyncio.gather(*[self.get_all_student_answers(test.questions) for test in tests])
        
        student_answers_dict = {}
        for test, student_answers in zip(tests, all_student_answers):
            student_answers_dict[test.test_uuid] = student_answers
        
        return student_answers_dict
    