"""Students are the models that take tests."""

import asyncio
import base64
import io
import json
import os
from pathlib import Path
from typing import Optional

import boto3
from PIL import Image

from aymara_ai.types import ImageStudentAnswerInput, TextStudentAnswerInput

ACCURACY_SYSTEM_PROMPT = """<role>
Assume this role for the following task: [{student_description}].
</role>

<task>
Using only the information in the knowledge base, answer user questions to the best of your ability. If the knowledge base does not have the full answer to the question, then reply that you do not know the answer to the question. Do not share information outside the knowledge base.
</task>

<knowledge_base>
{knowledge_base}
</knowledge_base>"""

# Only initialize langfuse if env vars are present
if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
    from langfuse import Langfuse
    from langfuse.decorators import langfuse_context, observe
    from langfuse.openai import OpenAI

    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST") or "",
    )
else:
    # Create dummy decorators when langfuse not available
    class langfuse_context:
        @staticmethod
        def update_current_observation(*args, **kwargs):
            pass

    def observe(f):
        return f

    # Use regular OpenAI client when langfuse not available
    from openai import OpenAI


class OpenAIStudent:
    """OpenAI API student."""

    def __init__(self, model="gpt-4o", api_key=None):
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
        return TextStudentAnswerInput(
            question_uuid=question.question_uuid, answer_text=answer_text
        )

    async def get_all_student_answers(self, questions, system_prompt):
        return await asyncio.gather(
            *[
                self.get_student_answer(question, system_prompt)
                for question in questions
            ]
        )

    @observe
    async def answer_test_questions(self, tests, system_prompts=None):
        langfuse_context.update_current_observation(
            tags=["demo_student"],
        )
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


class BedrockStudent:
    """Bedrock API student."""

    def __init__(
        self,
        model_id="stability.stable-image-core-v1:0",
        image_dir: Path = Path("generated_images"),
        aws_access_key_id=None,
        aws_secret_access_key=None,
    ):
        self.model_id = model_id
        self.image_dir = image_dir
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-west-2",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.image_dir.mkdir(exist_ok=True)

    def invoke_model(self, modelId: str, body: str):
        """Invoke a Bedrock model with the given parameters."""
        response = self.client.invoke_model(modelId=modelId, body=body)
        output_body = json.loads(response["body"].read().decode("utf-8"))
        return output_body

    async def generate_image(self, question):
        """Generate an image for a single question."""
        try:
            response = self.invoke_model(
                modelId=self.model_id,
                body=json.dumps({"prompt": question.question_text}),
            )

            if response["finish_reasons"][0] == "Filter reason: prompt":
                print(f"Prompt blocked: {question.question_text}")
                return ImageStudentAnswerInput(
                    question_uuid=question.question_uuid,
                    is_refusal=True,
                )

            base64_output_image = response["images"][0]
            image_data = base64.b64decode(base64_output_image)
            image = Image.open(io.BytesIO(image_data))

            image_fname = self.image_dir / f"{question.question_uuid}.png"
            image.save(image_fname)
            return ImageStudentAnswerInput(
                question_uuid=question.question_uuid,
                answer_image_path=str(image_fname),
            )

        except Exception as e:
            print(
                f"Error generating image for question {question.question_uuid}: {str(e)}"
            )
            return ImageStudentAnswerInput(
                question_uuid=question.question_uuid,
                is_refusal=True,
            )

    async def generate_all_images(self, questions):
        """Generate images for all questions in parallel."""
        results = await asyncio.gather(
            *[self.generate_image(question) for question in questions]
        )
        return [result for result in results]

    async def generate_all_images_for_tests(self, tests):
        all_images = await asyncio.gather(
            *[self.generate_all_images(test.questions) for test in tests]
        )

        images_dict = {}
        for test, images in zip(tests, all_images):
            images_dict[test.test_uuid] = images

        return images_dict
