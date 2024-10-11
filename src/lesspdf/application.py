"""Main logic for the application."""

from types import FrameType

import click

from lesspdf.document import Document


class Application:
    """Main application class."""

    UP: int = 1
    DOWN: int = -1
    IN: int = 1
    OUT: int = -1

    def __init__(self, document: Document) -> None:
        """Initialize application with a parsed document.

        Setup will open the document and setup the terminal.
        """
        self.document = document
        click.echo(f"Creating application with file: {document.file}")

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
