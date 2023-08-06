# zettelkasten/cli.py
# type: ignore[attr-defined]

from typing import Optional

import random
from enum import Enum

import typer
from rich.console import Console

from . import __version__


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="zettelkasten",
    help="Folder based zettelkasten with a bibtex reference system and emacs "
    + "org-mode file zettels",
    add_completion=False,
)
console = Console()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        # callback=version_callback,
        # is_eager=True,
        help="Prints the version of the zettelkasten package.",
    ),
):
    """ Prints the version of the package"""
    console.print(
        f"[yellow]zettelkasten[/] version: [bold blue]{__version__}[/]"
    )
    raise typer.Exit()


@app.command()
def add():
    """Adds a Zettel"""
    typer.echo("Adding Zettel")


@app.command()
def change():
    """Change a Zettel"""
    typer.echo("Change Zettel")
