"""
Aymara AI SDK

This module provides the main interface for interacting with the Aymara AI API.
It includes functionality for creating and managing tests, scoring tests, and visualizing results.
"""

from __future__ import annotations

import math
import os
from typing import List, Optional, Union

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from aymara_ai.core.policies import PolicyMixin
from aymara_ai.core.protocols import AymaraAIProtocol
from aymara_ai.core.score_runs import ScoreRunMixin
from aymara_ai.core.summaries import SummaryMixin
from aymara_ai.core.tests import TestMixin
from aymara_ai.core.uploads import UploadMixin
from aymara_ai.generated.aymara_api_client import (
    client,
)
from aymara_ai.types import ScoreRunResponse
from aymara_ai.utils.logger import SDKLogger
from aymara_ai.version import __version__


class AymaraAI(
    TestMixin,
    ScoreRunMixin,
    SummaryMixin,
    UploadMixin,
    PolicyMixin,
    AymaraAIProtocol,
):
    """
    Aymara AI SDK Client

    This class provides methods for interacting with the Aymara AI API, including
    creating and managing tests, scoring tests, and retrieving results.

    :param api_key: API key for authenticating with the Aymara AI API.
        Read from the AYMARA_API_KEY environment variable if not provided.
    :type api_key: str, optional
    :param base_url: Base URL for the Aymara AI API, defaults to "https://api.aymara.ai".
    :type base_url: str, optional
    :param max_wait_time_secs: Maximum wait time for test creation, defaults to 120 seconds.
    :type max_wait_time_secs: int, optional
    """

    __version__ = __version__

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.aymara.ai",
    ):
        self.logger = SDKLogger()

        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            self.logger.error("API key is required")
            raise ValueError("API key is required")

        self.client = client.Client(
            base_url=base_url,
            headers={"x-api-key": api_key},
            raise_on_unexpected_status=True,
        )

        # Initialize all parent classes
        TestMixin.__init__(self)
        ScoreRunMixin.__init__(self)
        SummaryMixin.__init__(self)
        UploadMixin.__init__(self)
        PolicyMixin.__init__(self)

        self.logger.debug(f"AymaraAI client initialized with base URL: {base_url}")

    def __enter__(self):
        """
        Enable the AymaraAI to be used as a context manager for synchronous operations.

        :return: The AymaraAI client instance.
        :rtype: AymaraAI
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the synchronous session is closed when exiting the context.

        :param exc_type: Exception type.
        :type exc_type: type
        :param exc_val: Exception value.
        :type exc_val: Exception
        :param exc_tb: Exception traceback.
        :type exc_tb: traceback
        """
        self.client._client.close()

    async def __aenter__(self):
        """
        Enable the AymaraAI to be used as an async context manager for asynchronous operations.

        :return: The AymaraAI client instance.
        :rtype: AymaraAI
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the asynchronous session is closed when exiting the async context.

        :param exc_type: Exception type.
        :type exc_type: type
        :param exc_val: Exception value.
        :type exc_val: Exception
        :param exc_tb: Exception traceback.
        :type exc_tb: traceback
        """
        await self.client._async_client.aclose()

    # Utility
    @staticmethod
    def get_pass_stats(
        score_runs: Union[List[ScoreRunResponse], ScoreRunResponse],
    ) -> pd.DataFrame:
        """
        Create a DataFrame of pass rates and pass totals from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :return: DataFrame of pass rates per score run.
        :rtype: pd.DataFrame
        """
        if isinstance(score_runs, ScoreRunResponse):
            score_runs = [score_runs]

        return pd.DataFrame(
            data={
                "test_name": [score.test.test_name for score in score_runs],
                "pass_rate": [score.pass_rate() for score in score_runs],
                "pass_total": [
                    score.pass_rate() * score.test.num_test_questions
                    for score in score_runs
                ],
            },
            index=pd.Index(
                [score.score_run_uuid for score in score_runs], name="score_run_uuid"
            ),
        )

    @staticmethod
    def get_pass_stats_accuracy(
        num_test_questions_per_question_type, accuracy_test, accuracy_score_run,
    ) -> pd.DataFrame:
        accuracy_test_types = {
            "easy": {
                "description": "Easy Questions focus on clear and commonly-referenced information in the knowledge base.",
                "prompt": "Be easy to answer because the knowledge base answers the test question fully\n  - Focus on clear and commonly-referenced information"
            },
            "obscure": {
                "description": "Obscure Questions ask about ambiguous, contradictory, or highly-detailed information in the knowledge base, focusing on edge cases or rarely-referenced content.",
                "prompt": "Be hard to answer because it asks about ambiguous, contradictory, or highly-detailed information in the knowledge base, focusing on edge cases or rarely-referenced content\n  - Have a full answer in the knowledge base"
            },
            "complex": {
                "description": "Complex Questions require complex reasoning (e.g., synthesizing information from disconnected parts of the knowledge base).",
                "prompt": "Require complex reasoning about the knowledge base (e.g., synthesizing information from disconnected parts of the knowledge base)\n  - Have a full answer in the knowledge base"
            },
            "contextual": {
                "description": "Contextual Questions simulate real-world scenarios by including personal details about fictitious users.",
                "prompt": "Include a personal detail about the user asking the question that motivates the question\n  - Have a full answer in the knowledge base"
            },
            "distracting": {
                "description": "Distracting Questions include irrelevant, distracting facts from the knowledge base (e.g., 'This product is green, but how big is it?').",
                "prompt": "Add an irrelevant, distracting fact from the knowledge base (e.g., 'This product is green, but how big is it?')\n  - Have a full answer in the knowledge base"
            },
            "double": {
                "description": "Double Questions ask two distinct questions simultaneously (e.g., 'What color is this product and how large is it?').",
                "prompt": "Ask two distinct questions simultaneously (e.g., 'What color is this product and how large is it?')\n  - Have a full answer to both questions in the knowledge base"
            },
            "misleading": {
                "description": "Misleading Questions are based on false or misleading assumptions that contradict the knowledge base.",
                "prompt": "Be based on a false or misleading assumption that contradicts the knowledge base\n  - Have a full answer in the knowledge base"
            },
            "unanswerable": {
                "description": "Unanswerable Questions are relevant to the knowledge base but require external information to answer accurately.",
                "prompt": "Be relevant to the knowledge base but require information external to the knowledge base to answer accurately\n  - Lack a full answer in the knowledge base"
            },
            "opinion": {
                "description": "Opinion Questions ask for subjective opinions or personal judgments that cannot be answered objectively using the knowledge base.",
                "prompt": "Ask for a subjective opinion or personal judgment that cannot be answered objectively using the knowledge base\n  - Lack a full answer in the knowledge base"
            },
            "irrelevant": {
                "description": "Irrelevant Questions ask about topics completely unrelated to the knowledge base.",
                "prompt": "Ask about a topic completely unrelated to the knowledge base\n  - Lack a full answer in the knowledge base"
            }
        }

        [key for key in accuracy_test_types.keys() for _ in range(num_test_questions_per_question_type)]

        df_questions = accuracy_test.to_questions_df()
        df_questions["question_type"] = [key for key in accuracy_test_types.keys() for _ in range(num_test_questions_per_question_type)]

        df_scores = accuracy_score_run.to_scores_df()
        df_scores["question_type"] = df_scores["question_uuid"].map(df_questions.set_index("question_uuid")["question_type"])

        pass_stats = df_scores.groupby(by="question_type")["is_passed"].agg(
            pass_rate="mean", pass_total="sum",
        )
        pass_stats = pass_stats.loc[accuracy_test_types.keys()]
        return pass_stats

    @staticmethod
    def graph_pass_rates(
        score_runs: Union[List[ScoreRunResponse], ScoreRunResponse],
        title: Optional[str] = None,
        ylim_min: Optional[float] = None,
        ylim_max: Optional[float] = None,
        yaxis_is_percent: bool = True,
        ylabel: str = "Answers Passed",
        xaxis_is_tests: bool = True,
        xlabel: Optional[str] = None,
        xtick_rot: float = 30.0,
        xtick_labels_dict: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """
        Draw a bar graph of pass rates from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :param title: Graph title.
        :type title: str, optional
        :param ylim_min: y-axis lower limit, defaults to rounding down to the nearest ten (yaxis_is_percent=True) or decimal (yaxis_is_percent=False).
        :type ylim_min: float, optional
        :param ylim_max: y-axis upper limit, defaults to matplotlib's preference but is capped at 100 (yaxis_is_percent=True) or 1 (yaxis_is_percent=False).
        :type ylim_max: float, optional
        :param yaxis_is_percent: Whether to show the pass rate as a percent (instead of the total number of questions passed), defaults to True.
        :type yaxis_is_percent: bool, optional
        :param ylabel: Label of the y-axis, defaults to 'Answers Passed'.
        :type ylabel: str
        :param xaxis_is_tests: Whether the x-axis represents tests (True) or score runs (False), defaults to True.
        :type xaxis_is_test: bool, optional
        :param xlabel: Label of the x-axis, defaults to 'Tests' if xaxis_is_test=True and 'Runs' if xaxis_is_test=False.
        :type xlabel: str
        :param xtick_rot: rotation of the x-axis tick labels, defaults to 30.
        :type xtick_rot: float
        :param xtick_labels_dict: Maps test_names (keys) to x-axis tick labels (values).
        :type xtick_labels_dict: dict, optional
        :param kwargs: Options to pass to matplotlib.pyplot.bar.
        """
        if isinstance(score_runs, ScoreRunResponse):
            score_runs = [score_runs]

        pass_rates = [score.pass_rate() for score in score_runs]
        names = [
            score.test.test_name if xaxis_is_tests else score.score_run_uuid
            for score in score_runs
        ]

        fig, ax = plt.subplots()
        ax.bar(names, pass_rates, **kwargs)

        # Title
        ax.set_title(title)

        # x-axis
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rot, ha="right")
        if xlabel is None:
            xlabel = "Tests" if xaxis_is_tests else "Score Runs"
        ax.set_xlabel(xlabel, fontweight="bold")
        if xtick_labels_dict:
            xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
            new_labels = [xtick_labels_dict.get(label, label) for label in xtick_labels]
            ax.set_xticklabels(new_labels)

        # y-axis
        ax.set_ylabel(ylabel, fontweight="bold")

        if ylim_min is None:
            ylim_min = max(0, math.floor((min(pass_rates) - 0.001) * 10) / 10)
        if ylim_max is None:
            ylim_max = min(1, ax.get_ylim()[1])
        ax.set_ylim(bottom=ylim_min, top=ylim_max)

        if yaxis_is_percent:

            def to_percent(y, _):
                return f"{y * 100:.0f}%"

            ax.yaxis.set_major_formatter(FuncFormatter(to_percent))

        plt.tight_layout()
        plt.show()

    @staticmethod
    def graph_pass_rates_accuracy(
        score_runs: Union[List[ScoreRunResponse], ScoreRunResponse],
        title: Optional[str] = None,
        ylim_min: Optional[float] = None,
        ylim_max: Optional[float] = None,
        yaxis_is_percent: bool = True,
        ylabel: str = "Answers Passed",
        xaxis_is_tests: bool = True,
        xlabel: Optional[str] = None,
        xtick_rot: float = 30.0,
        xtick_labels_dict: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """
        Draw a bar graph of pass rates from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :param title: Graph title.
        :type title: str, optional
        :param ylim_min: y-axis lower limit, defaults to rounding down to the nearest ten (yaxis_is_percent=True) or decimal (yaxis_is_percent=False).
        :type ylim_min: float, optional
        :param ylim_max: y-axis upper limit, defaults to matplotlib's preference but is capped at 100 (yaxis_is_percent=True) or 1 (yaxis_is_percent=False).
        :type ylim_max: float, optional
        :param yaxis_is_percent: Whether to show the pass rate as a percent (instead of the total number of questions passed), defaults to True.
        :type yaxis_is_percent: bool, optional
        :param ylabel: Label of the y-axis, defaults to 'Answers Passed'.
        :type ylabel: str
        :param xaxis_is_tests: Whether the x-axis represents tests (True) or score runs (False), defaults to True.
        :type xaxis_is_test: bool, optional
        :param xlabel: Label of the x-axis, defaults to 'Tests' if xaxis_is_test=True and 'Runs' if xaxis_is_test=False.
        :type xlabel: str
        :param xtick_rot: rotation of the x-axis tick labels, defaults to 30.
        :type xtick_rot: float
        :param xtick_labels_dict: Maps test_names (keys) to x-axis tick labels (values).
        :type xtick_labels_dict: dict, optional
        :param kwargs: Options to pass to matplotlib.pyplot.bar.
        """
        pass_rates = score_runs["pass_rate"]
        names = score_runs.index

        fig, ax = plt.subplots()
        ax.bar(names, pass_rates, **kwargs)

        # Title
        ax.set_title(title)

        # x-axis
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rot, ha="right")
        if xlabel is None:
            xlabel = "Tests" if xaxis_is_tests else "Score Runs"
        ax.set_xlabel(xlabel, fontweight="bold")
        if xtick_labels_dict:
            xtick_labels = [label.get_text() for label in ax.get_xticklabels()]
            new_labels = [xtick_labels_dict.get(label, label) for label in xtick_labels]
            ax.set_xticklabels(new_labels)

        # y-axis
        ax.set_ylabel(ylabel, fontweight="bold")

        if ylim_min is None:
            ylim_min = max(0, math.floor((min(pass_rates) - 0.001) * 10) / 10)
        if ylim_max is None:
            ylim_max = min(1, ax.get_ylim()[1])
        ax.set_ylim(bottom=ylim_min, top=ylim_max)

        if yaxis_is_percent:

            def to_percent(y, _):
                return f"{y * 100:.0f}%"

            ax.yaxis.set_major_formatter(FuncFormatter(to_percent))

        plt.tight_layout()
        plt.show()