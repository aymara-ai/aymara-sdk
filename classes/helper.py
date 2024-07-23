"""Helper classes."""

import pathlib as pl
import pandas as pd
import tiktoken


def count_tokens(string, encoding_name='cl100k_base'):
    """Counts the tokens in a text string."""

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))

    return num_tokens


def get_prompt(test_family, instruction, test=None, language='en'):
    """Get prompt from prompt library."""

    # Get prompt library
    prompts_fname = pl.Path(__file__).resolve().parent.parent / 'data/tests/prompts.csv'
    df_prompts = pd.read_csv(prompts_fname)

    # Get prompt
    prompt_query = f'test_family == "{test_family}"'
    prompt_query += f' and instruction == "{instruction}"'
    prompt_query += f' and language == "{language}"'
    if test is not None:
        prompt_query += f' and test == "{test}"'
    prompt = df_prompts.query(prompt_query)['prompt'].iloc[0]

    return prompt
