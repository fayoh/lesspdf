"""Unit tests for the Application class."""

from importlib.resources import as_file, files
from pathlib import Path
from signal import Signals
from unittest.mock import patch

import pytest

from lesspdf.application import Application
from lesspdf.document import Document, DocumentFileError
from tests import resources

resource_dir = files(resources)


def test_application_init() -> None:
    """Minimal test."""
    with (
        as_file(resource_dir.joinpath("example.pdf")) as pdf,
        patch("click.echo") as mock_echo,
    ):
        document = Document(pdf)
        app = Application(document)
        assert app.document == document
        mock_echo.assert_called_once()


def test_application_init_bad_file() -> None:
    """Minimal test."""
    non_existent_filename = "non-existent.pdf"
    with pytest.raises(DocumentFileError, match=f".*{non_existent_filename}") as exc_info:
        Document(Path(non_existent_filename))

    with pytest.raises(DocumentFileError), as_file(resource_dir) as r_dir:
        Document(r_dir)
    assert "Could not open" in str(exc_info.value)

    # with pytest.raises(DocumentFileError), as_file(resource_dir.joinpath("corrupt.pdf")):
    #     Document(resource_dir.joinpath("example.txt"))


def test_application_go_to_page_relative() -> None:
    """Test moving to a page relative to the current page."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        document = Document(pdf)
        app = Application(document)
        app.go_to_page_relative(1)
        assert document.page_number == 1
        app.go_to_page_relative(-1)
        assert document.page_number == 0


def test_application_zoom() -> None:
    """Test zooming in or out on the document."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        document = Document(pdf)
        app = Application(document)
        app.zoom(Application.IN)
        app.zoom(Application.OUT)


def test_application_scroll() -> None:
    """Test scrolling the document."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        document = Document(pdf)
        app = Application(document)
        app.scroll(Application.UP)
        app.scroll(Application.DOWN)


def test_application_resize_handler() -> None:
    """Test handling window resize signal."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        document = Document(pdf)
        app = Application(document)
        app.resize_handler(Signals.SIGWINCH, None)
