from importlib.resources import as_file, files
from pathlib import Path
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
    with pytest.raises(DocumentFileError, match=r"File does not") as exc_info:
        Document(Path("non-existent.pdf"))
    assert "File does not exist" in str(exc_info.value)

    with pytest.raises(DocumentFileError), as_file(resource_dir) as r_dir:
        Document(r_dir)
