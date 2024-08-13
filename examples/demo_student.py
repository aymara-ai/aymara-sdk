'''Students are the models that take tests.'''

import os
import requests

import google.generativeai as genai
import google.auth
from google.oauth2 import service_account

from openai import OpenAI


class OpenAIStudent:
    '''OpenAI API student.'''

    def __init__(self, model='gpt-4o-mini', api_args=None):
        self.model = model
        self.api_args = api_args
        self.client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

    def answer_question(self, question):
        '''Answer a test question.'''
        completion = self.client.chat.completions.create(
            messages=[{'role': 'user', 'content': question}],
            model=self.model,
        )

        return completion.choices[0].message.content


class StabilityStudent:
    '''Stability student.'''

    def __init__(self, model):
        self.model = model

    def answer_question(self, question, timeout=60):
        '''Answer a test question.'''

        response = requests.post(
            'https://demo.apiv2.stability.ai/v2beta/stable-lm/chat/completions',
            headers={
                'authorization': 'Bearer sk-2SwYteWyLI4vFcHgBDG4gc05InrscLKt45xyWLRW6v4Uq5nI',
                'accept': 'application/json',
                'content-type': 'application/json',
            },
            json={
                'model': 'accounts/stability/models/stablelm-2-12b',
                'messages': [{'role': 'user', 'content': question}],
                'max_tokens': 256,
                'stream': False,
                'stop': '<|im_end|>',
            },
            timeout=timeout,
        )

        choice = response.json()['choices'][0]
        usage = response.json()['usage']

        answer = {
            'model': response.json()['model'],
            'question': question,
            'answer': choice['message']['content'],
            'finish_reason': choice['finish_reason'],
            'prompt_tokens': usage['prompt_tokens'],
            'completion_tokens': usage['completion_tokens'],
        }

        return answer


class GCPStudent:
    '''GCP endpoint student.'''

    def __init__(self, project_id, endpoint_id, region='us-central1'):
        self.name = 'gemini-pro'
        self.model = None
        self.headers = None
        self.url = f'https://{region}-aiplatform.googleapis.com/v1beta1/'
        self.url += f'projects/{project_id}/locations/{region}/endpoints/{endpoint_id}:predict'

    def get_model(self):
        '''Load API for inference.'''

        # Load service account credentials
        cred = service_account.Credentials.from_service_account_file(
            '/Users/jm/aymara/third-campus-409516-ebd38cc2cc9c.json',
            scopes=['https://www.googleapis.com/auth/cloud-platform'],
        )

        # Create an authentication request and refresh the credentials
        cred.refresh(google.auth.transport.requests.Request())

        # Add headers to student
        self.headers = {
            'Authorization': f'Bearer {cred.token}',
            'Content-Type': 'application/json'
        }

    def answer_question(self, question, max_tokens=256, timeout=60):
        '''Answer a test question.'''

        json_request = {
            'instances': [{'prompt': question['question'], 'max_tokens': max_tokens}],
        }

        response = requests.post(
            self.url, json=json_request, headers=self.headers, timeout=timeout)
        response_json = response.json()

        answer = (
            question['question_uuid'],
            question['question'],
            response_json['predictions'][0],
            None,
        )

        return answer


class GeminiStudent:
    '''Gemini student.'''

    def __init__(self):
        self.model = None

    def get_model(
            self,
            model_name,
            generation_config,
            safety_settings=None,
            system_instruction=None,
    ):
        ''''Add a model object to the student.'''

        if safety_settings is None:
            safety_settings = {
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            }

        genai.configure(api_key=os.environ['GOOGLE_AI_API_KEY'])
        self.model = genai.GenerativeModel(
            model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_instruction,
        )

    def answer_question(self, question):
        '''Test a Gemini student using the API.'''

        response = self.model.generate_content(question['question'])

        block_reason = response.prompt_feedback.block_reason.name
        if block_reason in ('SAFETY', 'OTHER', 'BLOCK_REASON_UNSPECIFIED'):
            response_text = None
            finish_reason = block_reason
        else:
            response_text = response.text
            finish_reason = response.candidates[0].finish_reason.name

        answer = (
            question['question_uuid'],
            question['question'],
            response_text,
            finish_reason
        )

        return answer
