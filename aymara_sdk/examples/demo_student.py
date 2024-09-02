'''Students are the models that take tests.'''

import os


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
