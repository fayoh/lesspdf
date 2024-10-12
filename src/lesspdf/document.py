"""Class for handling the document object."""

from pathlib import Path

import pymupdf  # type: ignore
from pymupdf import FileDataError  # type: ignore


class Document:
    """Class for handling the document object."""

    def __init__(self, path: Path) -> None:
        """Initialize the document object from a file.

        Args:
            path (Path): The path to the document file.
            throws DocumentFileError: If the file cannot be opened.
        """
        self.file: Path = path
        self.page_number: int = 0
        try:
            self._document = pymupdf.open(str(self.file))
        except FileDataError as e:
            raise DocumentFileError(str(self.file)) from e


class DocumentFileError(Exception):
    """Error raised when a document file cannot be opened."""

    def __init__(self, file_path: str) -> None:
        """Initialize the error with the file path."""
        super().__init__(f"Could not open: {file_path}")
