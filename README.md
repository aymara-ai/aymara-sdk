# Aymara Python SDK

<!-- sphinx-doc-begin -->

Hi! 👋 We're [Aymara](https://aymara.ai).

We help developers measure & improve the alignment of their genAI applications, making genAI safer & more accurate.

So we built this library for you.

Our Python SDK provides convenient access to the Aymara REST API from Python 3.9+. The SDK includes type definitions for requests & responses and offers synchronous & asynchronous clients powered by asyncio.

Access our API with a [free trial](https://aymara.ai/free-trial) or [upgrade](https://aymara.ai/upgrade) for access to full funcionality.

If you found a bug, have a question, or want to request a feature, say hello at [support@aymara.ai](mailto:support@aymara.ai) or [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) on our GitHub repo.

<!-- sphinx-ignore-start -->

## Documentation

[docs.aymara.ai/sdk_reference](https://docs.aymara.ai/sdk_reference.html) has our full library API.

<!-- sphinx-ignore-end -->

## Features

Now

- Create safety & jailbreak tests
- Score test answers
- Get and graph test scores
- Summarize and get advice on non-passing test answers
- Asynchronous & synchronous test creation and scoring

Upcoming

- Hallucination tests
- Text-to-image tests
- AI regulation tests

## Installation

Install the SDK with pip. We suggest using a virtual environment to manage dependencies.

```bash
pip install aymara-ai
```

## Configuration

The SDK needs to know who you are. Create an env variable with your Aymara API key:

```bash
export AYMARA_API_KEY=[AYMARA_API_KEY]
```

Or supply your key directly to the client:

```python
client = AymaraAI(api_key="your_api_key")
```

<!-- sphinx-ignore-start -->

## Usage

Refer to [this notebook](https://docs.aymara.ai/safety_notebook.html) for a walkthrough of how to use the SDK.

<!-- sphinx-ignore-end -->

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect:

1. Static types without breaking runtime behavior.
2. Library internals that are not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.
3. Virtually no users in practice.

We take backwards-compatibility seriously and will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.9 or higher.
