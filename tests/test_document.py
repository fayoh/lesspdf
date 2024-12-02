"""Unit tests for the Document class."""

from importlib.resources import as_file, files

import pytest

from lesspdf.document import Document, DocumentFileError
from tests import resources

resource_dir = files(resources)


def test_document_initialization_with_valid_file() -> None:
    """Test Document initialization with a valid file."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        doc = Document(pdf)

    expected_num_pages = 4
    # Assertions
    assert doc.file == pdf
    assert doc.page_number == 0
    assert doc.num_pages == expected_num_pages


def test_document_initialization_with_invalid_file() -> None:
    """Test Document initialization with an invalid file."""
    # Expect DocumentFileError to be raised
    with as_file(resource_dir.joinpath("corrupt.pdf")) as pdf, pytest.raises(DocumentFileError) as _exc_info:
        Document(pdf)


def test_get_page_image() -> None:
    """Test getting an image of a page."""
    with as_file(resource_dir.joinpath("example.pdf")) as pdf:
        doc = Document(pdf)
        image = doc.get_page_image()
        assert image is not None
        assert image.width > 0
        assert image.height > 0
