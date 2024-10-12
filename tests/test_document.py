"""Unit tests for the Document class."""

from importlib.resources import as_file, files
from pathlib import Path

import pytest

from lesspdf.document import Document, DocumentFileError
from tests import resources

resource_dir = files(resources)


def test_document_initialization_with_valid_file(tmp_path: Path) -> None:
    """Test Document initialization with a valid file."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        doc = Document(pdf)

    # Assertions
    assert doc.file == pdf
    assert doc.page_number == 0


def test_document_initialization_with_invalid_file() -> None:
    """Test Document initialization with an invalid file."""
    # Expect DocumentFileError to be raised
    with as_file(resource_dir.joinpath("corrupt.pdf")) as pdf, pytest.raises(DocumentFileError) as exc_info:
        Document(pdf)
