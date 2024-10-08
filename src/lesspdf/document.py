"""Class for handling the document object."""


from pathlib import Path


class Document:
    """Class for handling the document object."""

    def __init__(self, path: Path) -> None:
        """Initialize the document object from a file."""
        self.file: Path = path
        self.page_number: int = 0
        if not (self.file.exists() and self.file.is_file()):
            raise DocumentFileError(f"File does not exist: {self.file}")


class DocumentFileError(Exception):
    """Error raised when a document file cannot be opened."""
