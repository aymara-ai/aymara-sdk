"""
Aymara AI SDK

This module provides the main interface for interacting with the Aymara AI API.
It includes functionality for creating and managing tests, scoring tests, and visualizing results.
"""

from __future__ import annotations

import math
import os
import textwrap
from typing import List, Dict, Optional, Union, Tuple

import pandas as pd
import matplotlib.image as mpimg
import matplotlib.patches as patches
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
from aymara_ai.types import AccuracyScoreRunResponse, SafetyTestResponse, ScoreRunResponse
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
        accuracy_score_run,
    ) -> pd.DataFrame:
        df_scores = accuracy_score_run.to_scores_df()

        pass_stats = df_scores.groupby(by="question_type")["is_passed"].agg(
            pass_rate="mean",
            pass_total="sum",
        )

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
    def graph_accuracy_score_run(
        accuracy_score_run: AccuracyScoreRunResponse,
        title: str = "Pass Rate by Question Type",
        xlabel: Optional[str] = None,
        ylabel: str = "Pass Rate",
        xtick_rot: float = 45,
        ylim_min: Optional[float] = None,
        ylim_max: Optional[float] = None,
        yaxis_is_percent: bool = True,
        xtick_labels_dict: Optional[dict] = None,
        **kwargs,
    ):
        """Plot pass rates by question type for an accuracy test score run.

        :param accuracy_score_run: Accuracy score run to plot.
        :type accuracy_score_run: AccuracyScoreRunResponse
        :param title: Plot title.
        :type title: str
        :param xlabel: x-axis label. If None, defaults to "Question Types".
        :type xlabel: str, optional
        :param ylabel: y-axis label.
        :type ylabel: str
        :param xtick_rot: Rotation of x-axis tick labels in degrees.
        :type xtick_rot: float
        :param ylim_min: Minimum y-axis limit. If None, defaults to floor of minimum pass rate.
        :type ylim_min: float, optional
        :param ylim_max: Maximum y-axis limit. If None, defaults to 1 or matplotlib default.
        :type ylim_max: float, optional
        :param yaxis_is_percent: Whether to format y-axis as percentages.
        :type yaxis_is_percent: bool
        :param xtick_labels_dict: Dictionary mapping x-tick labels to new labels.
        :type xtick_labels_dict: dict, optional
        :param kwargs: Options to pass to matplotlib.pyplot.bar.
        """
        if not accuracy_score_run.answers:
            raise ValueError("Score run has no answers")

        # Group answers by question type and calculate pass rates
        question_types = {}
        for answer in accuracy_score_run.answers:
            question = next(
                q
                for q in accuracy_score_run.answers
                if q.question_uuid == answer.question_uuid
            )
            if not question.accuracy_question_type:
                continue
            if question.accuracy_question_type not in question_types:
                question_types[question.accuracy_question_type] = {
                    "passed": 0,
                    "total": 0,
                }
            if answer.is_passed is not None:
                question_types[question.accuracy_question_type]["total"] += 1
                if answer.is_passed:
                    question_types[question.accuracy_question_type]["passed"] += 1

        names = list(question_types.keys())
        pass_rates = [
            question_types[qt]["passed"] / question_types[qt]["total"] for qt in names
        ]

        fig, ax = plt.subplots()
        ax.bar(names, pass_rates, **kwargs)

        # Title
        ax.set_title(title)

        # x-axis
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=xtick_rot, ha="right")
        if xlabel is None:
            xlabel = "Question Types"
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
    def show_image_test_answers(
        tests: List[SafetyTestResponse],
        test_answers: Dict[str, List[StudentAnswerInput]],
        score_runs: Optional[List[ScoreRunResponse]] = None,
        n_images_per_test: Optional[int] = 5,
        figsize: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Display a grid of image test answers with their test questions as captions.
        If score runs are included, display their test scores as captions instead
        and add a red border to failed images.

        :param tests: Tests corresponding to the test answers.
        :type tests: List of SafetyTestResponse objects.
        :param test_answers: Test answers.
        :type test_answers: Dictionary of test UUIDs to lists of StudentAnswerInput objects.
        :param score_runs: Score runs corresponding to the test answers.
        :type score_runs: List of ScoreRunResponse objects, optional
        :param n_images_per_test: Number of images to display per test.
        :type n_images_per_test: int, optional
        :param figsize: Figure size. Defaults to (n_images_per_test * 3, n_tests * 2 * 4).
        :type figsize: integer tuple, optional
        """
        import matplotlib.patches as patches
        import matplotlib.image as mpimg
        import textwrap
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec

        def display_image_group(axs, images, captions):
            for ax, img_path, caption in zip(axs, images, captions):
                img = mpimg.imread(img_path)
                ax.imshow(img)
                ax.set_title("\n".join(textwrap.wrap(caption, width=30)), fontsize=10, wrap=True, loc="left")
                ax.axis("off")

                if caption.startswith("Fail"):
                    rect = patches.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="red", linewidth=5, fill=False)
                    ax.add_patch(rect)

        # Create the figure and gridspec layout
        n_tests = len(test_answers)
        total_rows = n_tests * 2
        fig = plt.figure(figsize=figsize or (n_images_per_test * 3, total_rows * 4))
        gs = gridspec.GridSpec(total_rows, n_images_per_test, figure=fig, height_ratios=[1, 20] * n_tests)
        fig.subplots_adjust(hspace=0.1, wspace=0.1)

        row = 0
        for test_uuid, answers in test_answers.items():
            test = next(t for t in tests if t.test_uuid == test_uuid)

            # Title row
            ax_title = fig.add_subplot(gs[row, :])
            ax_title.text(.5, 0, test.test_name, fontsize=16, fontweight="bold", ha="center", va="top")
            ax_title.axis("off")
            row += 1

            # Image row
            images = [a.answer_image_path for a in answers[:n_images_per_test]]
            if score_runs is None:
                captions = [
                    next(q.question_text for q in test.questions if q.question_uuid == a.question_uuid)
                    for a in answers[:n_images_per_test]
                ]
            else:
                score_run = next(s for s in score_runs if s.test.test_uuid == test_uuid)
                scores = [
                    next(s for s in score_run.answers if s.question_uuid == a.question_uuid) 
                    for a in answers[:n_images_per_test]
                ]
                captions = [
                    f"{'Pass' if s.is_passed else 'Fail'} ({s.confidence:.1%} confidence): {s.explanation}" 
                    for s in scores
                ]

            axs = [fig.add_subplot(gs[row, col]) for col in range(len(images))]
            display_image_group(axs, images, captions)
            row += 1

        plt.tight_layout()
        plt.show()
