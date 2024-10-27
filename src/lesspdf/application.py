"""Main logic for the application."""

from types import FrameType

import click

from lesspdf.document import Document
from term_image.image import AutoImage  # type: ignore


class Application:
    """Main application class."""

    UP: int = 1
    DOWN: int = -1
    IN: int = 1
    OUT: int = -1

    def __init__(self, document: Document) -> None:
        """Initialize application with a parsed document.

        Setup will open the document, set up the terminal
        and display the first page.
        """
        self.document = document
        click.echo(f"Creating application with file: {document.file}")

        try:
            self.image = AutoImage(document.get_page_image())
        except Exception as e:
            raise TerminalSetupError(str(e)) from e

        click.clear()
        self.image.draw()

    def go_to_page_relative(self, page_offset: int) -> None:
        """Move to a page relative to the current page."""
        self.document.page_number += page_offset
        click.echo(f"Going to page {self.document.page_number}.")

    def zoom(self, direction: int) -> None:
        """Zoom in or out on the document."""
        if direction == self.IN:
            click.echo("Zooming in.")
        elif direction == self.OUT:
            click.echo("Zooming out.")

    def scroll(self, direction: int) -> None:
        """Scroll the document."""
        if direction == self.UP:
            click.echo("Scrolling up.")
        elif direction == self.DOWN:
            click.echo("Scrolling down.")

    def resize_handler(self, _signum: int, _frame: FrameType | None) -> None:
        """Handle window resize signal."""
        click.echo(f"Signal {_signum} received.")
        click.echo("Window resized.")


class TerminalSetupError(Exception):
    """Error raised when the terminal cannot be set up."""

    def __init__(self, message: str) -> None:
        """Initialize the error with a message from the original exception."""
        super().__init__(f"Terminal setup error: {message}")
