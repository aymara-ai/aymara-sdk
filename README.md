# Aymara AI SDK

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

Here's a quick example of how to use the Aymara AI SDK:

```python
from sdk import AymaraAI
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

# Score the test with your student responses
score_run_response = client.score_test(
    test_uuid=result.test_uuid,
    student_response_json=json.dumps(question_answers)
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

## License

TODO: Add license

## Support

For support, please contact us at support@aymara.ai or open an issue on our [GitHub repository](https://github.com/aymara-ai/aymara-ai).
