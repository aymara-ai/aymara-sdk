# Aymara AI SDK

<!-- sphinx-doc-begin -->

Aymara AI SDK is a Python library for creating, managing, and scoring AI alignment tests. This SDK allows developers to interact with the Aymara AI API to assess the safety and alignment of AI models.

## Features

- Create and manage AI alignment tests
- Score AI model responses
- Support for various AI models (OpenAI, Google's Gemini, Stability AI)
- Asynchronous and synchronous test creation and scoring

## Installation

To install the Aymara AI SDK, run the following command:

```bash
pip install aymara-ai
```

## Configuration

The SDK uses environment variables for configuration. Create a `.env` file in your project root with the following content:

```bash
AYMARA_API_KEY=your_api_key
```

You can also supply the API key directly to the client:

```python
client = AymaraAI(api_key="your_api_key")
```

## Quick Start

Here are quick examples of how to use the Aymara AI SDK, both synchronously and asynchronously:

### Synchronous Example

```python
from sdk import AymaraAI
from your_student_module import YourStudent
from dotenv import load_dotenv

load_dotenv() # If using environment variables

# Initialize the client
client = AymaraAI()

# Create a test synchronously
result = client.create_test(
    test_name="Sample Test",
    student_description="This is a sample description for the student.",
    test_policy="Your safety policy here",
    n_test_questions=2
)

# Get test questions
for i, question in enumerate(result.questions, 1):
    print(f"Question {i}:")
    print(f"UUID: {question.question_uuid}")
    print(f"Text: {question.question_text}")

# Use the questions above to get outputs from your LLM (referred to as student)
student = YourStudent()
student_responses = []
for question in result.questions:
    answer_text = student.answer_question(question=question.question_text)
    student_responses.append({
        "question_uuid": str(question.question_uuid),
        "answer_text": answer_text
    })

# Score the test with your student responses
score_run_response = client.score_test(
    test_uuid=result.test_uuid,
    student_response_json=json.dumps(student_responses)
)

# Print score results
for i, answer in enumerate(score_run_response.answers, 1):
    print(f"Answer {i}:")
    print(f"Question Text: {answer.question_text}")
    print(f"Answer Text: {answer.answer_text}")
    print(f"Is Safe: {answer.is_safe}")
    print(f"Confidence: {answer.confidence}")
    print(f"Explanation: {answer.explanation}")
```

### Asynchronous Example

```python
import asyncio
import json
from dotenv import load_dotenv
from sdk import AymaraAI
from your_student_module import YourStudent # Replace with your actual student implementation

load_dotenv() # If using environment variables
async def main():
    async with AymaraAI() as client:
        # Create a test asynchronously
        result = await client.create_test_async(
            test_name="Sample Test",
            student_description="This is a sample description for the student.",
            test_policy="Your safety policy here",
            n_test_questions=2
        )

        # Wait for the test to be ready
        test = await client.get_test_async(test_uuid=result.test_uuid)
        while test.test_status != "completed":
            await asyncio.sleep(5)
            test = await client.get_test_async(test_uuid=result.test_uuid)

        # Print test questions
        for i, question in enumerate(test.questions, 1):
            print(f"Question {i}:")
            print(f"UUID: {question.question_uuid}")
            print(f"Text: {question.question_text}")

        # Use the questions above to get outputs from your LLM (referred to as student)
        student = YourStudent()
        question_answers = []
        for question in test.questions:
            answer_text = student.answer_question(question=question.question_text)
            question_answers.append({
                "question_uuid": str(question.question_uuid),
                "answer_text": answer_text
            })

        # Score the test asynchronously
        score_run_response = await client.score_test_async(
            test_uuid=result.test_uuid,
            student_response_json=json.dumps(question_answers)
        )


        # Wait for the scores to be ready
        while score_run_response.score_run_status != "completed":
            await asyncio.sleep(5)
            score_run_response = await client.get_score_run_async(
                score_run_uuid=score_run_response.score_run_uuid
            )

        # Print score results
        for i, answer in enumerate(score_run_response.answers, 1):
            print(f"Answer {i}:")
            print(f"Question Text: {answer.question_text}")
print(f"Answer Text: {answer.answer_text}")
print(f"Is Safe: {answer.is_safe}")
            print(f"Confidence: {answer.confidence}")
            print(f"Explanation: {answer.explanation}")

if __name__ == "__main__":
    asyncio.run(main())
```

Both the synchronous and asynchronous methods allow for auomatically waiting for question generation and scoring to complete using the `wait_for_completion` flag.

See the SDK reference for more details.

## License

TODO: Add license

## Support

For support, please contact us at support@aymara.ai or open an issue on our [GitHub repository](https://github.com/aymara-ai/aymara-ai).
