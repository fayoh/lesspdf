"""CLI: handle user input and call application layer."""

import signal
import sys
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import NoReturn

import click

from lesspdf.application import Application, TerminalSetupError
from lesspdf.document import Document, DocumentFileError


@dataclass(frozen=True)
class _InputKeys:
    """Input keys for the CLI."""

    K_ESC: str = "\x1b"
    K_RT: str = K_ESC + "[C"
    K_LT: str = K_ESC + "[D"
    K_UP: str = K_ESC + "[A"
    K_DN: str = K_ESC + "[B"
    K_HOME: str = K_ESC + "[H"
    K_END: str = K_ESC + "[F"
    K_PAGE_UP: str = K_ESC + "[5~"
    K_PAGE_DOWN: str = K_ESC + "[6~"
    QUIT: str = "q"
    NEXT_PAGE: str = "n"
    PREV_PAGE: str = "p"
    ZOOM_IN: str = "+"
    ZOOM_OUT: str = "-"


InputKeys = _InputKeys()


def create_key_function_map(app: Application) -> dict[str, Callable]:
    """Create a mapping of keys to functions."""
    return {
        InputKeys.NEXT_PAGE: partial(app.go_to_page_relative, page_offset=1),
        InputKeys.PREV_PAGE: partial(app.go_to_page_relative, page_offset=-1),
        InputKeys.K_PAGE_UP: partial(app.go_to_page_relative, page_offset=1),
        InputKeys.K_PAGE_DOWN: partial(app.go_to_page_relative, page_offset=-1),
        InputKeys.K_UP: partial(app.scroll, direction=app.UP),
        InputKeys.K_DN: partial(app.scroll, direction=app.DOWN),
        InputKeys.ZOOM_IN: partial(app.zoom, direction=app.IN),
        InputKeys.ZOOM_OUT: partial(app.zoom, direction=app.OUT),
        InputKeys.QUIT: sys.exit,
    }


@click.command()
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
)
def main(file: Path) -> NoReturn:
    """Start the application."""
    click.echo(f"Hello from lesspdf! Opening {file}.")

    try:
        document = Document(file)
    except DocumentFileError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)

    try:
        app = Application(document)
    except TerminalSetupError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)

    # Install signal handler for window resize
    signal.signal(signal.SIGWINCH, app.resize_handler)

    key_function_map = create_key_function_map(app)

    while True:
        user_input = click.getchar()
        if fun := key_function_map.get(user_input):
            fun()
