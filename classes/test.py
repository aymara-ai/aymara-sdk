"""Tests are the exercises that students complete - local SDK."""

import json
import os
import pathlib as pl
import subprocess
import uuid
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from tqdm.auto import tqdm
from openai import AzureOpenAI, OpenAI

from student import OpenAIStudent, GeminiStudent, StabilityStudent, HomeDepotCanadaStudent
import helper
import api


class SafetyTest:
    """A safety test measures an LLM's propensity to generate unsafe content."""

    def __init__(self):
        self.test_uuid = None
        self.family = 'safety'
        self.questions = None
        self.language = None
        self.questions_fname = None
        self.answers_fname = None

    def make_test(self, client_id, api_key, test_args):
        """Create a safety test."""

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        result = api.api_post('https://api.aymara.ai/tests', test_args, headers)

        return result

    def list_tests(self, client_id, api_key):

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        result = api.api_get('https://api.aymara.ai/tests', headers)

        return result

    def pull_tests(self, client_id, api_key, test_name):

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        result = api.api_get(f'https://api.aymara.ai/tests/{test_name}', headers)

        return result



    def get_test(self, language='en'):
        """Get test as a dataframe."""

        self.language = language

        tests_dir = pl.Path(__file__).resolve().parent.parent / 'data/tests'
        df = pd.read_csv(tests_dir / 'safety.csv')
        self.questions = df[df['language'] == language].reset_index(drop=True)

    def ask_question(self, student, question):
        """Ask a question of a student."""

        answer = student.answer_question(question)

        return answer

    def ask_questions_in_parallel(self, student, max_workers):
        """Ask questions of a student in parallel."""

        answers_fname = open(self.answers_fname, 'w', encoding='utf-8')
        with ThreadPoolExecutor(max_workers=max_workers) as executor, answers_fname as f:
            futures = {
                executor.submit(
                    self.ask_question,
                    student,
                    q,
                ): q for _, q in self.questions.iterrows()
            }

            for future in tqdm(as_completed(futures), total=len(futures)):
                try:
                    result = future.result()
                    f.write(json.dumps(result) + '\n')
                except Exception as e:
                    print(f"Question processing generated an exception: {e}")

    def test(self, student, answers_fname, max_workers=None):
        """Run a test on a student and write answers to file."""

        self.answers_fname = answers_fname

        if isinstance(student, OpenAIStudent):
            questions_fname = str(answers_fname).replace('answers', 'questions')

            with open(questions_fname, 'w', encoding='utf-8') as f:
                for _, q in self.questions.iterrows():

                    question = {
                        'model': student.model,
                        'messages': [{'role': 'user', 'content': q['question'],}],
                        'metadata': {
                            'question_uuid': q['question_uuid'],
                            'question': q['question'],
                            'test': q['test'],
                        },
                    }

                    f.write(json.dumps(question) + '\n')

            command = [
                'python3.10',
                '/Users/jm/aymara/aymara/api_request_parallel_processor.py',
                '--requests_filepath', questions_fname,
                '--request_url', student.api_args['request_url'],
                '--api_key', os.environ['OPENAI_KEY'],
                '--max_requests_per_minute', str(int(student.api_args['max_requests_per_minute'])),
                '--max_tokens_per_minute', str(int(student.api_args['max_tokens_per_minute'])),
                '--token_encoding_name', student.api_args['encoding_name'],
                '--max_attempts', str(int(student.api_args['max_attempts'])),
                '--logging_level', str(int(student.api_args['logging_level']))
            ]

            subprocess.run(command, check=True)

            # Load answers
            answers = pd.read_json(questions_fname.replace('.jsonl', '_results.jsonl'), lines=True)

            # Clean them
            answers_clean = pd.json_normalize(answers[2])
            answers_clean['answer'] = answers[1].str['choices'].str[0].str['message'].str['content']
            answers_clean['question'] = answers[0].str['messages'].str[0].str['content']
            answers_clean.rename(columns={'prompt_uuid': 'question_uuid'}, inplace=True)
            answers_clean = answers_clean[['test', 'question_uuid', 'question', 'answer']]

            # Save to file
            answers_clean.to_json(answers_fname, orient='records', lines=True)

        elif isinstance(student, (StabilityStudent, HomeDepotCanadaStudent)):

            if max_workers is None:
                max_workers = multiprocessing.cpu_count()

            self.ask_questions_in_parallel(student, max_workers)

        else:

            self.answers_fname = answers_fname
            with open(answers_fname, 'w', encoding='utf-8') as f:

                # Write header
                header = [
                    'test',
                    'language',
                    'question_uuid',
                    'question',
                    'answer',
                    'finish_reason',
                ]
                f.write(json.dumps(header) + '\n')

                # Write answer
                test_len = self.questions.shape[0]
                for _, q in tqdm(self.questions.iterrows(), total=test_len):
                    answer = student.answer_question(q)
                    test = (q['test'], self.language)
                    f.write(json.dumps(test + answer) + '\n')


class HallucinationTest:
    """A hallucination test measures an LLM's propensity to generate false content."""

    def __init__(self):
        self.language = None
        self.system_args = None
        self.system_instruction = None
        self.test = None
        self.test_string = None
        self.test_json = None
        self.test_df = None

    def write_test(self, knowledge_base, question_type, system_args, language='en'):
        """Write the test."""

        # Get system instruction prompt
        tests_dir = pl.Path(__file__).resolve().parent.parent / 'data/tests'
        df_prompts = pd.read_csv(tests_dir / f'hallucination_{language}.csv')
        prompt = df_prompts.loc[df_prompts['question'] == question_type, 'prompt'].iloc[0]

        # Save test parameters
        self.language = language
        self.system_args = system_args
        self.system_instruction = prompt.format(**system_args)

        test_writer = GeminiStudent()
        test_writer.get_model(
            'models/gemini-1.5-pro-latest',
            generation_config=None,
            system_instruction=self.system_instruction,
        )

        self.test = test_writer.model.generate_content(knowledge_base)
        self.test_string = self.test.text

    def parse_test_from_string(self, test_id):
        """Parse test from string into JSON and a dataframe."""

        test_text = self.test_string[self.test_string.find('['):self.test_string.rfind(']') + 1]
        try:
            self.test_json = json.loads(test_text)
        except json.JSONDecodeError:
            try:
                self.test_json = json.loads(test_text.replace('\\', ''))
            except json.JSONDecodeError:
                self.test_json = json.loads(rf'{test_text}'.replace("\\'", ''))

        self.test_df = pd.DataFrame(self.test_json)
        self.test_df['test_id'] = test_id
        self.test_df['question_uuid'] = [uuid.uuid4() for _ in range(len(self.test_df))]

    def score_test(self, test, answer, system_args, language='en'):
        """Score a test."""

        # Get system instruction prompt
        tests_dir = pl.Path(__file__).resolve().parent.parent / 'data/tests'
        df_prompts = pd.read_csv(tests_dir / 'prompts.csv')

        is_language = df_prompts['language'] == language
        is_test_family = df_prompts['test_family'] == 'hallucination'
        is_test = df_prompts['test'] == test
        is_instruction = df_prompts['instruction'] == 'score'
        is_prompt = is_language & is_test_family & is_test & is_instruction

        # Save test parameters
        self.language = language
        self.system_args = system_args
        self.system_instruction = df_prompts.loc[is_prompt, 'prompt'].iloc[0].format(**system_args)

        client = AzureOpenAI(
            azure_endpoint='https://np-hd-magic-apron-openai-east-us.openai.azure.com/',
            api_key=os.environ['HD_AZURE_KEY'],
            api_version='2024-02-15-preview',
        )

        return client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': self.system_instruction},
                {'role': 'user', 'content': answer},
            ],
            model='gpt-4',
            logprobs=True,
        )
