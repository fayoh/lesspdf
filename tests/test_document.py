from pathlib import Path

import pytest

from lesspdf.document import Document, DocumentFileError


def test_document_initialization_with_valid_file(tmp_path) -> None:
    """Test Document initialization with a valid file."""
    # Create a temporary file
    temp_file = tmp_path / "test.pdf"
    temp_file.write_text("dummy content")

    # Initialize Document with the temporary file
    doc = Document(temp_file)

    # Assertions
    assert doc.file == temp_file
    assert doc.page_number == 0


def test_document_initialization_with_invalid_file() -> None:
    """Test Document initialization with an invalid file."""
    # Path to a non-existent file
    invalid_file = Path("/non/existent/file.pdf")

    # Expect DocumentFileError to be raised
    with pytest.raises(DocumentFileError) as exc_info:
        Document(invalid_file)

    # Assertions
    assert str(exc_info.value) == f"Could not open: {invalid_file}"
