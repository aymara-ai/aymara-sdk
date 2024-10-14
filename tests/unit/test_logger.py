from unittest.mock import MagicMock, patch

import pytest

from aymara_ai.types import Status
from aymara_ai.utils.logger import SDKLogger


@pytest.fixture
def sdk_logger():
    return SDKLogger()


def test_sdk_logger_initialization(sdk_logger):
    assert isinstance(sdk_logger, SDKLogger)
    assert sdk_logger.name == "sdk"
    assert sdk_logger.level == 10  # DEBUG level


def test_progress_bar_context_manager(sdk_logger):
    with patch("aymara_ai.utils.logger.tqdm") as mock_tqdm:
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        with sdk_logger.progress_bar("Test", "123", Status.PENDING):
            assert "123" in sdk_logger.tasks
            assert sdk_logger.tasks["123"]["test_name"] == "Test"
            assert sdk_logger.tasks["123"]["status"] == Status.PENDING
            mock_pbar.update.assert_called_once()

        assert "123" not in sdk_logger.tasks


def test_update_progress_bar(sdk_logger):
    with patch("aymara_ai.utils.logger.tqdm") as mock_tqdm:
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        with sdk_logger.progress_bar("Test", "123", Status.PENDING):
            sdk_logger.update_progress_bar("123", Status.COMPLETED)
            assert sdk_logger.tasks["123"]["status"] == Status.COMPLETED
            mock_pbar.set_description_str.assert_called()
            if sdk_logger.is_notebook:
                assert mock_pbar.colour == "green"
            else:
                mock_pbar.set_description_str.assert_called_with(
                    sdk_logger._get_progress_description("123")
                )


def test_get_progress_description(sdk_logger):
    with patch("time.time", return_value=1000):
        sdk_logger.tasks["123"] = {
            "test_name": "Test",
            "uuid": "123",
            "status": Status.PENDING,
            "start_time": 900,
        }
        description = sdk_logger._get_progress_description("123")
        assert "Test" in description
        assert "123" in description
        assert "100s" in description
        assert Status.PENDING.name in description


@pytest.mark.parametrize(
    "status,expected_color",
    [
        (Status.PENDING, "orange"),
        (Status.COMPLETED, "green"),
        (Status.FAILED, "red"),
    ],
)
def test_update_progress_bar_colors(sdk_logger, status, expected_color):
    with patch("aymara_ai.utils.logger.tqdm") as mock_tqdm:
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        with sdk_logger.progress_bar("Test", "123", Status.PENDING):
            sdk_logger.update_progress_bar("123", status)
            if sdk_logger.is_notebook:
                assert mock_pbar.colour == expected_color
            else:
                mock_pbar.set_description_str.assert_called_with(
                    sdk_logger._get_progress_description("123")
                )
