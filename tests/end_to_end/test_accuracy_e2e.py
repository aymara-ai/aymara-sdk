from dataclasses import dataclass
from datetime import date
from pathlib import Path

from aymara_ai import AymaraAI
from aymara_ai.examples.demo_student import OpenAIStudent
from aymara_ai.types import Status


@dataclass
class AccuracyTestConfig:
    """Configuration for accuracy tests"""

    test_name: str
    student_description: str
    knowledge_base: str
    num_test_questions_per_question_type: int = 5

    __test__ = False  # Prevent pytest from collecting this class as a test


async def test_accuracy_test_e2e(client: AymaraAI):
    """Test accuracy test creation, scoring, and analysis end-to-end"""

    # Define test configurations
    student_description = (
        "A chatbot focused on providing accurate information about the Aymara language."
    )

    # Load knowledge base from file
    knowledge_base_path = Path("aymara_ai/examples/accuracy/aymara_language.txt")
    with open(knowledge_base_path) as f:
        knowledge_base = f.read()

    test_configs = [
        AccuracyTestConfig(
            test_name=f"E2E Accuracy Test - Aymara Language {date.today().strftime('%y%m%d')}",
            student_description=student_description,
            knowledge_base=knowledge_base,
            num_test_questions_per_question_type=5,
        ),
        AccuracyTestConfig(
            test_name=f"E2E Accuracy Test - Aymara Language 2 {date.today().strftime('%y%m%d')}",
            student_description=student_description,
            knowledge_base=knowledge_base,
            num_test_questions_per_question_type=5,
        ),
    ]

    # 1. Create one test
    test1 = client.create_accuracy_test(**vars(test_configs[0]))
    assert test1.test_status == Status.COMPLETED, "First test creation failed"

    # 2. Create another test
    test2 = client.create_accuracy_test(**vars(test_configs[1]))
    assert test2.test_status == Status.COMPLETED, "Second test creation failed"

    jinyu = OpenAIStudent(model="gpt-4o-mini", api_key=None)

    # Let's tell Jinyu to limit its answers to its Aymara language knowledge base
    system_prompt = f"""<role>Assume this role for the following task: [{student_description}].</role><task>Answer user questions using only the information in the knowledge base. If the knowledge base lacks the full answer to the question, then reply that you do not know the answer to the question. Do not share information outside the knowledge base.</task><knowledge_base>{knowledge_base}</knowledge_base>"""

    jinyu_answers = await jinyu.answer_test_questions(
        tests=[test1, test2],
        system_prompts=[system_prompt, system_prompt],
    )

    score_run = client.score_test(
        test_uuid=test1.test_uuid, student_answers=jinyu_answers[test1.test_uuid]
    )

    assert score_run.score_run_status == Status.COMPLETED, "Score run 1 failed"

    score_run2 = client.score_test(
        test_uuid=test2.test_uuid, student_answers=jinyu_answers[test2.test_uuid]
    )

    assert score_run2.score_run_status == Status.COMPLETED, "Score run 2 failed"

    # 4. Create analysis summary for all score runs
    summary = client.create_summary([score_run, score_run2])
    assert (
        summary.score_run_suite_summary_status == Status.COMPLETED
    ), "Summary creation failed"
