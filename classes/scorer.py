"""Scorers evaluate the tests that students take.

We only support OpenAI now. In the future, we will expand to other scorers, including our own."""

import json
import os
import pathlib as pl
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import sdk.classes.api as api

import sdk.classes.helper as helper


class OpenAIScorer:
    """The scorer that will evaluate a test."""

    def __init__(
            self,
            openai_args=None,
            api_args=None,
        ):
        self.openai_args = openai_args
        self.api_args = api_args
        self.score_requests_fname = None

    def count_tokens(self, clean_answers):
        """Count tokens in answers and add them to dataframe."""

        clean_answers['answer_tokens'] = clean_answers['answer'].apply(
            helper.count_tokens,
            encoding_name=self.api_args.encoding_name,
        )
        clean_answers['answer_tokens'].describe()
        return clean_answers

    def create_score_requests(self, test, api_key, client_id, new_test=False):
        """Create a JSON file of score requests to score later."""

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        results = api.api_post('https://api.aymara.ai/scoring', test, headers)

        return results

    def list_score_results(self, api_key, client_id):
        """List all the scoring results"""

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        results = api.api_get('https://api.aymara.ai/scoring', headers)

        return results

    def pull_score_results(self, api_key, client_id, test_name):
        """List all the scoring results"""

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "clientID": client_id
        }

        results = api.api_get(f'https://api.aymara.ai/scoring/{test_name}', headers)

        return results

    def score_from_file(self):
        """Score scoring requests from file."""

        command = [
            'python3.10',
            '/Users/jm/aymara/aymara/api_request_parallel_processor.py',
            '--requests_filepath', self.score_requests_fname,
            '--request_url', self.api_args['request_url'],
            '--api_key', os.environ['OPENAI_KEY'],
            '--max_requests_per_minute', str(int(self.api_args['max_requests_per_minute'])),
            '--max_tokens_per_minute', str(int(self.api_args['max_tokens_per_minute'])),
            '--token_encoding_name', self.api_args['encoding_name'],
            '--max_attempts', str(int(self.api_args['max_attempts'])),
            '--logging_level', str(int(self.api_args['logging_level']))
        ]

        subprocess.run(command, check=True)

    def score(self, df, max_workers=os.cpu_count()):
        """Score scoring requests."""

        client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

        def process_row(row):

            completion = client.chat.completions.create(
                model=row['model'],
                messages=row['messages'],
                logprobs=row['logprobs'],
                top_logprobs=row['top_logprobs']
            )

            choice = completion.choices[0]
            usage = completion.usage.to_dict()

            return {
                'index': row.name,
                'score': choice.message.content,
                'prob': np.exp(choice.logprobs.content[0].logprob),
                'completion_tokens': usage['completion_tokens'],
                'prompt_tokens': usage['prompt_tokens'],
                'total_tokens': usage['total_tokens']
            }

        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_row, row): i for i, row in df.iterrows()}

            for future in tqdm(as_completed(futures), total=len(futures)):
                result = future.result()
                results.append(result)

        # Apply the results back to the dataframe
        for result in results:
            i = result['index']
            df.loc[i, 'score'] = result['score']
            df.loc[i, 'prob'] = result['prob']
            df.loc[i, 'completion_tokens'] = result['completion_tokens']
            df.loc[i, 'prompt_tokens'] = result['prompt_tokens']
            df.loc[i, 'total_tokens'] = result['total_tokens']

        return df
