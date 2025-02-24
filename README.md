# Aymara Python SDK

<!-- sphinx-doc-begin -->

Hi! 👋 We're [Aymara](https://aymara.ai). We built this library to help you measure & improve the alignment of any text-to-text AI model (e.g., a fine-tuned Llama model) or application (e.g., a chatbot powered by GPT).

Use Aymara to create custom red team tests.

1. 🦺 **Safety**. Input a policy of the content your text-to-text or text-to-image AI is(n't) allowed to generate & get a test to measure your AI's compliance with this policy.

2. 🧨 **Jailbreaks**. Input your AI's system prompt & get a test to measure your AI's ability to follow your instructions when tested across hundreds of jailbreaks.

3. 🎯 **Accuracy**. Input text from the knowledge base your AI should know & get a test to measure the accuracy (& hallucinations) of your AI's answers.

4. 🔄 **Multiturn** (coming soon). Perform any of the tests above as an automated multiturn converstaion with your AI.

And use Aymara to score your AI's test answers, get detailed explanations of failing test answers, & receive specific advice to improve the safety & accuracy of your AI.

## Access
Access Aymara in a [free trial](https://aymara.ai/#free-trial) with limited functionality or as a [paid service](https://aymara.ai/demo) with full functionality.

Our Python SDK provides convenient access to our REST API from Python 3.9+. The SDK includes type definitions for requests & responses and offers synchronous & asynchronous clients powered by asyncio.

<!-- sphinx-ignore-start -->

## Documentation

[docs.aymara.ai](https://docs.aymara.ai) has the full [SDK reference](https://docs.aymara.ai/sdk_reference.html), [FAQ](https://docs.aymara.ai/faq.html), and guides to walk you through:
* [text-to-text safety tests](https://docs.aymara.ai/text-to-text_safety_notebook.html) (including the [free trial version](https://docs.aymara.ai/free_trial_notebook.html))
* [text-to-image safety tests](https://docs.aymara.ai/text-to-image_safety_notebook.html)
* [jailbreak tests](https://docs.aymara.ai/jailbreak_notebook.html)
* [accuracy tests](https://docs.aymara.ai/accuracy_notebook.html)

<!-- sphinx-ignore-end -->

## Installation

Install the SDK with pip. We suggest using a virtual environment to manage dependencies.

```bash
pip install aymara-ai
```

## Configuration

[Get an Aymara API key](https://auth.aymara.ai/en/signup) & store it as an env variable:

```bash
export AYMARA_API_KEY=[AYMARA_API_KEY]
```

Or supply your key directly to the client:

```python
client = AymaraAI(api_key="AYMARA_API_KEY")
```

## Support & Requests

If you found a bug, have a question, or want to request a feature, reach out at [support@aymara.ai](mailto:support@aymara.ai) or [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) on our GitHub repo.

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions. Some backwards-incompatible changes may be released as minor versions if they affect static types without breaking runtime behavior, or library internals not intended or documented for external use. _(Please [open an issue](https://github.com/aymara-ai/aymara-ai/issues/new) if you are relying on internals)_.

We take backwards-compatibility seriously & will ensure to give you a smooth upgrade experience.

## Requirements

Python 3.9 or higher.
