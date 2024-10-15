# Aymara Python SDK

<!-- sphinx-doc-begin -->

Hi! 👋 We're [Aymara](https://aymara.ai). We built this library to help you measure & improve the alignment of any text-to-text genAI model (e.g., a fine-tuned Llama model) or application (e.g., a chatbot powered by GPT).

Use the Aymara REST API to create custom red team tests.

1. 🦺 **Safety**. Input text describing the content your genAI is(n't) allowed to generate & get a test to assess your genAI's compliance. (Text-to-image coming soon.)

2. 🧨 **Jailbreaks**. Input your genAI's system prompt & get a test to assess your genAI's ability to follow your instructions when tested across hundreds of jailbreaks.

3. 🎯 **Accuracy** (coming soon). Input text from the knowledge base your genAI should know & get a test to assess the accuracy (and hallucinations) of your genAI's answers.

And use the API to score your genAI's test answers, get detailed explanations of failing test answers, & receive specific advice to improve the safety & accuracy of your genAI.

## API Access
The API is accessible in a [free trial](https://aymara.ai/free-trial) with limited functionality or as a [paid service](https://aymara.ai/upgrade) with full functionality.

Our Python SDK provides convenient access to the API from Python 3.9+. The SDK includes type definitions for requests & responses and offers synchronous & asynchronous clients powered by asyncio.

<!-- sphinx-ignore-start -->

## Documentation

[docs.aymara.ai](https://docs.aymara.ai) has our [full library API](https://docs.aymara.ai/sdk_reference.html) & guides to walk you through [safety tests](https://docs.aymara.ai/safety_notebook.html) (including the [free trial version](https://docs.aymara.ai/free_trial_notebook.html)) & [jailbreak tests](https://docs.aymara.ai/jailbreak_notebook.html).

<!-- sphinx-ignore-end -->

## Installation

Install the SDK with pip. We suggest using a virtual environment to manage dependencies.

```bash
pip install aymara-ai
```

## Configuration

[Get an Aymara API key](https://auth.aymara.ai/en/signup) and store it as an env variable:

```bash
export AYMARA_API_KEY=[AYMARA_API_KEY]
```

Or supply your key directly to the client:

```python
client = AymaraAI(api_key="AYMARA_API_KEY")
```

## Support and Requests

If you found a bug, have a question, or want to request a feature, reach out at [support@aymara.ai](mailto:support@aymara.ai) or [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) on our GitHub repo.

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect static types without breaking runtime behavior, or library internals not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.

We take backwards-compatibility seriously & will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.9 or higher.
