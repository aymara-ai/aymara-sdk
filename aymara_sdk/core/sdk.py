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

from aymara_sdk.core.protocols import AymaraAIProtocol
from aymara_sdk.core.score_run import ScoreRunMixin
from aymara_sdk.core.tests import TestMixin
from aymara_sdk.generated.aymara_api_client import (
    client,
)
from aymara_sdk.types import BaseScoreRunResponse
from aymara_sdk.utils.constants import DEFAULT_MAX_WAIT_TIME
from aymara_sdk.utils.logger import SDKLogger


class AymaraAI(
    TestMixin,
    ScoreRunMixin,
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
    :param max_wait_time: Maximum wait time for test creation, defaults to {DEFAULT_MAX_WAIT_TIME}.
    :type max_wait_time: int, optional
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.aymara.ai",
        max_wait_time: int = DEFAULT_MAX_WAIT_TIME,
    ):
        self.logger = SDKLogger()

        if api_key is None:
            api_key = os.getenv("AYMARA_API_KEY")
        if api_key is None:
            self.logger.error("API key is required")
            raise ValueError("API key is required")

        self.client = client.Client(base_url=base_url, headers={"x-api-key": api_key})
        self.max_wait_time = max_wait_time
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
        score_runs: Union[List[BaseScoreRunResponse], BaseScoreRunResponse],
    ) -> pd.DataFrame:
        """
        Create a DataFrame of pass rates and pass totals from one or more score runs.

        :param score_runs: List of test score runs to graph.
        :type score_runs: List[ScoreTestResponse]
        :return: DataFrame of pass rates per score run.
        :rtype: pd.DataFrame
        """
        if isinstance(score_runs, BaseScoreRunResponse):
            score_runs = [score_runs]

        return pd.DataFrame(
            data={
                "test_name": [score.test_name for score in score_runs],
                "pass_rate": [score.pass_rate() for score in score_runs],
                "pass_total": [
                    score.pass_rate() * score.num_test_questions for score in score_runs
                ],
            },
            index=pd.Index(
                [score.score_run_uuid for score in score_runs], name="score_run_uuid"
            ),
        )

    @staticmethod
    def graph_pass_rates(
        score_runs: Union[List[BaseScoreRunResponse], BaseScoreRunResponse],
        title: Optional[str] = None,
        ylim_min: Optional[float] = None,
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
        :param ylim_min: y-axis lower limit, defaults to rounding down to the nearest decimal (yaxis_is_percent=True) or ten (yaxis_is_percent=False).
        :type ylim_min: float, optional
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
        if isinstance(score_runs, BaseScoreRunResponse):
            score_runs = [score_runs]

        pass_rates = [score.pass_rate() for score in score_runs]
        names = [
            score.test_name if xaxis_is_tests else score.score_run_uuid
            for score in score_runs
        ]

        if ylim_min is None:
            ylim_min = math.floor(min(pass_rates) * 10) / 10

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
        if yaxis_is_percent:

            def to_percent(y, _):
                return f"{y * 100:.0f}%"

            ax.yaxis.set_major_formatter(FuncFormatter(to_percent))

        plt.tight_layout()
        plt.show()