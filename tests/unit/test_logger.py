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


def test_progress_bar_upload_progress(sdk_logger):
    with patch("aymara_ai.utils.logger.tqdm") as mock_tqdm:
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        with sdk_logger.progress_bar(
            "Test", "123", Status.UPLOADING, upload_total=100
        ) as pbar:
            pbar.update_upload_progress(50)
            assert sdk_logger.tasks["123"]["upload_progress"] == 50
            mock_pbar.set_description_str.assert_called_with(
                sdk_logger._get_progress_description("123")
            )


def test_progress_bar_update_uuid(sdk_logger):
    with patch("aymara_ai.utils.logger.tqdm") as mock_tqdm:
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        with sdk_logger.progress_bar("Test", "123", Status.PENDING) as pbar:
            pbar.update_uuid("456")
            assert "123" not in sdk_logger.tasks
            assert "456" in sdk_logger.tasks
            assert sdk_logger.tasks["456"]["uuid"] == "456"


def test_warning_message_notebook(sdk_logger):
    with patch("aymara_ai.utils.logger.display") as mock_display:
        sdk_logger.is_notebook = True
        sdk_logger.warning("Check this link: https://example.com/test. More text")
        mock_display.assert_called_once()
        html_content = mock_display.call_args[0][0].data
        assert '<a href="https://example.com/test"' in html_content
        assert '<span style="color: orange;">' in html_content


def test_warning_message_terminal(sdk_logger):
    with patch("logging.Logger.warning") as mock_warning:
        sdk_logger.is_notebook = False
        test_message = "Test warning message"
        sdk_logger.warning(test_message)
        mock_warning.assert_called_once()


def test_is_running_in_notebook():
    with patch("IPython.get_ipython") as mock_get_ipython:
        # Test Jupyter notebook case
        mock_get_ipython.return_value.__class__.__name__ = "ZMQInteractiveShell"
        assert SDKLogger._is_running_in_notebook() is True

        # Test Terminal IPython case
        mock_get_ipython.return_value.__class__.__name__ = "TerminalInteractiveShell"
        assert SDKLogger._is_running_in_notebook() is False

        # Test other shell case
        mock_get_ipython.return_value.__class__.__name__ = "OtherShell"
        assert SDKLogger._is_running_in_notebook() is False

        # Test when IPython is not available
        mock_get_ipython.side_effect = NameError()
        assert SDKLogger._is_running_in_notebook() is False
