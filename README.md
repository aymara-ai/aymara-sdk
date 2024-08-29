# Aymara Python SDK

<!-- sphinx-doc-begin -->

Hi! 👋 We're [Aymara](https://aymara.ai/).

We help developers measure & improve the alignment of their genAI applications, making genAI safer & more accurate. 

So we built this library for you.

Aymara Python SDK provides convenient access to the Aymara REST API from a Python 3.7+ application. The SDK includes [type definitions](https://github.com/aymara-ai/aymara-ai/blob/main/aymara_sdk/types.py) for requests & responses and offers synchronous & asynchronous clients powered by asyncio.

If you found a bug, have a question, or want to request a feature, say hello at [sdk-support@aymara.ai](mailto:sdk-support@aymara.ai) or [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) on our GitHub repo.

## Documentation

[docs.aymara.ai](http://docs.aymara.ai/) has our full library API. [api.aymara.ai/docs](https://api.aymara.ai/docs) has our REST API documentation.

## Features

Now
- Create safety tests
- Score test answers
- Get and graph test scores
- Asynchronous & synchronous test creation and scoring

Upcoming
- Jailbreak tests
- Hallucination tests
- Text-to-image tests
- AI regulation tests 

## Installation

```bash
pip install aymara-ai
```

## Configuration

The SDK needs to know who you are. Create an `.env` file in your project root with your Aymara API key:

```bash
AYMARA_API_KEY=your_api_key
```

Or supply your key directly to the client:

```python
client = AymaraAI(api_key="your_api_key")
```

## Usage

### Synchronous Example

```python
import json
from sdk import AymaraAI
import MyGenAI  # Replace with your genAI client

# Initialize the client
client = AymaraAI(api_key="your_api_key")

# Create a test synchronously
result = client.create_test(
    test_name="misinformation_test_240824",  # a human-readable name for your test
    student_description="MyGenAI, a chatbot hat answers user questions.",  # a description of your genAI
    test_policy="Do not generate or encourage misinformation: false, inaccurate, or misleading information that is spread without the intent to deceive.",  # the safety policy you want to test
    n_test_questions=20,  # the number of questions in your test
)

# Get test questions
for question in result.questions:
    print(f"UUID: {question.question_uuid}")
    print(f"Text: {question.question_text}")

# Test your genAI (referred to as a student) with your test questions
student_responses = []
for question in result.questions:
    answer_text = MyGenAI.answer_prompt(question.question_text)
    student_responses.append({
        "question_uuid": str(question.question_uuid),
        "answer_text": answer_text
    })

# Score your test answers
score_run_response = client.score_test(
    test_uuid=result.test_uuid,
    student_response_json=json.dumps(student_responses),
)

# View the test answers that did not pass
for answer in score_run_response.answers:
    print(f"Question Text: {answer.question_text}")
    print(f"Answer Text: {answer.answer_text}")
    print(f"Explanation: {answer.explanation}")  # Explanation of why the answer didn't comply with the safety policy
    print(f"Confidence: {answer.confidence}")  # Probability confidence the answer didn't comply with the safety policy

# Get your test's answer pass statistics
AymaraAI.get_pass_stats(score_run_response)

# View your test's answer pass rates in a graph
AymaraAI.graph_pass_rates(score_run_response)
```

### Asynchronous Example

```python
import asyncio
import json
from dotenv import load_dotenv
from sdk import AymaraAI
import YourGenAI  # replace with your actual student implementation

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

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect:

1. Static types without breaking runtime behavior.
2. Library internals that are not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.
3. Virtually no users in practice.

We take backwards-compatibility seriously and will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.7 or higher.

## License

Copyright 2024 Aymara

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.