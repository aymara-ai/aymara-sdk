import os
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pandas as pd
import pytest

from aymara_ai import AymaraAI
from aymara_ai.generated.aymara_api_client.models.test_type import (
    TestType as AymaraTestType,
)
from aymara_ai.types import (
    AccuracyScoredAnswerResponse,
    AccuracyScoreRunResponse,
    BaseTestResponse,
    ScoredAnswerResponse,
    ScoreRunResponse,
    Status,
)


def test_aymara_ai_initialization():
    # Clear the AYMARA_API_KEY environment variable
    if "AYMARA_API_KEY" in os.environ:
        del os.environ["AYMARA_API_KEY"]
    with pytest.raises(ValueError):
        AymaraAI()  # No API key provided

    ai = AymaraAI(api_key="test_api_key")
    assert ai.client is not None

    ai_custom = AymaraAI(
        api_key="test_api_key",
        base_url="https://custom.api.com",
    )
    assert ai_custom.client._base_url == "https://custom.api.com"


def test_aymara_ai_context_manager():
    with patch("aymara_ai.core.sdk.client.Client") as mock_client:
        with AymaraAI(api_key="test_api_key") as ai:
            assert ai.client is not None
        mock_client.return_value._client.close.assert_called_once()


@pytest.mark.asyncio
async def test_aymara_ai_async_context_manager():
    with patch("aymara_ai.core.sdk.client.Client") as mock_client:
        mock_async_client = mock_client.return_value._async_client
        mock_async_client.aclose = AsyncMock()
        async with AymaraAI(api_key="test_api_key") as ai:
            assert ai.client is not None
        mock_async_client.aclose.assert_called_once()


@pytest.fixture
def mock_score_run_response():
    return ScoreRunResponse(
        score_run_uuid="test-uuid",
        score_run_status=Status.COMPLETED,
        pass_rate=0.5,
        test=BaseTestResponse(
            test_name="Test 1",
            test_uuid="test-test-uuid",
            test_status=Status.COMPLETED,
            test_type=AymaraTestType.SAFETY,
            organization_name="Organization 1",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Don't allow any unsafe answers",
            test_system_prompt=None,
        ),
        answers=[
            ScoredAnswerResponse(
                answer_uuid=f"answer-uuid-{i}",
                question_uuid=f"question-uuid-{i}",
                answer_text=f"Answer {i}",
                question_text=f"Question {i}",
                explanation=f"Explanation {i}",
                confidence=0.8,
                is_passed=i % 2 == 0,
            )
            for i in range(1, 11)
        ],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_get_pass_stats_single_run(mock_score_run_response):
    result = AymaraAI.get_pass_stats(mock_score_run_response)

    assert isinstance(result, pd.DataFrame)
    assert result.index.name == "score_run_uuid"
    assert list(result.columns) == ["test_name", "pass_rate", "pass_total"]
    assert result.loc["test-uuid", "test_name"] == "Test 1"
    assert result.loc["test-uuid", "pass_rate"] == 0.5
    assert result.loc["test-uuid", "pass_total"] == 5.0


def test_get_pass_stats_multiple_runs():
    score_runs = [
        ScoreRunResponse(
            score_run_uuid=f"uuid-{i}",
            score_run_status=Status.COMPLETED,
            pass_rate=0.5,
            test=BaseTestResponse(
                test_name=f"Test {i}",
                test_uuid=f"test-uuid-{i}",
                test_status=Status.COMPLETED,
                test_type=AymaraTestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
            ),
            answers=[
                ScoredAnswerResponse(
                    answer_uuid=f"answer-uuid-{j}",
                    question_uuid=f"question-uuid-{j}",
                    answer_text=f"Answer {j}",
                    question_text=f"Question {j}",
                    explanation=f"Explanation {j}",
                    confidence=0.8,
                    is_passed=j < i,
                )
                for j in range(1, 11)
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for i in range(1, 4)
    ]

    result = AymaraAI.get_pass_stats(score_runs)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 3)
    assert list(result.index) == ["uuid-1", "uuid-2", "uuid-3"]
    assert list(result["pass_rate"]) == [0.5, 0.5, 0.5]
    assert list(result["pass_total"]) == [5.0, 5.0, 5.0]


@pytest.mark.parametrize("yaxis_is_percent", [True, False])
@pytest.mark.parametrize("xaxis_is_tests", [True, False])
def test_graph_pass_stats(mock_score_run_response, yaxis_is_percent, xaxis_is_tests):
    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "matplotlib.pyplot.show"
    ) as mock_show, patch("matplotlib.pyplot.tight_layout") as mock_tight_layout:
        mock_fig, mock_ax = Mock(), Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Mock the get_ylim() method to return a tuple
        mock_ax.get_ylim.return_value = (0, 1)

        AymaraAI.graph_pass_stats(
            [mock_score_run_response],
            title="Test Graph",
            yaxis_is_percent=yaxis_is_percent,
            xaxis_is_tests=xaxis_is_tests,
        )

        mock_subplots.assert_called_once()
        mock_ax.bar.assert_called_once()
        mock_ax.set_title.assert_called_once_with("Test Graph")
        mock_ax.set_xlabel.assert_called_once()
        mock_ax.set_ylabel.assert_called_once()
        mock_ax.set_ylim.assert_called_once()  # Add this assertion
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()


def test_graph_pass_stats_custom_options(mock_score_run_response):
    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "matplotlib.pyplot.show"
    ) as mock_show, patch("matplotlib.pyplot.tight_layout") as mock_tight_layout:
        mock_fig, mock_ax = Mock(), Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Mock the get_ylim() method to return a tuple
        mock_ax.get_ylim.return_value = (0, 1)

        # Mock the get_xticklabels() method to return a list of Mock objects
        mock_ax.get_xticklabels.return_value = [Mock(get_text=lambda: "Test 1")]

        AymaraAI.graph_pass_stats(
            [mock_score_run_response],
            title="Custom Graph",
            ylim_min=0.5,
            ylim_max=1.0,
            ylabel="Custom Y Label",
            xlabel="Custom X Label",
            xtick_rot=45.0,
            xtick_labels_dict={"Test 1": "Custom Test Label"},
            color="red",
        )

        mock_subplots.assert_called_once()
        mock_ax.bar.assert_called_once()
        mock_ax.set_title.assert_called_once_with("Custom Graph")
        mock_ax.set_xlabel.assert_called_once_with("Custom X Label", fontweight="bold")
        mock_ax.set_ylabel.assert_called_once_with("Custom Y Label", fontweight="bold")

        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()

        # Additional assertions to check if custom options are applied correctly
        mock_ax.set_ylim.assert_called_once_with(bottom=0.5, top=1.0)
        mock_ax.set_xticklabels.assert_called()

        # Check if xtick_labels_dict is applied correctly
        mock_ax.set_xticklabels.assert_any_call(
            mock_ax.get_xticklabels(), rotation=45.0, ha="right"
        )

        xtick_labels = [label.get_text() for label in mock_ax.get_xticklabels()]
        new_labels = [
            {"Test 1": "Custom Test Label"}.get(label, label) for label in xtick_labels
        ]
        mock_ax.set_xticklabels.assert_any_call(new_labels)


def test_graph_pass_stats_multiple_runs():
    score_runs = [
        ScoreRunResponse(
            score_run_uuid=f"uuid-{i}",
            score_run_status=Status.COMPLETED,
            pass_rate=0.5,
            test=BaseTestResponse(
                test_name=f"Test {i}",
                test_uuid=f"test-uuid-{i}",
                test_status=Status.COMPLETED,
                test_type=AymaraTestType.SAFETY,
                organization_name="Organization 1",
                num_test_questions=10,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                test_policy="Don't allow any unsafe answers",
                test_system_prompt=None,
            ),
            answers=[
                ScoredAnswerResponse(
                    answer_uuid=f"answer-uuid-{j}",
                    question_uuid=f"question-uuid-{j}",
                    answer_text=f"Answer {j}",
                    question_text=f"Question {j}",
                    explanation=f"Explanation {j}",
                    confidence=0.8,
                    is_passed=j < i,
                )
                for j in range(1, 11)
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for i in range(1, 4)
    ]

    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "matplotlib.pyplot.show"
    ) as mock_show, patch("matplotlib.pyplot.tight_layout") as mock_tight_layout:
        mock_fig, mock_ax = Mock(), Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Mock the get_ylim() method to return a tuple
        mock_ax.get_ylim.return_value = (0, 1)

        AymaraAI.graph_pass_stats(score_runs)

        mock_subplots.assert_called_once()
        mock_ax.bar.assert_called_once()
        mock_ax.set_title.assert_called_once()
        mock_ax.set_xlabel.assert_called_once()
        mock_ax.set_ylabel.assert_called_once()
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()


@pytest.fixture
def mock_accuracy_score_run():
    return AccuracyScoreRunResponse(
        score_run_uuid="test-uuid",
        score_run_status=Status.COMPLETED,
        test=BaseTestResponse(
            test_name="Accuracy Test",
            test_uuid="test-test-uuid",
            test_status=Status.COMPLETED,
            test_type=AymaraTestType.ACCURACY,
            organization_name="Organization 1",
            num_test_questions=10,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Test accuracy",
            test_system_prompt=None,
        ),
        answers=[
            AccuracyScoredAnswerResponse(
                answer_uuid=f"answer-uuid-{i}",
                question_uuid=f"question-uuid-{i}",
                answer_text=f"Answer {i}",
                question_text=f"Question {i}",
                explanation=f"Explanation {i}",
                confidence=0.8,
                is_passed=i % 2 == 0,
                accuracy_question_type="type_" + str((i % 3) + 1),
            )
            for i in range(1, 11)
        ],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_get_pass_stats_accuracy(mock_accuracy_score_run):
    result = AymaraAI.get_pass_stats_accuracy(mock_accuracy_score_run)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["question_type", "pass_rate", "pass_total"]
    assert len(result.index) == 3  # Three different question types
    assert all(0 <= rate <= 1 for rate in result["pass_rate"])
    assert all(isinstance(total, (int, float)) for total in result["pass_total"])


def test_graph_accuracy_score_run(mock_accuracy_score_run):
    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "matplotlib.pyplot.show"
    ) as mock_show, patch("matplotlib.pyplot.tight_layout") as mock_tight_layout:
        mock_fig, mock_ax = Mock(), Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_ax.get_ylim.return_value = (0, 1)
        mock_ax.get_xticklabels.return_value = [
            Mock(get_text=lambda: f"type_{i}") for i in range(1, 4)
        ]

        AymaraAI.graph_pass_stats_accuracy(mock_accuracy_score_run)

        mock_subplots.assert_called_once()
        mock_ax.bar.assert_called_once()
        mock_ax.set_xlabel.assert_called_once_with("Question Types", fontweight="bold")
        mock_ax.set_ylabel.assert_called_once_with("Answers Passed", fontweight="bold")
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()


def test_graph_accuracy_score_run_custom_options(mock_accuracy_score_run):
    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "matplotlib.pyplot.show"
    ) as mock_show, patch("matplotlib.pyplot.tight_layout") as mock_tight_layout:
        mock_fig, mock_ax = Mock(), Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_ax.get_ylim.return_value = (0, 1)
        mock_ax.get_xticklabels.return_value = [
            Mock(get_text=lambda: f"type_{i}") for i in range(1, 4)
        ]

        AymaraAI.graph_pass_stats_accuracy(
            mock_accuracy_score_run,
            title="Custom Accuracy Graph",
            ylim_min=0.2,
            ylim_max=0.8,
            ylabel="Custom Y Label",
            xlabel="Custom X Label",
            xtick_rot=60.0,
            xtick_labels_dict={"type_1": "Type One"},
            color="blue",
        )

        mock_subplots.assert_called_once()
        mock_ax.bar.assert_called_once()
        mock_ax.set_title.assert_called_once_with("Custom Accuracy Graph")
        mock_ax.set_xlabel.assert_called_once_with("Custom X Label", fontweight="bold")
        mock_ax.set_ylabel.assert_called_once_with("Custom Y Label", fontweight="bold")
        mock_ax.set_ylim.assert_called_once_with(bottom=0.2, top=0.8)
        mock_tight_layout.assert_called_once()
        mock_show.assert_called_once()


def test_graph_accuracy_score_run_empty_answers():
    empty_score_run = AccuracyScoreRunResponse(
        score_run_uuid="test-uuid",
        score_run_status=Status.COMPLETED,
        test=BaseTestResponse(
            test_name="Empty Test",
            test_uuid="test-uuid",
            test_status=Status.COMPLETED,
            test_type=AymaraTestType.ACCURACY,
            organization_name="Organization 1",
            num_test_questions=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            test_policy="Test accuracy",
            test_system_prompt=None,
        ),
        answers=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    with pytest.raises(ValueError, match="Score run test-uuid has no answers"):
        AymaraAI.graph_pass_stats([empty_score_run])
