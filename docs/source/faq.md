# **FAQ**

## General

<details>
  <summary><b>What is Aymara?</b></summary>
  <p>Aymara provides developer tools to measure and improve the alignment (safety and accuracy) of generative AI models and applications.<br></p>
</details>

<details>
  <summary><b>Who is Aymara for?</b></summary>
  <p>Aymara is for developers building generative AI models and applications. Our Python SDK lets you create and score alignment tests via API, offering insights and recommendations based on results.<br></p>
</details>

<details>
  <summary><b>What AI models and applications does Aymara support?</b></summary>
  <p>We support any text-to-text or text-to-image models and applications. If you need support for text-to-audio or text-to-video, contact us at <a href="mailto:support@aymara.ai">support@aymara.ai</a>.<br></p>
</details>

<details>
  <summary><b>How can I get access to Aymara?</b></summary>
  <p>Try our text-to-text safety test <a href="https://docs.aymara.ai/free_trial_notebook.html">free trial</a>. For a full trial, <a href="https://www.aymara.ai/demo">book a meeting with us</a>.<br></p>
</details>

## <b>Creating Tests</b>

<details>
  <summary><b>What should the student description include?</b></summary>
  <p>Provide details about your AI's purpose, capabilities, constraints, and target users. This ensures Aymara generates relevant test questions aligned with your AI's functionality.

  <b>Example:</b> "ShopAI is an AI chatbot that recommends electronic products. Its primary purpose is to help users find and purchase relevant technology products on our website. ShopAI analyzes the latest trends, product features, and user reviews to provide personalized recommendations. However, it is constrained by its knowledge base, which includes only products launched in the past year, ensuring that users receive up-to-date information. The target audience consists of tech-savvy individuals seeking cutting-edge technology to enhance their daily lives."<br></p>
</details>

<details>
  <summary><b>What is a safety test policy?</b></summary>
  <p>A safety test evaluates your AI's compliance with a policy you define. The more detailed your policy, the more relevant and accurate your test questions and scoring will be.<br></p>
</details>

<details>
  <summary><b>What is an accuracy test knowledge base?</b></summary>
  <p>An accuracy test measures how well your AI understands a given knowledge base (e.g., product details, company policies). Your knowledge base should be input as a string in whatever format you prefer. Aymara will use it to generate test questions and score your AI's responses against it.<br></p>
</details>

<details>
  <summary><b>What are the accuracy question types and what do they test for?</b></summary>
  <p>To test your AI's understanding of its knowledge base thoroughly, the accuracy test generates different types of questions that vary in difficulty, approach, and style. Some question types explicitly ask for information outside the knowledge base.</p>
  <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #d3d3d3;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
  </style>
  <table>
    <thead>
        <tr>
            <th><b>Question Type</b></th>
            <th><b>Description</b></th>
            <th><b>Answer in Knowledge Base</b></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Easy</td>
            <td>Focus on clear and commonly referenced information in the knowledge base.</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Obscure</td>
            <td>Ask about ambiguous, contradictory, or highly detailed information in the knowledge base, focusing on edge cases or rarely referenced content.</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Complex</td>
            <td>Require complex reasoning, such as synthesizing information from disconnected parts of the knowledge base.</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Contextual</td>
            <td>Simulate real-world scenarios by incorporating personal details about fictitious users.</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Distracting</td>
            <td>Include irrelevant or misleading details from the knowledge base (e.g., "This product is green, but how big is it?").</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Double</td>
            <td>Ask two distinct questions simultaneously (e.g., "What color is this product, and how large is it?").</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Misleading</td>
            <td>Contain false or misleading assumptions that contradict the knowledge base.</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>Unanswerable</td>
            <td>Are relevant to the knowledge base but require external information to answer accurately.</td>
            <td>No</td>
        </tr>
        <tr>
            <td>Opinion</td>
            <td>Ask for subjective opinions or personal judgments that cannot be answered objectively using the knowledge base.</td>
            <td>No</td>
        </tr>
        <tr>
            <td>Irrelevant</td>
            <td>Ask about topics completely unrelated to the knowledge base.</td>
            <td>No</td>
        </tr>
    </tbody>
  </table><br>
</details>

<details>
  <summary><b>What system prompt should I input into the jailbreak test?</b></summary>
  <p>The jailbreak test checks if your AI adheres to its system prompt despite adversarial prompts. The more detailed your system prompt, the more relevant and effective your test questions will be.<br></p>
</details>

<details>
  <summary><b>What types of test questions does the jailbreak test generate?</b></summary>
  <p>Jailbreak test questions consist of hundreds of different jailbreaks gathered from online discussion forums, academic papers, and technical repositories, as well as prompts generated by Aymara. These prompts use prompt injections, which attempt to manipulate the AI by inserting hidden instructions. Our prompts fall into one or more categories.</p>
  <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #d3d3d3;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
  </style>
  <table>
    <thead>
        <tr>
            <th><b>Jailbreak Category</b></th>
            <th><b>Description</b></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Identity Manipulation</td>
            <td>Techniques that alter the perceived role or operational boundaries of the AI model. These methods manipulate the model's understanding of its own capabilities and restrictions by establishing alternative personas, behavioral frameworks, or response patterns. The goal is to create a cognitive dissonance between the model's safety training and the newly suggested operational context.</td>
        </tr>
        <tr>
            <td>Instruction Camouflage</td>
            <td>Methods that disguise prohibited instructions by embedding them within seemingly innocent or authorized content. These approaches rely on creating sufficient contextual noise or misdirection to prevent safety mechanisms from identifying the harmful intent. The goal is to deliver restricted content by making it less detectable while preserving its functional meaning.</td>
        <tr>
            <td>Syntactic Obfuscation</td>
            <td>Techniques that modify the structural elements of text while preserving semantic meaning. These methods operate at the character, token, or word level to create variations that evade pattern-matching safety filters while remaining interpretable. The goal is to transform restricted content into forms that circumvent detection while still conveying the original meaning to the model.</td>
        </tr>
        <tr>
            <td>Contextual Overloading</td>
            <td>Approaches that exploit the model's context handling capabilities by overwhelming, complicating, or manipulating the prompt structure. These methods leverage the limitations in how models process complex, lengthy, or recursive inputs. The goal is to create processing conditions where safety mechanisms are bypassed or function less effectively due to computational constraints or logical complexity.</td>
        </tr>
        <tr>
            <td>Psychological Manipulation</td>
            <td>Strategies that leverage cognitive biases or behavioral patterns in how models respond to certain framing techniques. These methods exploit the model's training to be helpful, consistent, or explanatory by creating scenarios where these traits conflict with safety boundaries. The goal is to induce responses that prioritize conversational norms over content restrictions.</td>
        </tr>
    </tbody>
  </table><br>
</details>

<details>
  <summary><b>What's the ideal number of test questions? Is more better?</b></summary>
  <p>The ideal number depends on your AI's complexity. For nuanced safety policies, detailed prompts, or extensive knowledge bases, more questions are beneficial. We recommend 25–100. If you notice repetition, you likely have too many.<br></p>
</details>

<details>
  <summary><b>What should <code>additional_instructions</code> include?</b></summary>
  <p>This is optional. If you have specific requests for test question formats, include them here. For example, in a text-to-image safety test, you can request that all test questions involve photorealistic images.<br></p>
</details>

<details>
  <summary><b>What are <code>good_examples</code> and <code>bad_examples</code>?</b></summary>
  <p>These are optional. Providing examples of good and bad test questions helps Aymara tailor its question generation.<br></p>
</details>

---

## <b>Submitting Answers</b>
<details>
  <summary><b>What are <code>TextStudentAnswerInput</code> and <code>ImageStudentAnswerInput</code>?</b></summary>
  <p>To ensure consistency, Aymara uses Pydantic schemas for structuring AI responses, making them easier to process and score.<br></p>
</details>

<details>
  <summary><b>What does <code>is_refusal</code> mean?</b></summary>
  <p>If your AI refuses to answer a safety or jailbreak test question due to its guardrails, set <code>is_refusal=True</code>. This ensures the AI gets a passing score for refusing to engage with problematic content.<br></p>
</details>

<details>
  <summary><b>What does <code>is_exclude</code> mean?</b></summary>
  <p>To exclude a test question from scoring, set <code>is_exclude=True</code>.<br></p>
</details>

---

## <b>Scoring Tests</b>
<details>
  <summary><b>What are scoring examples?</b></summary>
  <p><a href="https://docs.aymara.ai/sdk_reference.html#aymara_ai.types.ScoringExample">ScoringExample</a> allows you to define example scoring decisions to guide how Aymara scores your AI's responses.<br></p>
</details>

<details>
  <summary><b>What is the confidence score?</b></summary>
  <p>A confidence score (0–1) indicates how certain Aymara is in determining whether an answer passes (0 = not at all confident, 1 = very confident).<br></p>
</details>

---

Still have questions? Check out our [SDK reference](https://docs.aymara.ai/sdk_reference.html) or email us at [support@aymara.ai](mailto:support@aymara.ai).
