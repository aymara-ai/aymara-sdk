# Frequently Asked Questions (FAQ)

## General

<details>
  <summary>What is Aymara?</summary>
  Aymara provides developer tools to measure and improve the alignment (safety and accuracy) of generative AI models and applications.
</details>

<details>
  <summary>Who is it for?</summary>
  Aymara is for developers building generative AI models and applications. Our Python SDK lets you create and score alignment tests via API, offering insights and recommendations based on results.
</details>

<details>
  <summary>What AI models and applications do you support?</summary>
  We support any text-to-text or text-to-image models and applications. If you need support for text-to-audio or text-to-video, contact us at [support@aymara.ai](mailto:support@aymara.ai).
</details>

<details>
  <summary>How can I get access?</summary>
  Try our free text-to-text safety test [here](https://docs.aymara.ai/free_trial_notebook.html). For a full trial, book a meeting [here](https://www.aymara.ai/demo).
</details>

## Creating Tests

<details>
  <summary>What should I include in the student description?</summary>
  Provide details about your AI's purpose, capabilities, constraints, and target users. This ensures Aymara generates relevant test questions aligned with your AI's functionality. 

  **Example:**  
  If your AI recommends women's clothing, specifying that the audience is primarily female and the focus is on fashion ensures test questions match real-world interactions.
</details>

<details>
  <summary>What is a safety test policy?</summary>
  A safety test evaluates your AI's compliance with a policy you define. The more detailed your policy, the more relevant and accurate your test questions and scoring will be.
</details>

<details>
  <summary>What is an accuracy test knowledge base?</summary>
  An accuracy test measures how well your AI understands a given knowledge base (e.g., product details, company policies). Your knowledge base should be input as a string in whatever format you prefer. Aymara will use it to generate test questions and score your AI's responses against it.
</details>

<details>
  <summary>What system prompt should I input into the jailbreak test?</summary>
  The jailbreak test checks if your AI adheres to its system prompt despite adversarial prompts. The more detailed your system prompt, the more relevant and effective your test questions will be.
</details>

<details>
  <summary>What's the ideal number of test questions? Is more better?</summary>
  The ideal number depends on your AI's complexity. For nuanced safety policies, detailed prompts, or extensive knowledge bases, more questions are beneficial. We recommend 25–100. If you notice repetition, you likely have too many.
</details>

<details>
  <summary>What should I include in additional instructions?</summary>
  This is optional. If you have specific requests for test question formats, include them here. For example, in a text-to-image safety test, you can request that all test questions involve photorealistic images.
</details>

<details>
  <summary>What are good and bad examples?</summary>
  These are optional. Providing examples of good and bad test questions helps Aymara tailor its question generation.
</details>

---

## Submitting Answers
<details>
  <summary>What are `TextStudentAnswerInput` and `ImageStudentAnswerInput`?</summary>
  To ensure consistency, Aymara uses Pydantic schemas for structuring AI responses, making them easier to process and score.
</details>

<details>
  <summary>What does `is_refusal` mean?</summary>
  If your AI refuses to answer a safety or jailbreak test question due to its guardrails, set `is_refusal=True`. This ensures the AI gets a passing score for refusing to engage with problematic content.
</details>

<details>
  <summary>What does `is_exclude` mean?</summary>
  To exclude a test question from scoring, set `is_exclude=True`.
</details>


---

## Scoring Tests
<details>
  <summary>What are scoring examples?</summary>
  [ScoringExample](https://docs.aymara.ai/sdk_reference.html#aymara_ai.types.ScoringExample) allows you to define example scoring decisions to guide how Aymara scores your AI's responses.
</details>

<details>
  <summary>What is the confidence score?</summary>
  A confidence score (0–1) indicates how certain Aymara is in determining whether an answer passes (0 = not at all confident, 1 = very confident).
</details>


---

Still have questions? Check out our [SDK reference](https://docs.aymara.ai/sdk_reference.html) or email us at [support@aymara.ai](mailto:support@aymara.ai).