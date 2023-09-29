from pathlib import Path

import click

directory = click.argument("directory", type=click.Path(exists=True))
extension = click.argument("extension", nargs=-1)


@click.group()
def cli():
    pass


@cli.command("audio")
@directory
@extension
def sort_audio(directory: Path, extension: tuple):
    """Sort by audio."""

    return directory
