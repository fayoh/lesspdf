"""Class for handling the document object."""

from pathlib import Path


class Document:
    """Class for handling the document object."""

    def __init__(self, path: Path) -> None:
        """Initialize the document object from a file."""
        self.file: Path = path
        self.page_number: int = 0
        if not (self.file.exists() and self.file.is_file()):
            raise DocumentFileError(str(self.file))


class DocumentFileError(Exception):
    """Error raised when a document file cannot be opened."""

    def __init__(self, file_path: str) -> None:
        """Initialize the error with the file path."""
        super().__init__(f"Could not open: {file_path}")
