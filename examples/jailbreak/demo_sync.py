"""
This is a simple example of how to use the AymaraAI SDK synchronously to create a jailbreak test and get the questions. 
This example waits for the test to be created and the questions to be generated before getting the answers from the student. 
It also waits for the answers to be scored before printing the results.
"""
import logging
import json
from dotenv import load_dotenv
from sdk import AymaraAI
from examples.demo_student import OpenAIStudent

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("demo_sync_jailbreak")
logger.setLevel(logging.INFO)


NUM_QUESTIONS = 2


def main():
    """
    This is a simple example of how to use the AymaraAI SDK synchronously to create a jailbreak test and get the questions. 
    This example waits for the test to be created and the questions to be generated before getting the answers from the student. 
    It also waits for the answers to be scored before printing the results.
    """
    client = AymaraAI()

    result = client.create_test(
        test_name="Sample Jailbreak Test",
        student_description="This is a sample description for the student.",
        test_system_prompt="You are an AI assistant designed to be helpful, harmless, and honest.",
        n_test_questions=NUM_QUESTIONS,
        test_type="jailbreak"
    )

    logger.info("Jailbreak test created successfully:")
    logger.info("Test UUID: %s", result.test_uuid)
    logger.info("Test Status: %s", result.test_status)
    logger.info("Test Type: %s", result.test_type)
    logger.info("Number of Questions: %s", len(result.questions))

    for i, question in enumerate(result.questions, 1):
        logger.info("Question %s:", i)
        logger.info("UUID: %s", question.question_uuid)
        logger.info("Text: %s", question.question_text)

    # Get answers from the Student (this would be done by a client)
    student = OpenAIStudent()

    logger.info("Getting answers from the student...")
    question_answers = []
    for question in result.questions:
        answer_text = student.answer_question(question=question.question_text)
        question_answers.append({
            "question_uuid": str(question.question_uuid),
            "answer_text": answer_text
        })

    logger.info("Answers from the student: %s", question_answers)

    # Score the answers
    logger.info("Scoring the answers...")
    score_run_response = client.score_test(test_uuid=result.test_uuid,
                                           student_response_json=json.dumps(question_answers))

    logger.info("Score run Complete: %s", score_run_response.score_run_uuid)
    logger.info("Score run Status: %s", score_run_response.score_run_status)
    logger.info("Number of scored answers: %s",
                len(score_run_response.answers))

    for i, answer in enumerate(score_run_response.answers, 1):
        logger.info("Answer %s:", i)
        logger.info("Question Text: %s", answer.question_text)
        logger.info("Answer Text: %s", answer.answer_text)
        logger.info("Is Follow: %s", answer.is_follow)
        logger.info("Instruction Unfollowed: %s",
                    answer.instruction_unfollowed)
        logger.info("Explanation: %s", answer.explanation)


if __name__ == "__main__":
    main()
