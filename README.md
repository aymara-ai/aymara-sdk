# Aymara Python SDK

<!-- sphinx-doc-begin -->

Hi! 👋 We're [Aymara](https://aymara.ai/).

We help developers measure & improve the alignment of their genAI applications, making genAI safer & more accurate.

So we built this library for you.

Aymara Python SDK provides convenient access to the Aymara REST API from a Python 3.7+ application. The SDK includes [type definitions](https://github.com/aymara-ai/aymara-ai/blob/main/aymara_sdk/types.py) for requests & responses and offers synchronous & asynchronous clients powered by asyncio.

If you found a bug, have a question, or want to request a feature, say hello at [sdk-support@aymara.ai](mailto:sdk-support@aymara.ai) or [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) on our GitHub repo.

## Documentation

[docs.aymara.ai](http://docs.aymara.ai/) has our full library API.

## Features

Now

- Create safety tests
- Score test answers
- Get and graph test scores
- Summarize and get advice on non-passing test answers
- Asynchronous & synchronous test creation and scoring

Upcoming

- Jailbreak tests
- Hallucination tests
- Text-to-image tests
- AI regulation tests

## Installation

You will need the Aymara GitHub personal access token from your company. Treat the token like a password and never share it or include it in your code. Instead, add it to your .env file:

```bash
export GITHUB_PAT=[GITHUB_PAT]
```

Then, create a virtual environment and install the SDK from GitHub:

```bash
pip install git+https://${GITHUB_PAT}@github.com/aymara-ai/aymara-ai@v0.1.0
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

In this repo, refer to `/examples/safety/safety_notebook.ipynb` for a walkthrough of how to use the SDK.

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect:

1. Static types without breaking runtime behavior.
2. Library internals that are not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.
3. Virtually no users in practice.

We take backwards-compatibility seriously and will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.7 or higher.
