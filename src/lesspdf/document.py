"""Class for handling the document object."""

from functools import cached_property
from pathlib import Path

import PIL
import PIL.Image
import pymupdf  # type: ignore
from pymupdf import FileDataError  # type: ignore

# TODO: page_number should be a property with a setter that checks the value
# against the number of pages in the document.


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

    @cached_property
    def num_pages(self) -> int:
        """Return the number of pages in the document."""
        return len(self._document)

    def get_page_image(self) -> PIL.Image.Image:
        """Return an image of the current page.

        Returns:
            PIL.Image.Image: The image of the current page.
        """
        # TODO: Only generate the image if the page number or zoom level has changed. (delete the property when changing any settings)
        # Bit of a hack to get the page image without exporting a pixmap
        # and then converting it to an image and opening in pillow.
        # Comes from a pr to pymupdf that hasn't been merged yet
        #
        # https://github.com/pymupdf/PyMuPDF/pull/3911
        new_pixmap = self._document.get_page_pixmap(pno=self.page_number)
        colorspace = new_pixmap.colorspace
        if colorspace is None:
            mode = "L"
        elif colorspace.n == 1:
            mode = "L" if new_pixmap.alpha == 0 else "LA"
        elif colorspace.n == 3:
            mode = "RGB" if new_pixmap.alpha == 0 else "RGBA"
        else:
            mode = "CMYK"

        self.page_image = PIL.Image.frombytes(
            mode,
            (new_pixmap.width, new_pixmap.height),
            new_pixmap.samples,
        )

        return self.page_image


class DocumentFileError(Exception):
    """Error raised when a document file cannot be opened."""

    def __init__(self, file_path: str) -> None:
        """Initialize the error with the file path."""
        super().__init__(f"Could not open: {file_path}")
