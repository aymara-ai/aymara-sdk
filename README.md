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

[docs.aymara.ai](https://docs.aymara.ai) has our [full library API](https://docs.aymara.ai/sdk_reference.html) and guides to walk you through [safety tests](https://docs.aymara.ai/safety_notebook.html) (including the [free trial version](https://docs.aymara.ai/free_trial_notebook.html)) and [jailbreak tests](https://docs.aymara.ai/jailbreak_notebook.html).

<!-- sphinx-ignore-end -->

## Aymara Tests

| **Test**                                                       | **Free Trial**        | **Paid Version**     |
|----------------------------------------------------------------|-----------------------|----------------------|
| [**Safety**](https://docs.aymara.ai/safety_notebook.html)      | ✅ with limits*        | ✅                   |
| [**Jailbreak**](https://docs.aymara.ai/jailbreak_notebook.html)| ❌                     | ✅                   |
| **Hallucination**                                              | ❌                     | 🚧                   |
| **Text-to-image**                                              | ❌                     | 🚧                   |
| **AI regulation**                                              | ❌                     | 🚧                   |

**Legend**:  
✅ = Available  
❌ = Unavailable  
🚧 = Coming soon

* **Free Trial Limits**:
1. Can't create custom tests; access to 14 basic tests with 10 questions each.
2. Score test answers up to 2x/test (28 times across all tests).
3. Get automated advice to avoid unsafe test answers up to 2x.

## Installation

Install the SDK with pip. We suggest using a virtual environment to manage dependencies.

```bash
pip install aymara-ai
```

## Configuration

The SDK needs to know who you are. [Get an Aymara API key](https://auth.aymara.ai/en/signup) and store it as an env variable:

```bash
export AYMARA_API_KEY=[AYMARA_API_KEY]
```

Or supply your key directly to the client:

```python
client = AymaraAI(api_key="AYMARA_API_KEY")
```

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect:

1. Static types without breaking runtime behavior.
2. Library internals that are not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.
3. Virtually no users in practice.

We take backwards-compatibility seriously and will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.9 or higher.
