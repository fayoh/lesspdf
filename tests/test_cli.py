"""Tests for the CLI module."""

from importlib.resources import as_file, files
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from lesspdf.application import TerminalSetupError
from lesspdf.cli import main
from lesspdf.document import DocumentFileError
from tests import resources

resource_dir = files(resources)

@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking CLI commands."""
    return CliRunner()


# TODO: Use cli runner with temp dir for safety and point to any temporary file.
# When mocking the document class there is no need for real docuemtsn.


@pytest.mark.timeout(5)
@patch("lesspdf.cli.Application")
@patch("lesspdf.cli.Document")
def test_main_success(mock_document: MagicMock, mock_application: MagicMock, runner: CliRunner) -> None:
    """Test opening a valid file and immediately quit.

    Happy path and quit key is pressed.
    """
    mock_document.return_value = MagicMock()
    mock_application.return_value = MagicMock()

    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        result = runner.invoke(main, args=[str(pdf)], input="q")

    assert result.exit_code == 0


@pytest.mark.timeout(5)
def test_non_existant_file(runner: CliRunner) -> None:
    """Test opening a file that does not exist, expect error code."""
    result = runner.invoke(main, args=["/path/to/file.pdf"])

    assert result.exit_code == 2  # noqa: PLR2004
    assert "does not exist" in result.output


@pytest.mark.timeout(5)
@patch("lesspdf.cli.Document", side_effect=DocumentFileError("test_marker_error"))
def test_corrupt_file(_mock_document: MagicMock, runner: CliRunner) -> None:  # noqa: PT019
    """Test opening a corrupt file, expect error code."""
    # TODO: CLI must catch the exception
    file_path = "tests/resources/example.pdf"
    result = runner.invoke(main, args=[file_path])
    assert result.exit_code == 1
    assert "test_marker_error" in result.output

@pytest.mark.timeout(5)
@patch("lesspdf.cli.Document")
@patch("lesspdf.cli.Application", side_effect=TerminalSetupError("Terminal error"))
def test_main_terminal_setup_error(_mock_application: MagicMock, _mock_document: MagicMock, runner: CliRunner) -> None:  # noqa: PT019
    """Test application exits if not able to setup terminal."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        result = runner.invoke(main, args=[str(pdf)])
    assert result.exit_code == 1

#@pytest.mark.timeout(5)
@patch("lesspdf.cli.Document")
@patch("lesspdf.cli.Application")
def test_input(mock_application: MagicMock, _mock_document: MagicMock, runner: CliRunner) -> None:  # noqa: PT019
    """Test application methods are called from inp."""
    input_str = "np+-q"
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        result = runner.invoke(main, args=[str(pdf)], input=input_str)
    assert result.exit_code == 0
    # 1 for each key press + resize_handler and init
    assert len(mock_application.mock_calls) == len(input_str) + 1

# @pytest.mark.timeout(5)
# @patch("lesspdf.cli.signal.signal")
# @patch("lesspdf.cli.create_key_function_map")
# @patch("lesspdf.cli.Document")
# @patch("lesspdf.cli.Application")
# def test_main_signal_handler(
#     mock_application: MagicMock, mock_document: MagicMock, mock_create_key_function_map: MagicMock, mock_signal: MagicMock, runner: CliRunner,
# ) -> None:
#     """Test that the signal handler is installed and called when the window is resized."""
#     mock_document.return_value = MagicMock()
#     mock_application.return_value = MagicMock()
#     mock_create_key_function_map.return_value = {}
#
#     with patch("lesspdf.cli.click.getchar", side_effect=["q"]):
#         result = runner.invoke(main, ["/path/to/file.pdf"])
#
#     mock_signal.assert_called_once()
#     mock_create_key_function_map.assert_called_once()
#     assert result.exit_code == 0
